import getpass

def inputPassword(prompt):
    return getpass.getpass(prompt)

if __name__ == "__main__":
    password = inputPassword("Password: ")
    print(password)