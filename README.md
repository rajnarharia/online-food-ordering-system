# 🍔 Online Food Ordering System
## A Modern Streamlit-Based Food Ordering Platform

A modern and interactive Online Food Ordering System built using Python and Streamlit. The application provides a complete digital food-ordering experience with food discovery, search and filtering, wishlist management, cart and checkout, order management, user authentication, smart food recommendations, and an administrative dashboard.

The project is designed as an educational and portfolio application demonstrating practical Python, Streamlit, Pandas, data management, authentication, and interactive dashboard development.

## 🚀 Live Application
**🌐 Live Demo:**
[https://online-food-ordering-system-unafxmpes6og4jmcscj4br.streamlit.app/](https://online-food-ordering-system-unafxmpes6og4jmcscj4br.streamlit.app/)

## 📌 Project Overview
The Online Food Ordering System allows users to browse available food items, search and filter the menu, add items to their wishlist and cart, place orders, view order history, and receive order-status updates.

The application also includes a smart food recommendation feature that analyzes available food data and user preferences to provide relevant recommendations.

An administrative dashboard provides order management and business analytics.

The project uses a CSV-based backend with Pandas to keep the application lightweight, portable, and easy to run without requiring a database server.

## ✨ Features

### 👤 User Authentication
- User registration
- User login
- User logout
- Session-based authentication
- Customer and Admin roles
- User-specific profile information
- Secure password handling

### 🍕 Food Menu
Users can browse the available food catalog with:
- Food images
- Food name
- Category
- Price
- Rating
- Reviews
- Preparation time
- Calories
- Nutritional information
- Vegetarian / Non-Vegetarian information
- Availability
- Discounts
- Food descriptions

### 🔍 Smart Food Search & Filtering
The menu supports:
- Search by food name
- Search by category
- Vegetarian filter
- Non-Vegetarian filter
- Category filtering
- Price-based filtering
- Rating-based filtering
- Sorting by price
- Sorting by rating
- Sorting by popularity

### ❤️ Wishlist
Users can:
- Add food items to wishlist
- Remove items from wishlist
- View their wishlist
- Add wishlist items to cart
- Maintain a user-specific wishlist

Wishlist information is stored using the CSV-based data layer.

### 🛒 Shopping Cart
The cart provides:
- Add food items
- Remove food items
- Increase quantity
- Decrease quantity
- Item subtotal
- Order subtotal
- Tax calculation
- Delivery fee
- Coupon discount
- Final payable amount
- Clear cart
- Delivery instructions

Cart information is maintained using Streamlit session state until checkout.

### 🎟️ Coupon System
The application supports coupon-based discounts.
Coupons can include:
- Coupon code
- Discount percentage
- Minimum order amount
- Maximum discount
- Expiry date
- Active/inactive status

Coupon validation is performed before applying a discount to an order.

### 🧾 Checkout & Orders
The checkout workflow includes:
- Cart review
- Quantity confirmation
- Delivery address
- Delivery instructions
- Coupon validation
- Payment method selection
- Order confirmation
- Order creation
- Cart clearing
- Order history update

Each order contains relevant information such as:
- Order ID
- User
- Date
- Ordered items
- Quantity
- Subtotal
- Tax
- Delivery fee
- Discount
- Total
- Payment method
- Order status

### 📦 Order Status Tracking
The system supports an order lifecycle:
Order Placed → Confirmed → Preparing → Out for Delivery → Delivered

Orders can also be marked as:
Cancelled

Customers can view their order status from their order history/profile.
*This project implements order-status tracking. It does not provide real-time GPS delivery tracking.*

### 🔔 Notifications
The application supports user notifications related to order activity, such as:
- Order placed
- Order confirmed
- Order preparing
- Out for delivery
- Order delivered
- Order cancelled

Notifications can be associated with the corresponding user and order activity.

### 🤖 Smart Food Recommendation Engine
The application includes a Smart Food Recommendation Engine.
The recommendation system uses available food information and user preferences to identify relevant food choices.
It can consider factors such as:
- Vegetarian preference
- Non-vegetarian preference
- Food category
- Rating
- Popularity
- Price
- Calories
- Protein
- Food name/category matching
- Wishlist
- Previous user activity where available

The recommendation logic is rule-based/scoring-based.
*Important: This project does not claim to use a trained Machine Learning model or external LLM unless such a model/API is explicitly configured.*

### 📊 Admin Dashboard
Authorized administrators can access the administrative dashboard.
The dashboard provides business-level information such as:
- Total revenue
- Total orders
- Active orders
- Delivered orders
- Cancelled orders
- Total customers
- Average order value
- Today's orders
- Today's revenue

### 📈 Analytics
The dashboard provides data-driven analytics using actual application records.
Available analytics may include:
- Revenue trends
- Order trends
- Popular food items
- Category-wise performance
- Order-status distribution

Date filters can be used for analysing different periods, such as:
- Last 7 Days
- Last 30 Days
- Last 90 Days
- All Time

The application avoids presenting random/mock revenue analytics as actual business data.

### 🛠️ Admin Order Management
Administrators can manage customer orders and update order status through the available order-management interface.
Supported statuses include:
- Order Placed
- Confirmed
- Preparing
- Out for Delivery
- Delivered
- Cancelled

## 📂 CSV-Based Backend
This project intentionally does not require a database server.
The application uses:
**Python + Pandas + CSV + Streamlit**
for its data layer.

Typical CSV datasets include:
```
data/
├── foods.csv
├── users.csv
├── orders.csv
├── order_items.csv
├── wishlist.csv
├── addresses.csv
├── coupons.csv
└── notifications.csv
```
The exact files used by the application should match the current repository.

**Advantages of the CSV approach:**
- Easy to understand
- Easy to edit
- Portable
- No database server required
- Easy to backup
- Easy to inspect
- Suitable for educational/demo applications
- Simple deployment

*CSV storage is intended for this educational/demo project. A large-scale production system would normally require a dedicated persistent database.*

## 📤 CSV Data Management
Where enabled for administrators, the application can support CSV-based data management.
An administrator can work with CSV data through the application without requiring SQL.
Typical operations include:
- Upload CSV
- Validate CSV structure
- Preview data
- Update data
- Download/export CSV

CSV validation should ensure that required columns and data types are correct before replacing existing data.

## 💰 Currency
The application uses:
**₹ INR (Indian Rupees)**
for food prices, cart calculations, discounts, orders, and dashboard values.

## 🧱 Technology Stack
| Category | Technology |
| --- | --- |
| Programming Language | Python |
| Web Framework | Streamlit |
| Data Processing | Pandas |
| Numerical Processing | NumPy |
| Frontend/UI | Streamlit + HTML/CSS |
| Data Storage | CSV |
| Version Control | Git & GitHub |
| Deployment | Streamlit Cloud |

## 📁 Project Structure
The project follows a modular structure similar to:
```
online-food-ordering-system/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
│
├── components/
│   └── navbar.py
│
├── data/
│   ├── foods.csv
│   ├── users.csv
│   ├── orders.csv
│   ├── order_items.csv
│   ├── wishlist.csv
│   ├── addresses.csv
│   ├── coupons.csv
│   └── notifications.csv
│
├── views/
│   ├── auth.py
│   ├── home.py
│   ├── menu.py
│   ├── cart_checkout.py
│   ├── profile.py
│   ├── admin_dashboard.py
│   ├── ai_features.py
│   └── static_pages.py
│
├── utils/
│   ├── styles.py
│   └── csv_handler.py
│
└── images/
```
If the current repository contains additional or different files, keep the README structure consistent with the actual repository rather than inventing files.

## ⚙️ Installation & Setup

**1. Clone the Repository**
```bash
git clone https://github.com/rajnarharia/online-food-ordering-system.git
```

**2. Open the Project**
```bash
cd online-food-ordering-system
```

**3. Create a Virtual Environment**
Windows:
```bash
python -m venv .venv
```
Linux / macOS:
```bash
python3 -m venv .venv
```

**🔐 Activate Virtual Environment**
Windows PowerShell:
```powershell
.venv\Scripts\activate
```
Windows Command Prompt:
```cmd
.venv\Scripts\activate
```
Linux / macOS:
```bash
source .venv/bin/activate
```

**📦 Install Dependencies**
```bash
python -m pip install -r requirements.txt
```

**▶️ Run the Application**
```bash
python -m streamlit run app.py
```
The application will normally open at:
http://localhost:8501

## 👨‍💼 Application Workflow
**Customer Workflow**
Register / Login ↓ Home ↓ Browse Food ↓ Search / Filter ↓ Food Details ↓ Wishlist / Cart ↓ Checkout ↓ Place Order ↓ Order Tracking ↓ Order History

**Admin Workflow**
Admin Login ↓ Admin Dashboard ↓ Analytics ↓ Manage Orders ↓ Update Order Status ↓ Manage Food / CSV Data ↓ Review Business Data

## 🔐 Security & Data Handling
The application includes session-based authentication and role-based access.
Important security practices include:
- Passwords should not be stored as plain text.
- Admin functionality should be restricted to authorized users.
- Users should only access their own profile/order information.
- Uploaded CSV files should be validated before being accepted.
- Sensitive credentials should not be hardcoded into the public repository.

## 🧪 Testing Checklist
The application should be tested for:
- [x] Registration
- [x] Login
- [x] Logout
- [x] Menu browsing
- [x] Search
- [x] Food filters
- [x] Sorting
- [x] Wishlist
- [x] Cart
- [x] Quantity management
- [x] Coupon validation
- [x] Checkout
- [x] Order creation
- [x] Order history
- [x] Order status
- [x] Notifications
- [x] Smart recommendations
- [x] Admin authentication
- [x] Dashboard analytics
- [x] CSV data handling
- [x] CSV upload/validation where available

## 📌 Current Limitations
This is an educational/portfolio project and has some limitations.
- CSV storage is designed for small/demo-scale usage.
- Real-time GPS delivery tracking is not implemented.
- A real payment gateway is not connected unless explicitly configured.
- The recommendation engine is rule/scoring based rather than a trained ML model.
- Large-scale concurrent production usage would require a more robust backend architecture.

## 🚀 Future Scope
Possible future enhancements include:
- Real payment gateway integration
- Real-time GPS delivery tracking
- Restaurant/vendor dashboard
- Delivery partner module
- Advanced ML-based recommendation system
- Voice-based ordering
- Multilingual support
- Email/SMS notifications
- Advanced customer analytics
- Production-grade persistent data storage
- Cloud-based data management
- Advanced personalization

## 🎓 Educational Purpose
This project demonstrates practical implementation of:
- Python programming
- Streamlit web development
- Pandas data processing
- CSV-based data management
- User authentication
- Session management
- Shopping cart logic
- Order processing
- Recommendation logic
- Data visualization
- Dashboard development
- Modular software architecture

The project is intended for educational, internship, demonstration, and portfolio purposes.

## 🤝 Contributing
Contributions and improvements are welcome.
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Test the application
5. Commit your changes
6. Push the branch
7. Open a Pull Request

## 📄 License
This project is intended for educational and portfolio purposes.

## 👨‍💻 Developer
**Raj Narharia**
Artificial Intelligence Undergraduate | Python Developer | Machine Learning Enthusiast
GitHub: [https://github.com/rajnarharia](https://github.com/rajnarharia)

⭐ **Project**
If you find this project useful, consider giving the repository a ⭐.

Made with ❤️ using Python and Streamlit
