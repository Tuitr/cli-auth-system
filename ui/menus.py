from errors import PassmanError
from ui.console import clear, info, success, error, ask, pause, printUsers
from ui.password_input import inputPassword

class GuestMenu:
    def __init__(self, auth):
        self.auth = auth

    def _register(self):
        clear()
        info("=== Регистрация ===")
        login = ask("Логин: ")
        password = inputPassword("Пароль: ")
        try:
            self.auth.register(login, password)
            success("Регистрация прошла успешно, теперь можно войти")
        except PassmanError as e:
            error(str(e))
        pause()

    def _login(self):
        clear()
        info("=== Введите логин и пароль ===")
        login = ask("Логин: ")
        password = inputPassword("Пароль: ")
        try:
            user = self.auth.login(login, password)
            success(f"Добро пожаловать, {user.login}!")
            pause()
            return user
        except PassmanError as e:
            error(str(e))
            pause()
            return None

    def _loginAdmin(self):
        clear()
        info("=== Введите логин и пароль ===")
        login = ask("Логин: ")
        password = inputPassword("Пароль: ")
        try:
            user = self.auth.loginAdmin(login, password)
            success(f"Добро пожаловать, {user.login}!")
            pause()
            return user
        except PassmanError as e:
            error(str(e))
            pause()
            return None


    def show(self):
        while True:
            clear()
            info("=== Менеджер паролей ===")
            info("1. Зарегистрироваться")
            info("2. Войти")
            info("3. Войти как администратор")
            info("0. Выход")
            choice = ask("Выберите пункт: ")
            match choice:
                case "1":
                    self._register()
                case "2":
                    user = self._login()
                    if user is not None:
                        return ("user", user)
                case "3":
                    user = self._loginAdmin()
                    if user is not None:
                        return ("admin", user)
                case "0":
                    return ("exit", None)
                case _:
                    error("Нет такого пункта")
                    pause()

class UserMenu:
    def __init__(self, userService):
        self.userService = userService

    def _changePassword(self, user):
        clear()
        info("=== Смена пароля ===")
        oldPassword = inputPassword("Введите текущий пароль: ")
        newPassword = inputPassword("Введите новый пароль: ")
        newPasswordCheck = inputPassword("Введите новый пароль еще раз: ")
        if newPassword != newPasswordCheck:
            error("Пароли не совпадают")
            pause()
            return
        try:
            self.userService.changePassword(user, oldPassword, newPassword)
            success("Пароль успешно изменен!")
        except PassmanError as e:
            error(str(e))
        pause()

    def _changeLogin(self, user):
        clear()
        info("=== Смена логина ===")
        newLogin = ask("Введите новый логин: ")
        try:
            self.userService.changeLogin(user, newLogin)
            success(f"Логин успешно изменен на {newLogin}!")
        except PassmanError as e:
            error(str(e))
        pause()

    def show(self, user):
        while True:
            clear()
            info(f"=== Личный кабинет: {user.login} ===")
            info("1. Изменить пароль")
            info("2. Изменить логин")
            info("0. Выйти")
            choice = ask("Выберите пункт: ")
            match choice:
                case "1":
                    self._changePassword(user)
                case "2":
                    self._changeLogin(user)
                case "0":
                    info("Вы вышли из аккаунта")
                    pause()
                    return
                case _:
                    error("Нет такого пункта")
                    pause()

class AdminMenu(UserMenu):
    def __init__(self, userService, adminService):
        super().__init__(userService)
        self.adminService = adminService

    def _search(self):
        clear()
        info("=== Поиск пользователей ===")
        query = ask("Введите логин или его часть (Enter — показать всех): ")
        printUsers(self.adminService.search(query))
        pause()

    def _delete(self, admin):
        clear()
        info("=== Удаление пользователя ===")
        userLogin = ask("Введите логин: ")
        choice = ask(f"Удалить {userLogin}? (да/нет): ")
        if choice.lower() != "да":
            info("Удаление отменено")
            pause()
            return
        try:
            self.adminService.deleteUser(admin, userLogin)
            success(f"Пользователь {userLogin} нахуй удален!")
        except PassmanError as e:
            error(str(e))
        pause()

    def show(self, user):
        while True:
            clear()
            info(f"=== Панель администратора: {user.login} ===")
            info("1. Найти пользователя")
            info("2. Удалить пользователя")
            info("3. Изменить пароль")
            info("0. Выйти")
            choice = ask("Выберите пункт: ")
            match choice:
                case "1":
                    self._search()
                case "2":
                    self._delete(user)
                case "3":
                    self._changePassword(user)
                case "0":
                    info("Вы вышли из аккаунта")
                    pause()
                    return
                case _:
                    error("Нет такого пункта")
                    pause()

