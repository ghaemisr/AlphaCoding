# Talking about encryption and how we store passwords.

import hashlib

filename = "users.txt"


def contains_int(s):
    return any(i.isdigit() for i in s)


def contains_letters(s):
    return any(i.isalpha() for i in s)


def contains_special_char(s):
    special_chars = ["*", "_", "/", "@", "#", "$", "%"]
    return any((i in special_chars) for i in s)


def login(username, password):
    username = hashlib.md5(username.encode('UTF-8')).hexdigest()
    password = hashlib.md5(password.encode('UTF-8')).hexdigest()
    success = False
    with open(filename, "r+") as f:
        for credentials in f.readlines():
            if credentials == (username + "" + password + "\n"):
                success = True
    return success


def register(username, password):
    h_name = hashlib.md5(username.encode('UTF-8')).hexdigest()
    h_pass = hashlib.md5(password.encode('UTF-8')).hexdigest()
    # check if the username exists or not
    with open(filename, "r+") as f:
        for credentials in f.readlines():
            if credentials.startswith(h_name):
                print("Username is unavailable")
                return False

    # check password strength
    if contains_letters(password) and contains_int(password) and contains_special_char(password):
        with open(filename, "a") as f:
            f.write(h_name + "" + h_pass + "\n")
    else:
        print('weak password, must contain letters, numbers and' +
              'a special character ("*", "_", "/", "@", "#", "$", "%")')
        return False
    return True


if __name__ == "__main__":
    option = input("Login or Register (type l or r)")
    if option == "l":
        if login(input("Username: "), input("Password: ")):
            print("Login success")
        else:
            print("Invalid username or password")
    elif option == "r":
        if register(input("Username"), input("Password: ")):
            print("Registration success")
    else:
        print("l to login or r to register")
