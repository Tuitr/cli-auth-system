import json

from config import DATA_FILE, DEFAULT_ADMIN, ROLE_ADMIN
from models import User

class UserStorage:
    def __init__(self, path=DATA_FILE):
        self.path = path
        if not self.path.exists():
            self._createDefault()

    def _createDefault(self):
        admin = User(DEFAULT_ADMIN["login"], DEFAULT_ADMIN["password"], ROLE_ADMIN)
        self._save({admin.login: admin})

    def _load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        users = {}
        for u in data["users"].values():
            user = User.fromDict(u)
            users[user.login] = user
        return users

    def _save(self, users):
        data = {"users": {}}
        for user in users.values():
            data["users"][user.login] = user.toDict()

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get(self, login):
        return self._load().get(login)


    def save(self, user):
        users = self._load()
        users[user.login] = user
        self._save(users)

    def delete(self, login):
        users = self._load()
        users.pop(login, None)
        self._save(users)

    def all(self):
        return list(self._load().values())

if __name__ == "__main__":
    s = UserStorage()
    print([u.login for u in s.all()])  # ['admin']
    s.save(User("nikita", "qwerty12"))
    print(s.get("nikita").createdAt)  # дата
    print(s.get("nobody"))  # None
    s.delete("nikita")
    print([u.login for u in s.all()])  # ['admin']