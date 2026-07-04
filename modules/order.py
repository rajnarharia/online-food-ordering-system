import json
from modules.cart import cart


def place_order():

    print("\n========== PLACE ORDER ==========")

    if len(cart) == 0:
        print("Your cart is empty")
        return


    total = 0

    for item in cart:
        total += item["price"]


    order = {
        "items": cart,
        "total": total
    }


    with open("data/orders.json", "r") as file:
        orders = json.load(file)


    orders.append(order)


    with open("data/orders.json", "w") as file:
        json.dump(orders, file, indent=4)


    cart.clear()


    print("\n✅ Order Placed Successfully!")
    print("Total Amount = ₹", total)