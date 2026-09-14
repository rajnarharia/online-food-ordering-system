import streamlit as st
import uuid
from datetime import datetime
from utils.data_store import create_order, validate_coupon

def render_cart():
    st.markdown("<h1 class='section-title' style='margin-bottom: 32px;'>Your Cart</h1>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.markdown(
            """
            <div style='text-align: center; padding: 100px 0; max-width: 400px; margin: 0 auto;'>
                <div style='font-size: 64px; margin-bottom: 24px; color: #374151;'>🛒</div>
                <h3 class='card-title' style='color: #FFFFFF; font-size: 24px;'>Your cart is empty</h3>
                <p class='body-text' style='margin-bottom: 32px;'>Looks like you haven't added any premium dishes yet.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        _, c2, _ = st.columns([1, 1, 1])
        with c2:
            if st.button("Explore Menu", type="primary", use_container_width=True):
                st.session_state.current_view = "Menu"
                st.rerun()
        return

    left_col, right_col = st.columns([2, 1], gap="large")
    
    with left_col:
        st.markdown("<h3 class='card-title' style='font-size: 20px; margin-bottom: 24px;'>Order Items</h3>", unsafe_allow_html=True)
                
        for i, item in enumerate(st.session_state.cart):
            with st.container():
                c1, c2, c3 = st.columns([1.5, 3, 1.5])
                with c1:
                    st.markdown(f"<img src='{item.get('image_url', '')}' style='width: 100%; height: 80px; border-radius: 12px; object-fit: cover;' />", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<p class='card-title' style='margin: 0; font-size: 18px;'>{item['name']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='small-text' style='margin: 4px 0 0 0;'>₹{item['price']} x {item['quantity']} = ₹{item['price'] * item['quantity']}</p>", unsafe_allow_html=True)
                with c3:
                    q1, q2, q3 = st.columns([1, 1, 1])
                    with q1: 
                        if st.button("-", key=f"sub_{i}", use_container_width=True):
                            if item['quantity'] > 1:
                                st.session_state.cart[i]['quantity'] -= 1
                            else:
                                st.session_state.cart.pop(i)
                            st.rerun()
                    with q2: 
                        st.markdown(f"<p style='text-align: center; margin-top: 10px; font-weight: 600;'>{item['quantity']}</p>", unsafe_allow_html=True)
                    with q3: 
                        if st.button("+", key=f"add_{i}", use_container_width=True):
                            st.session_state.cart[i]['quantity'] += 1
                            st.rerun()
                        
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<h3 class='card-title' style='font-size: 20px; margin-bottom: 16px;'>Delivery Details</h3>", unsafe_allow_html=True)
        address = st.text_area("Delivery Address", placeholder="Enter your full address here...")
        notes = st.text_area("Delivery Instructions", placeholder="e.g. Please ring the doorbell...")
        payment = st.selectbox("Payment Method", ["Cash on Delivery", "Demo Online Payment"])
        
    with right_col:
        with st.container():
            st.markdown("<h3 class='card-title' style='font-size: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 16px; margin-bottom: 16px;'>Order Summary</h3>", unsafe_allow_html=True)
            
            subtotal = sum([item['price'] * item['quantity'] for item in st.session_state.cart])
            tax = subtotal * 0.05
            delivery = 50.0 if subtotal < 500 else 0.0
            
            coupon = st.text_input("Coupon Code", placeholder="e.g. SAAS10")
            discount = 0
            
            if coupon:
                is_valid, result = validate_coupon(coupon, subtotal)
                if is_valid:
                    discount = result['discount']
                    st.success(f"Coupon Applied: ₹{discount:.2f} off!")
                else:
                    st.error(result)
            
            total = subtotal + tax + delivery - discount
            
            st.write("<br>", unsafe_allow_html=True)
            
            st.markdown(f"<div style='display: flex; justify-content: space-between; margin-bottom: 12px;'><span class='body-text'>Subtotal</span><span class='body-text' style='color: #FFF; font-weight: 500;'>₹{subtotal:.2f}</span></div>", unsafe_allow_html=True)
            if discount > 0:
                st.markdown(f"<div style='display: flex; justify-content: space-between; margin-bottom: 12px;'><span class='body-text' style='color: #22C55E;'>Discount</span><span class='body-text' style='color: #22C55E; font-weight: 500;'>-₹{discount:.2f}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='display: flex; justify-content: space-between; margin-bottom: 12px;'><span class='body-text'>Taxes</span><span class='body-text' style='color: #FFF; font-weight: 500;'>₹{tax:.2f}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='display: flex; justify-content: space-between; margin-bottom: 16px;'><span class='body-text'>Delivery</span><span class='body-text' style='color: #FFF; font-weight: 500;'>₹{delivery:.2f}</span></div>", unsafe_allow_html=True)
            
            st.markdown("<div style='border-top: 1px solid rgba(255,255,255,0.1); margin: 16px 0;'></div>", unsafe_allow_html=True)
            
            st.markdown(f"<div style='display: flex; justify-content: space-between; margin-bottom: 24px;'><span style='font-size: 20px; font-weight: 700; color: #FFF;'>Total</span><span style='font-size: 24px; font-weight: 700; color: #FFF;'>₹{total:.2f}</span></div>", unsafe_allow_html=True)
            
            if st.button("Proceed to Checkout", type="primary", use_container_width=True):
                user = st.session_state.user
                if not user:
                    st.error("Please log in to place an order.")
                    return
                    
                if not address:
                    st.error("Please provide a delivery address.")
                    return
                
                order_id = f"ORD-{str(uuid.uuid4())[:6].upper()}"
                
                # Insert order to DB
                create_order(
                    user_id=user['id'],
                    order_id=order_id,
                    items=st.session_state.cart,
                    subtotal=round(subtotal, 2),
                    tax=round(tax, 2),
                    delivery_fee=round(delivery, 2),
                    discount=round(discount, 2),
                    total=round(total, 2),
                    address=f"{address} | Notes: {notes}",
                    payment_method=payment
                )
                    
                st.success("Order placed successfully!")
                st.session_state.cart = []
                st.session_state.current_view = "Profile"
                st.rerun()
