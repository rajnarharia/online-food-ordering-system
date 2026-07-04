import json


def login():

    print("\n========== USER LOGIN ==========")

    username = input("Enter Username: ")
    password = input("Enter Password: ")


    with open("data/users.json", "r") as file:
        users = json.load(file)


    for user in users:

        if user["username"] == username and user["password"] == password:

            print("\n✅ Login Successful!")
            print("Welcome", username)

            return


    print("\n❌ Invalid Username or Password")