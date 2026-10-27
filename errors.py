class PassmanError(Exception):
    """Базовое исключение приложения, от него наследуются все остальные."""


class ValidationError(PassmanError):
    """Бросается, если логин или пароль не прошли проверку длины."""


class UserExistsError(PassmanError):
    """Бросается, если логин уже занят: при регистрации или смене логина."""


class UserNotFoundError(PassmanError):
    """Бросается, если пользователь с таким логином не найден."""


class WrongCredentialsError(PassmanError):
    """Бросается при неверном логине или пароле, а также при неверном старом пароле."""


class NotAdminError(PassmanError):
    """Бросается, если пользователь без роли admin пытается войти в панель администратора."""


class CannotDeleteError(PassmanError):
    """Бросается, если администратор пытается удалить себя или другого администратора."""

