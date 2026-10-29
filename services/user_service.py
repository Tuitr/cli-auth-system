from errors import ValidationError, UserExistsError, WrongCredentialsError
from services.auth_service import validateLogin, validatePassword

class UserService:
    def __init__(self, storage):
        self.storage = storage

    def changePassword(self, user, oldPassword, newPassword):
        if oldPassword != user.password:
            raise WrongCredentialsError("Неверный текущий пароль")
        validatePassword(newPassword)
        if newPassword == oldPassword:
            raise ValidationError("Новый пароль совпадает со старым")
        user.password = newPassword
        self.storage.save(user)

    def changeLogin(self, user, newLogin):
        oldLogin = user.login
        if oldLogin == newLogin:
            raise ValidationError("Новый логин совпадает с текущим")
        validateLogin(newLogin)
        if self.storage.get(newLogin):
            raise UserExistsError("Логин уже занят")
        self.storage.delete(oldLogin)
        user.login = newLogin
        self.storage.save(user)
        return user
