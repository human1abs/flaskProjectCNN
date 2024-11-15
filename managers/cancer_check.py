import os
import uuid

from werkzeug.exceptions import NotFound

from cnn_model.model_run import ModelPredict
from cnn_model.model_run import model
from constants import TEMP_FILE_FOLDER
from db import db
from models import RoleType, State
from models.cancer_check import CancerCheckModel
from services.s3 import S3Service
from utils.helpers import decode_photo


cnn = ModelPredict()
s3 = S3Service()


class CancerCheckManager:
    @staticmethod
    def get_all_cancer_checks_by_user(user):
        query = db.select(CancerCheckModel)
        if user.role == RoleType.user:
            query = query.filter_by(user_id=user.id)
        return db.session.execute(query).scalars().all()

    @staticmethod
    def create(data, user):
        data["user_id"] = user.id
        encoded_photo = data.pop("photo")
        extension = data.pop("photo_extension")
        name = f"{user.id}{str(uuid.uuid4())}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, f"{name}")
        decode_photo(path, encoded_photo)

        prediction = cnn.predict(path, model)
        data["result"] = f'{prediction}%'
        if prediction > 66:
            data['status'] = State.malignant
            data['description'] = f"Your skin formation is most probably malignant. You should visit a doctor ASAP!"
        elif prediction > 33:
            data['status'] = State.unclear
            data['description'] = "Our model cannot classify your skin formation with certainty. " \
                                  "We recommend that you visit a doctor for further testing"
        else:
            data['status'] = State.benign
            data['description'] = f"Your skin formation is most probably benign. No reasons to worry..."

        url = s3.upload_photo(path, name, extension)
        data["photo_url"] = url

        c = CancerCheckModel(**data)
        db.session.add(c)
        db.session.flush()

        return c

    @staticmethod
    def delete(id_):
        check = db.session.execute(db.select(CancerCheckModel).filter_by(id=id_)).scalar()
        if not check:
            raise NotFound

        db.session.delete(check)
        db.session.flush()
        return f"Cancer check with id: {id_} was successfully deleted."

    @staticmethod
    def malignant(id_):
        check = db.session.execute(db.select(CancerCheckModel).filter_by(id=id_)).scalar()

        if not check:
            raise NotFound
        check.status = State.malignant
        return f"Your skin formation is most probably {check.status.name}. " \
               f"You should visit a doctor ASAP!"

    @staticmethod
    def unclear(id_):
        check = db.session.execute(db.select(CancerCheckModel).filter_by(id=id_)).scalar()

        if not check:
            raise NotFound
        check.status = State.unclear

        return f"Our model cannot classify your skin formation with certainty. Status: {check.status.name}. " \
               f"We recommend that you visit a doctor for further testing"

    @staticmethod
    def benign(id_):
        check = db.session.execute(db.select(CancerCheckModel).filter_by(id=id_)).scalar()

        if not check:
            raise NotFound
        check.status = State.benign

        return f"Your skin formation is most probably {check.status.name}. " \
               f"No reasons to worry..."

