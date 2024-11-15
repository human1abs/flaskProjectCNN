from resources.auth import Register, Login, DeleteOwnAccount, Password
from resources.cancer_check import CancerCheck, MalignantChecks, BenignChecks, UnclearChecks, DeleteOwnCheck
from resources.user import DeleteUser, GetUser


routes = (
    (Register, "/register"),
    (Login, "/login"),
    (Password, "/user/change-password"),
    (DeleteOwnAccount, "/user/delete"),
    (CancerCheck, "/user/checks"),
    (DeleteOwnCheck, "/user/checks/<int:pk>/delete"),
    (MalignantChecks, "/admin/checks/<int:pk>/malignant"),
    (BenignChecks, "/admin/checks/<int:pk>/benign"),
    (UnclearChecks, "/admin/checks/<int:pk>/unclear"),
    (DeleteUser, "/admin/users/<int:pk>/delete"),
    (GetUser, "/admin/users/<int:pk>"),
)
