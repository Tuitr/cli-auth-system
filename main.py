from storage import UserStorage
from services.auth_service import AuthService
from services.user_service import UserService
from services.admin_service import AdminService
from ui.menus import GuestMenu, UserMenu, AdminMenu
from ui.app import App

def main():
    storage = UserStorage()
    authService = AuthService(storage)
    userService = UserService(storage)
    adminService = AdminService(storage)
    guestMenu = GuestMenu(authService)
    userMenu = UserMenu(userService)
    adminMenu = AdminMenu(userService, adminService)
    app = App(guestMenu, userMenu, adminMenu)
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nПрограмма завершена")

if __name__ == "__main__":
    main()