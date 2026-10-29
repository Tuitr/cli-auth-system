from config import MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH, MAX_LOGIN_LENGTH, MIN_LOGIN_LENGTH
from errors import ValidationError, UserExistsError, WrongCredentialsError, NotAdminError
from storage import UserStorage
from models import User

def validatePassword(password):
    if not (MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH):
        raise ValidationError(f"Пароль должен быть от {MIN_PASSWORD_LENGTH} до {MAX_PASSWORD_LENGTH} символов")
    if " " in password:
        raise ValidationError(f"Пароль не должен содержать пробела")

def validateLogin(login):
    if not (MIN_LOGIN_LENGTH <= len(login) <= MAX_LOGIN_LENGTH):
        raise ValidationError(f"Логин должен быть от {MIN_LOGIN_LENGTH} до {MAX_LOGIN_LENGTH} символов")
    if " " in login:
        raise ValidationError(f"Логин не должен содержать пробела")

class AuthService:
    def __init__(self, storage):
        self.storage = storage

    def _authenticate(self, login, password):
        user = self.storage.get(login)
        if user is None or user.password != password:
            raise WrongCredentialsError("Неверный логин или пароль")
        return user

    def register(self, login, password):
        validateLogin(login)
        validatePassword(password)
        if self.storage.get(login) is not None:
            raise UserExistsError("Логин уже занят")
        user = User(login, password)
        self.storage.save(user)
        return user



    def login(self, login, password):
        user = self._authenticate(login, password)
        return user

    def loginAdmin(self, login, password):
        user = self._authenticate(login, password)
        if User.isAdmin(user) is False:
            raise NotAdminError("Вы не являетесь администратором!")
        return user
