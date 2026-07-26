import streamlit as st
import json
from datetime import datetime

def render_cart():
    st.markdown("<h1 class='section-title' style='margin-bottom: 32px;'>Your Cart</h1>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        # Beautiful Empty State
        st.markdown(
            """
            <div style='text-align: center; padding: 100px 0; max-width: 400px; margin: 0 auto;'>
                <div style='font-size: 64px; margin-bottom: 24px; color: #374151;'>🛒</div>
                <h3 class='card-title' style='color: #FFFFFF; font-size: 24px;'>Your cart is empty</h3>
                <p class='body-text' style='margin-bottom: 32px;'>Looks like you haven't added any premium dishes yet. Explore our menu to find your next favorite meal.</p>
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

    # Split Layout
    left_col, right_col = st.columns([2, 1], gap="large")
    
    with left_col:
        st.markdown("<h3 class='card-title' style='font-size: 20px; margin-bottom: 24px;'>Order Items</h3>", unsafe_allow_html=True)
        
        # Group identical items
        cart_counts = {}
        for item in st.session_state.cart:
            _id = item['id']
            if _id in cart_counts:
                cart_counts[_id]['count'] += 1
            else:
                cart_counts[_id] = {'item': item, 'count': 1}
                
        for _id, data in cart_counts.items():
            item = data['item']
            count = data['count']
            
            with st.container(border=True):
                c1, c2, c3 = st.columns([1.5, 3, 1.5], vertical_alignment="center")
                with c1:
                    st.markdown(f"<img src='{item.get('image_url', '')}' style='width: 100%; height: 80px; border-radius: 12px;' />", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<p class='card-title' style='margin: 0; font-size: 18px;'>{item['name']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='small-text' style='margin: 4px 0 0 0;'>${item['price']}</p>", unsafe_allow_html=True)
                with c3:
                    # Functional quantity stepper
                    q1, q2, q3 = st.columns([1, 1, 1])
                    with q1: 
                        if st.button("-", key=f"sub_{_id}", help="Remove one"):
                            for i, cart_item in enumerate(st.session_state.cart):
                                if cart_item['id'] == _id:
                                    st.session_state.cart.pop(i)
                                    break
                            st.rerun()
                    with q2: 
                        st.markdown(f"<p style='text-align: center; margin-top: 10px; font-weight: 600;'>{count}</p>", unsafe_allow_html=True)
                    with q3: 
                        if st.button("+", key=f"add_{_id}", help="Add one"):
                            st.session_state.cart.append(item)
                            st.rerun()
                        
        st.write("<br>", unsafe_allow_html=True)
        # Order Notes
        st.text_area("Add delivery notes or allergy instructions", placeholder="e.g. Please ring the doorbell...")
        
    with right_col:
        # Sticky Summary Logic Wrapper
        st.markdown("<div style='position: sticky; top: 100px;'>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("<h3 class='card-title' style='font-size: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 16px; margin-bottom: 16px;'>Order Summary</h3>", unsafe_allow_html=True)
            
            subtotal = sum([float(item['price']) for item in st.session_state.cart])
            tax = subtotal * 0.08
            delivery = 2.99 if subtotal < 50 else 0.00
            total = subtotal + tax + delivery
            
            # Coupon Feature
            coupon = st.text_input("Coupon Code", placeholder="e.g. SAAS10")
            discount = 0
            if coupon == "SAAS10":
                discount = subtotal * 0.10
                st.markdown("<p style='color: #22C55E; font-size: 12px; font-weight: 600; margin-top: -12px;'>Valid: 10% Off Applied!</p>", unsafe_allow_html=True)
                total -= discount
            
            st.write("<br>", unsafe_allow_html=True)
            
            # Pricing breakdown
            st.markdown(f"<div style='display: flex; justify-content: space-between; margin-bottom: 12px;'><span class='body-text'>Subtotal</span><span class='body-text' style='color: #FFF; font-weight: 500;'>${subtotal:.2f}</span></div>", unsafe_allow_html=True)
            if discount > 0:
                st.markdown(f"<div style='display: flex; justify-content: space-between; margin-bottom: 12px;'><span class='body-text' style='color: #22C55E;'>Discount</span><span class='body-text' style='color: #22C55E; font-weight: 500;'>-${discount:.2f}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='display: flex; justify-content: space-between; margin-bottom: 12px;'><span class='body-text'>Taxes</span><span class='body-text' style='color: #FFF; font-weight: 500;'>${tax:.2f}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='display: flex; justify-content: space-between; margin-bottom: 16px;'><span class='body-text'>Delivery</span><span class='body-text' style='color: #FFF; font-weight: 500;'>${delivery:.2f}</span></div>", unsafe_allow_html=True)
            
            st.markdown("<div style='border-top: 1px solid rgba(255,255,255,0.1); margin: 16px 0;'></div>", unsafe_allow_html=True)
            
            st.markdown(f"<div style='display: flex; justify-content: space-between; margin-bottom: 24px;'><span style='font-size: 20px; font-weight: 700; color: #FFF;'>Total</span><span style='font-size: 24px; font-weight: 700; color: #FFF;'>${total:.2f}</span></div>", unsafe_allow_html=True)
            
            if st.button("Proceed to Checkout", type="primary"):
                # Real Checkout Logic
                try:
                    with open("data/orders.json", "r") as f:
                        orders_db = json.load(f)
                except Exception:
                    orders_db = []
                
                import uuid
                new_order = {
                    "id": f"ORD-{str(uuid.uuid4())[:6].upper()}",
                    "date": datetime.now().isoformat(),
                    "items": [{"id": item["id"], "name": item["name"], "price": item["price"]} for item in st.session_state.cart],
                    "subtotal": round(subtotal, 2),
                    "tax": round(tax, 2),
                    "delivery_fee": round(delivery, 2),
                    "discount": round(discount, 2),
                    "total": round(total, 2),
                    "status": "Preparing",
                    "delivery_progress": 10,
                    "estimated_delivery": "30 mins"
                }
                
                orders_db.append(new_order)
                
                with open("data/orders.json", "w") as f:
                    json.dump(orders_db, f, indent=4)
                    
                st.toast("Order placed successfully!", icon="✅")
                st.session_state.cart = [] # Clear cart
                st.session_state.current_view = "Profile" # Redirect to see the new order
                st.rerun()
                
        st.markdown("</div>", unsafe_allow_html=True)
