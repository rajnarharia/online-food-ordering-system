import json


def register():

    print("\n========== USER REGISTRATION ==========")

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    user = {
        "username": username,
        "password": password
    }


    with open("data/users.json", "r") as file:
        users = json.load(file)


    users.append(user)


    with open("data/users.json", "w") as file:
        json.dump(users, file, indent=4)


    print("\n✅ Registration Successful!")