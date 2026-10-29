from errors import UserNotFoundError, CannotDeleteError
from models import User


class AdminService:
    def __init__(self, storage):
        self.storage = storage

    def search(self, q):
        q = q.lower()
        result = []
        for user in self.storage.all():
            if q in user.login.lower():
                result.append(user)
        return result

    def deleteUser(self, admin, login):
        if login == admin.login:
            raise CannotDeleteError("Нельзя удалить самого себя")
        if self.storage.get(login) is None:
            raise UserNotFoundError("Пользователь не найден")
        if self.storage.get(login).role == "admin":
            raise CannotDeleteError("Нельзя удалить администратора")
        self.storage.delete(login)
