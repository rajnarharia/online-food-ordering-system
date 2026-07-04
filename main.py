from modules.admin import admin_panel
from modules.order import place_order
from modules.cart import add_to_cart, view_cart
from modules.menu import show_menu
from modules.login import login
from modules.register import register

while True:
    print("\n" + "=" * 50)
    print("      ONLINE FOOD ORDERING SYSTEM")
    print("=" * 50)

    print("1. Login")
    print("2. Register")
    print("3. Show Food Menu")
    print("4. Add To Cart")
    print("5. View Cart")
    print("6. Place Order")
    print("7. Admin Panel")
    print("8. Exit")

    choice = input("\nEnter your choice (1-3): ")

    if choice == "1":
     login()

    elif choice == "2":
     register()

    elif choice == "3":
     show_menu()

    elif choice == "4":
     add_to_cart()

    elif choice == "5":
     view_cart()

    elif choice == "6":
     place_order()

    elif choice == "7":
     admin_panel()

    elif choice == "8":
      print("\nThank you for using Online Food Ordering System")
    break

else:
    print("\nInvalid Choice")