import json


cart = []


def add_to_cart():

    print("\n========== ADD TO CART ==========")

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


    choice = int(input("\nEnter Food ID: "))


    for food in foods:

        if food["id"] == choice:

            cart.append(food)

            print("\n✅", food["name"], "Added To Cart")

            return


    print("\n❌ Food Item Not Found")



def view_cart():

    print("\n========== YOUR CART ==========")

    if len(cart) == 0:
        print("Your Cart is Empty")
        return


    total = 0


    for item in cart:

        print(
            item["name"],
            "- ₹",
            item["price"]
        )

        total += item["price"]


    print("--------------------")
    print("Total Bill = ₹", total)