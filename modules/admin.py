import json


# ADD FOOD FUNCTION
def add_food():

    print("\n========== ADD FOOD ==========")

    name = input("Enter Food Name: ")
    price = int(input("Enter Price: "))

    with open("data/foods.json", "r") as file:
        foods = json.load(file)

    new_food = {
        "id": len(foods) + 1,
        "name": name,
        "price": price
    }

    foods.append(new_food)

    with open("data/foods.json", "w") as file:
        json.dump(foods, file, indent=4)

    print("\n✅ Food Added Successfully")



# DELETE FOOD FUNCTION
def delete_food():

    print("\n========== DELETE FOOD ==========")

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

    food_id = int(input("\nEnter Food ID to Delete: "))

    for food in foods:

        if food["id"] == food_id:

            foods.remove(food)

            with open("data/foods.json", "w") as file:
                json.dump(foods, file, indent=4)

            print("\n✅ Food Deleted Successfully")

            return

    print("\n❌ Food Not Found")



# VIEW ORDERS FUNCTION
def view_orders():

    print("\n========== ALL ORDERS ==========")

    with open("data/orders.json", "r") as file:
        orders = json.load(file)


    if len(orders) == 0:
        print("No Orders Found")
        return


    count = 1


    for order in orders:

        print("\nOrder No:", count)

        for item in order["items"]:

            print(
                item["name"],
                "- ₹",
                item["price"]
            )

        print("Total Amount = ₹", order["total"])

        count += 1



# ADMIN PANEL FUNCTION
def admin_panel():

    print("\n========== ADMIN PANEL ==========")

    print("1. Add Food")
    print("2. Delete Food")
    print("3. View Orders")
    print("4. Back")


    choice = input("Enter Choice: ")


    if choice == "1":
        add_food()


    elif choice == "2":
        delete_food()


    elif choice == "3":
        view_orders()


    elif choice == "4":
        return


    else:
        print("Invalid Choice")