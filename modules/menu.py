import json


def show_menu():

    print("\n========== FOOD MENU ==========")


    with open("data/foods.json", "r") as file:
        foods = json.load(file)


    for food in foods:

        print(
            food["id"],
            ".",
            food["name"],
            "- ₹",
            food["price"]
        )