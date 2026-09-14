# Online Food Ordering System

A full-stack, comprehensive web application for online food ordering, built using Streamlit and Python. This project is designed as a robust internship/college presentation project featuring a complete user lifecycle, e-commerce functionalities, and a dynamic SQLite database backend.

## 🚀 Features

- **User Authentication**: Secure Login and Registration system with password hashing (SHA-256).
- **Role-Based Access**: Distinct `customer` and `admin` roles protecting sensitive routes.
- **Dynamic Food Menu**: Search, filter by dietary preferences (Veg/Non-Veg), and sort foods dynamically.
- **Cart & Checkout**: Persistent session-based cart with quantity controls, subtotal calculations, tax, delivery fee, and a fully functional coupon validation system (Try `SAAS10`).
- **Wishlist**: Add and remove favorite items, persisted across sessions.
- **Order Tracking**: Comprehensive order placement, history, and status tracking (Order Placed -> Confirmed -> Preparing -> Out for Delivery -> Delivered).
- **Smart Food Assistant**: A rule-based intelligent culinary companion recommending meals based on preferences, protein content, budget, and dietary restrictions.
- **Admin Dashboard**: Real-time business intelligence dashboard with actual revenue calculations, Pandas-driven charts, order management, and a Food Management panel (Add/Toggle active foods).
- **Responsive UI/UX**: World-class Vercel/Stripe-inspired aesthetic implemented purely in CSS/Streamlit layouts. Consistent currency formatting (₹).

## 🛠️ Technology Stack

- **Frontend**: Streamlit, Custom CSS, HTML Markdown Injection
- **Backend**: Python 3
- **Database**: SQLite3 (Local file-based SQL `foodie.db`)
- **Data Analysis**: Pandas, NumPy (for admin dashboard charts)

## 📁 Project Structure

```
.
├── app.py                     # Main Streamlit application entry point (Recommended)
├── main.py                    # Legacy CLI implementation wrapper
├── requirements.txt           # Python dependencies
├── database/
│   ├── db.py                  # SQLite database connection and helper functions
│   ├── schema.py              # SQLite table schemas definition
│   └── seed.py                # Initial database seeding script
├── components/
│   └── navbar.py              # Floating responsive navigation bar component
├── views/
│   ├── admin_dashboard.py     # Admin analytics and management panels
│   ├── ai_features.py         # Rule-based Smart Food Recommendation Assistant
│   ├── auth.py                # Login and Registration views
│   ├── cart_checkout.py       # Cart management and checkout processing
│   ├── home.py                # Dynamic landing page and trending items
│   ├── menu.py                # Searchable, filterable menu catalog
│   ├── profile.py             # User profile, wishlist, and order history
│   └── static_pages.py        # About us and Contact pages
└── utils/
    └── styles.py              # Global CSS definitions
```

## ⚙️ Installation & Setup

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repo-url>
   cd "online food ordering system"
   ```

2. **Create a Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize and Seed the Database**:
   ```bash
   python database/seed.py
   ```
   *This creates `foodie.db` and inserts sample foods, coupons, and an Admin user.*

5. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## 🔐 Demo Accounts

- **Admin Account**: 
  - Email: `admin@foodie.com`
  - Password: `admin123`
- **Customer Account**: 
  - Register a new account from the web UI to test the customer workflow.

## 🧠 Smart Recommendation Assistant Note

The "AI Assistant" in this project is implemented using an advanced **rule-based scoring engine** rather than a pre-trained ML/LLM model. It intelligently parses user input and scores actual database items based on dietary alignment, price constraints, protein requirements, and overall ratings to suggest the best matches locally.

## 🚀 Deployment (Streamlit Cloud)

The app is built to be strictly compatible with Streamlit Cloud:
- All file paths are relative to the project root.
- The database is initialized locally (Note: SQLite on Streamlit Cloud is ephemeral; it will reset on app reboot. For persistent production use, migrating `db.py` to PostgreSQL/Supabase is recommended).