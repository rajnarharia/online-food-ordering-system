import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from utils.data_store import get_all_orders, update_order_status, get_foods, add_food, toggle_food_active
from utils.csv_handler import load_csv, save_csv, get_filepath

def render_admin():
    user = st.session_state.user
    if not user or user.get("role") != "admin":
        st.error("Unauthorized")
        return
        
    tabs = st.tabs(["Dashboard", "Manage Orders", "Manage Menu", "Data Management"])
    
    with tabs[0]:
        render_dashboard_tab()
        
    with tabs[1]:
        render_manage_orders_tab()
        
    with tabs[2]:
        render_manage_menu_tab()
        
    with tabs[3]:
        render_data_management_tab()

def render_dashboard_tab():
    head_col, action_col = st.columns([3, 1])
    with head_col:
        st.markdown("<h1 class='section-title' style='margin: 0;'>Analytics Dashboard</h1>", unsafe_allow_html=True)
    
    orders = get_all_orders()
    
    with action_col:
        date_filter = st.selectbox("Filter", ["All Time", "Last 7 Days", "Last 30 Days", "Last 90 Days"], label_visibility="collapsed")
        
        now = datetime.now()
        filtered_orders = []
        for o in orders:
            try:
                dt = datetime.fromisoformat(o['date'])
                if date_filter == "Last 7 Days" and now - dt > timedelta(days=7): continue
                if date_filter == "Last 30 Days" and now - dt > timedelta(days=30): continue
                if date_filter == "Last 90 Days" and now - dt > timedelta(days=90): continue
                filtered_orders.append(o)
            except:
                filtered_orders.append(o)
                
    total_rev = sum(pd.to_numeric(o.get("total", 0), errors='coerce') for o in filtered_orders)
    active_orders = len([o for o in filtered_orders if o.get("status") not in ["Delivered", "Cancelled"]])
    total_orders_count = len(filtered_orders)
    avg_order = (total_rev / total_orders_count) if total_orders_count > 0 else 0
    
    cols = st.columns(4)
    metrics = [
        {"label": "Total Revenue", "value": f"₹{total_rev:,.2f}"},
        {"label": "Active Orders", "value": f"{active_orders}"},
        {"label": "Total Orders", "value": f"{total_orders_count:,}"},
        {"label": "Avg Order Value", "value": f"₹{avg_order:.2f}"}
    ]
    
    for i, metric in enumerate(metrics):
        with cols[i]:
            with st.container():
                st.markdown(f"<p class='small-text' style='margin: 0 0 8px 0; font-weight: 500;'>{metric['label']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 28px; font-weight: 700; color: #FFF; margin: 0 0 8px 0;'>{metric['value']}</p>", unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1], gap="large")
    
    with c1:
        st.markdown("<h3 class='card-title' style='font-size: 18px; margin-bottom: 24px;'>Revenue Overview</h3>", unsafe_allow_html=True)
        if filtered_orders:
            df = pd.DataFrame(filtered_orders)
            df['date'] = pd.to_datetime(df['date']).dt.date
            df['total'] = pd.to_numeric(df['total'], errors='coerce')
            revenue_by_date = df.groupby('date')['total'].sum().reset_index()
            st.bar_chart(revenue_by_date.set_index('date'), use_container_width=True)
        else:
            st.info("No orders in this period.")
            
    with c2:
        st.markdown("<h3 class='card-title' style='font-size: 18px; margin-bottom: 24px;'>Order Status</h3>", unsafe_allow_html=True)
        if filtered_orders:
            df = pd.DataFrame(filtered_orders)
            status_counts = df['status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            st.dataframe(status_counts, use_container_width=True)
        else:
            st.info("No orders in this period.")
            
def render_manage_orders_tab():
    st.markdown("<h3 class='card-title'>Manage Active Orders</h3>", unsafe_allow_html=True)
    orders = get_all_orders()
    active_orders = [o for o in orders if o.get("status") not in ["Delivered", "Cancelled"]]
    
    if not active_orders:
        st.info("No active orders.")
        return
        
    for order in active_orders:
        with st.container():
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1:
                st.write(f"**{order.get('order_id', order.get('id', ''))}** - ₹{order.get('total', 0)}")
                try:
                    dt = datetime.fromisoformat(order['date'])
                    st.write(dt.strftime("%Y-%m-%d %H:%M"))
                except:
                    st.write(order.get('date', ''))
            with c2:
                new_status = st.selectbox("Status", ["Order Placed", "Confirmed", "Preparing", "Out for Delivery", "Delivered", "Cancelled"], 
                                          index=["Order Placed", "Confirmed", "Preparing", "Out for Delivery", "Delivered", "Cancelled"].index(order.get('status', 'Order Placed')),
                                          key=f"status_{order.get('order_id')}")
            with c3:
                if st.button("Update", key=f"btn_{order.get('order_id')}", use_container_width=True):
                    update_order_status(order.get('order_id'), new_status)
                    st.success("Updated")
                    st.rerun()

def render_manage_menu_tab():
    st.markdown("<h3 class='card-title'>Manage Menu</h3>", unsafe_allow_html=True)
    
    with st.expander("➕ Add New Food"):
        with st.form("add_food_form"):
            name = st.text_input("Name")
            price = st.number_input("Price (₹)", min_value=0.0, step=10.0)
            category = st.text_input("Category")
            is_veg = st.checkbox("Vegetarian")
            desc = st.text_area("Description")
            cal = st.number_input("Calories", min_value=0)
            img = st.text_input("Image URL")
            
            if st.form_submit_button("Add Food"):
                if name and price:
                    add_food({
                        'name': name, 'price': price, 'category': category, 'is_veg': is_veg, 
                        'description': desc, 'calories': cal, 'image_url': img, 'is_active': True,
                        'rating': 4.5, 'reviews': 0, 'popularity': 50
                    })
                    st.success("Food added successfully!")
                    st.rerun()
                else:
                    st.error("Name and price are required.")
                    
    st.write("<br>", unsafe_allow_html=True)
    
    foods = get_foods()
    for food in foods:
        with st.container():
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.write(f"**{food['name']}** - ₹{food['price']}")
                st.write(f"*{food['category']}*")
            with c2:
                status = "Active" if food.get('is_active', True) else "Inactive"
                st.write(f"Status: **{status}**")
            with c3:
                is_active_bool = str(food.get('is_active', True)).lower() in ['true', '1']
                action = "Deactivate" if is_active_bool else "Activate"
                if st.button(action, key=f"toggle_{food['id']}", use_container_width=True):
                    toggle_food_active(food['id'], not is_active_bool)
                    st.rerun()

def render_data_management_tab():
    st.markdown("<h3 class='card-title'>CSV Data Management</h3>", unsafe_allow_html=True)
    st.write("Manage the backend CSV files here. Uploading a CSV will safely replace the existing database.")
    
    csv_files = ["foods.csv", "users.csv", "orders.csv", "order_items.csv", "coupons.csv"]
    
    selected_csv = st.selectbox("Select CSV File", csv_files)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label=f"Download {selected_csv}",
            data=open(get_filepath(selected_csv), 'rb').read(),
            file_name=selected_csv,
            mime='text/csv'
        )
        
    st.write("<br>", unsafe_allow_html=True)
    st.markdown("<p class='body-text'>Upload Replacement CSV</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'], key=f"upload_{selected_csv}")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("Preview:")
            st.dataframe(df.head())
            
            if st.button("Replace Data Safely"):
                # Basic validation
                current_df = load_csv(selected_csv)
                missing_cols = set(current_df.columns) - set(df.columns)
                if missing_cols:
                    st.error(f"Validation Failed! Missing required columns: {missing_cols}")
                else:
                    save_csv(selected_csv, df)
                    st.success(f"Successfully replaced {selected_csv}!")
                    st.rerun()
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
