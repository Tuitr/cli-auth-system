from ui.console import info
class App:
    def __init__(self,guestMenu, userMenu, adminMenu):
        self.guestMenu = guestMenu
        self.userMenu = userMenu
        self.adminMenu = adminMenu

    def run(self):
        while True:
            action, user = self.guestMenu.show()
            match action:
                case "user":
                    self.userMenu.show(user)
                case "admin":
                    self.adminMenu.show(user)
                case "exit":
                    info("До свидания!")
                    return