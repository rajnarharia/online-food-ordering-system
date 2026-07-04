import streamlit as st
import json
import base64


# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="Food Ordering System",
    page_icon="🍔",
    layout="wide"
)



# ================= BACKGROUND + UI DESIGN =================

def add_bg(image_file):

    with open(image_file, "rb") as file:

        encoded = base64.b64encode(
            file.read()
        ).decode()


    st.markdown(
        f"""
        <style>


        /* MAIN BACKGROUND */

        .stApp {{

            background-image:
            url("data:image/jpg;base64,{encoded}");

            background-size: cover;

            background-position: center;

            background-repeat: no-repeat;

            background-attachment: fixed;

        }}



        /* SIDEBAR */

        [data-testid="stSidebar"] {{

            background:
            rgba(0,0,0,0.75);

            backdrop-filter:
            blur(15px);

        }}


        [data-testid="stSidebar"] * {{

            color:white !important;

        }}



        /* CHOOSE OPTION BOX */

        div[data-baseweb="select"] > div {{

            background:
            rgba(255,255,255,0.25)
            !important;

            backdrop-filter:
            blur(15px);

            border-radius:
            15px !important;


            border:
            1px solid
            rgba(255,255,255,0.5);

        }}



        div[data-baseweb="select"] span {{

            color:white !important;

            font-weight:bold;

        }}



        /* HOME FEATURE CARDS */

        .feature-card {{

            background:
            rgba(0,0,0,0.70);


            backdrop-filter:
            blur(12px);


            padding:
            28px;


            border-radius:
            20px;


            text-align:
            center;


            color:
            white;


            font-size:
            22px;


            font-weight:
            bold;


            border:
            1px solid
            rgba(255,255,255,0.3);


            box-shadow:
            0px 8px 25px
            rgba(0,0,0,0.6);


            margin-bottom:
            30px;

        }}



        h1,h2,h3,h4,p,label {{

            color:white !important;

        }}



        </style>
        """,
        unsafe_allow_html=True
    )



add_bg("images/banner.jpg")



# ================= SESSION =================

if "cart" not in st.session_state:

    st.session_state.cart=[]



# ================= HEADER =================

st.markdown(
"""
<h1 style='text-align:center;color:white;'>
🍔 Online Food Ordering System 🍕
</h1>

<h3 style='text-align:center;color:white;'>
Order Your Favourite Food Anytime 🚚
</h3>
""",
unsafe_allow_html=True
)


# ================= SIDEBAR =================

st.sidebar.title(
    "🍽️ Navigation Menu"
)


option=st.sidebar.selectbox(
    "Choose Option",
    [
        "Home",
        "Login",
        "Register",
        "Food Menu",
        "Cart",
        "View Cart",
        "Place Order",
        "Admin"
    ]
)



# ================= HOME =================

if option=="Home":


    st.markdown(
    """
    <h2 style='text-align:center;color:white;'>
    Welcome To Our Food Ordering Platform 😋
    </h2>
    """,
    unsafe_allow_html=True
    )


    c1,c2,c3=st.columns(3)


    with c1:
        st.success("🍕 Fresh Food")


    with c2:
        st.info("🚚 Fast Delivery")


    with c3:
        st.warning("💳 Easy Payment")


    c4,c5,c6=st.columns(3)


    with c4:
        st.success("⭐ Best Quality")


    with c5:
        st.info("⏰ 24/7 Service")


    with c6:
        st.warning("🎁 Special Offers")



# ================= REGISTER =================

elif option=="Register":


    st.header("📝 Register")


    username=st.text_input(
        "Username"
    )


    password=st.text_input(
        "Password",
        type="password"
    )


    if st.button("Register"):


        with open(
            "data/users.json","r"
        ) as file:

            users=json.load(file)


        users.append(
            {
            "username":username,
            "password":password
            }
        )


        with open(
            "data/users.json","w"
        ) as file:

            json.dump(
                users,
                file,
                indent=4
            )


        st.success(
            "Registration Successful ✅"
        )



# ================= LOGIN =================

elif option=="Login":


    st.header("🔐 Login")


    username=st.text_input(
        "Username"
    )


    password=st.text_input(
        "Password",
        type="password"
    )


    if st.button("Login"):


        with open(
            "data/users.json","r"
        ) as file:

            users=json.load(file)


        check=False


        for user in users:

            if (
            user["username"]==username
            and
            user["password"]==password
            ):

                check=True


        if check:

            st.success(
            "Login Successful ✅"
            )

        else:

            st.error(
            "Wrong Details ❌"
            )
            # ================= FOOD MENU =================

elif option=="Food Menu":

    st.header("🍕 Food Menu")


    with open("data/foods.json","r") as file:

        foods=json.load(file)


    cols=st.columns(3)


    for i,food in enumerate(foods):

        with cols[i%3]:

            image_path = (
                "images/"
                + food["name"].lower()
                + ".jpg"
            )


            st.image(
                image_path,
                use_container_width=True
            )


            st.subheader(
                food["name"]
            )


            st.write(
                "💰 ₹",
                food["price"]
            )


            st.write("⭐⭐⭐⭐⭐")



# ================= CART =================

elif option=="Cart":


    st.header("🛒 Add To Cart")


    with open("data/foods.json","r") as file:

        foods=json.load(file)


    for food in foods:


        st.subheader(food["name"])


        st.write(
            "💰 ₹",
            food["price"]
        )


        if st.button(
            "Add "+food["name"]
        ):


            st.session_state.cart.append(food)


            st.success(
                food["name"]
                +" Added ✅"
            )



# ================= VIEW CART =================

elif option=="View Cart":


    st.header("🧾 Your Cart")


    if len(st.session_state.cart)==0:


        st.warning(
            "Cart Empty"
        )


    else:


        total=0


        for item in st.session_state.cart:


            st.write(
                item["name"],
                "- ₹",
                item["price"]
            )


            total+=item["price"]


        st.subheader(
            "Total Bill = ₹ "
            +str(total)
        )



# ================= PLACE ORDER =================

elif option=="Place Order":


    st.header("🚚 Place Order")


    if len(st.session_state.cart)==0:


        st.warning(
            "Cart Empty"
        )


    else:


        total=0


        for item in st.session_state.cart:

            total+=item["price"]


        st.subheader(
            "Total Amount ₹ "
            +str(total)
        )


        if st.button("Confirm Order"):


            order={
                "items":st.session_state.cart,
                "total":total
            }


            with open("data/orders.json","r") as file:

                orders=json.load(file)


            orders.append(order)


            with open("data/orders.json","w") as file:

                json.dump(
                    orders,
                    file,
                    indent=4
                )


            st.session_state.cart=[]


            st.success(
                "Order Placed Successfully 🚚"
            )



# ================= ADMIN PANEL =================

elif option=="Admin":


    st.header("👨‍💻 Admin Panel")


    admin_choice=st.selectbox(
        "Choose Admin Option",
        [
            "View Orders",
            "Add Food",
            "Delete Food"
        ]
    )


    # VIEW ORDERS

    if admin_choice=="View Orders":


        st.subheader("📋 Orders")


        with open("data/orders.json","r") as file:

            orders=json.load(file)


        if len(orders)==0:


            st.warning(
                "No Orders"
            )


        for order in orders:


            st.write("----------------")


            for item in order["items"]:


                st.write(
                    item["name"],
                    "- ₹",
                    item["price"]
                )


            st.success(
                "Total ₹ "
                +str(order["total"])
            )



    # ADD FOOD

    elif admin_choice=="Add Food":


        st.subheader(
            "🍔 Add Food"
        )


        name=st.text_input(
            "Food Name"
        )


        price=st.number_input(
            "Price",
            min_value=1
        )


        if st.button(
            "Add Food"
        ):


            with open("data/foods.json","r") as file:

                foods=json.load(file)


            foods.append(
                {
                "id":len(foods)+1,
                "name":name,
                "price":price
                }
            )


            with open("data/foods.json","w") as file:

                json.dump(
                    foods,
                    file,
                    indent=4
                )


            st.success(
                "Food Added Successfully ✅"
            )



    # DELETE FOOD

    elif admin_choice=="Delete Food":


        st.subheader(
            "🗑️ Delete Food"
        )


        with open("data/foods.json","r") as file:

            foods=json.load(file)


        names=[
            food["name"]
            for food in foods
        ]


        selected=st.selectbox(
            "Select Food",
            names
        )


        if st.button("Delete"):


            foods=[
                food
                for food in foods
                if food["name"]!=selected
            ]


            with open("data/foods.json","w") as file:

                json.dump(
                    foods,
                    file,
                    indent=4
                )


            st.success(
                "Deleted Successfully ✅"
            )