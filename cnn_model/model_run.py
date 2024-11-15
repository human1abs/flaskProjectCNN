from keras.applications.vgg16 import preprocess_input
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img

model = load_model('//cnn_model/skin_cancer_model.keras')


class ModelPredict:
    @staticmethod
    def predict(image_path, model):
        image = load_img(image_path, target_size=(128, 128))
        image = img_to_array(image)
        image = image / 255.0
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        image = preprocess_input(image)
        yhat = model.predict(image)
        label = yhat[0][0]
        prediction = round(label*100, 2)

        return prediction




