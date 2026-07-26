import streamlit as st
import json
import time
from datetime import datetime, timedelta

def render_cart():
    st.markdown("<h2 class='hero-title' style='font-size: 2.5rem; margin-bottom: 24px;'>Checkout</h2>", unsafe_allow_html=True)
    
    cart = st.session_state.cart
    
    if not cart:
        st.markdown(
            """
            <div style="text-align: center; padding: 4rem 0;">
                <svg width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="currentColor" style="opacity: 0.1;" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                    <line x1="3" y1="6" x2="21" y2="6"></line>
                    <path d="M16 10a4 4 0 0 1-8 0"></path>
                </svg>
                <h3 class='card-title' style='margin-top: 1.5rem; font-size: 1.5rem;'>Your cart is empty</h3>
                <p class="card-meta">Explore our menu and add some delicious items.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        return

    c1, c2 = st.columns([5, 3], gap="large")
    
    with c1:
        st.markdown("<p class='card-title' style='margin-bottom: 16px;'>Order Items</p>", unsafe_allow_html=True)
        
        cart_counts = {}
        for item in cart:
            cart_counts[item['id']] = cart_counts.get(item['id'], 0) + 1
            
        unique_items = {item['id']: item for item in cart}
        
        for item_id, count in cart_counts.items():
            item = unique_items[item_id]
            with st.container(border=True):
                ic1, ic2 = st.columns([4, 1])
                with ic1:
                    st.markdown(f"<p class='card-title' style='margin: 0;'>{item['name']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<span class='card-meta'>₹{item['price']} × {count}</span>", unsafe_allow_html=True)
                with ic2:
                    if st.button("Remove", key=f"remove_{item_id}"):
                        for i, c_item in enumerate(st.session_state.cart):
                            if c_item['id'] == item_id:
                                st.session_state.cart.pop(i)
                                st.rerun()
                                break
                                
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<p class='card-title' style='margin-bottom: 16px;'>Delivery Details</p>", unsafe_allow_html=True)
        st.text_input("Full Address", placeholder="Enter your delivery address")
        st.text_input("Payment details", placeholder="Card ending in 4242")
            
    with c2:
        with st.container(border=True):
            st.markdown("<p class='card-title'>Summary</p>", unsafe_allow_html=True)
            st.divider()
            
            subtotal = sum(item['price'] for item in cart)
            tax = round(subtotal * 0.05, 2)
            delivery = 50 if subtotal < 500 else 0
            
            coupon = st.text_input("Promo Code", placeholder="E.g. STARTUP20", label_visibility="collapsed")
            discount = round(subtotal * 0.20, 2) if coupon.upper() == "STARTUP20" else 0
            if discount > 0:
                st.success("20% Discount applied!", icon="✅")
                
            total = subtotal + tax + delivery - discount
            
            st.write("<br>", unsafe_allow_html=True)
            sc1, sc2 = st.columns(2)
            sc1.markdown("<span class='card-meta'>Subtotal</span>", unsafe_allow_html=True)
            sc2.markdown(f"<span class='card-meta' style='float: right; font-weight: 700;'>₹{subtotal}</span>", unsafe_allow_html=True)
            
            sc1, sc2 = st.columns(2)
            sc1.markdown("<span class='card-meta'>Tax</span>", unsafe_allow_html=True)
            sc2.markdown(f"<span class='card-meta' style='float: right; font-weight: 700;'>₹{tax}</span>", unsafe_allow_html=True)
            
            sc1, sc2 = st.columns(2)
            sc1.markdown("<span class='card-meta'>Delivery</span>", unsafe_allow_html=True)
            sc2.markdown(f"<span class='card-meta' style='float: right; font-weight: 700;'>{'₹'+str(delivery) if delivery > 0 else 'Free'}</span>", unsafe_allow_html=True)
            
            if discount > 0:
                sc1, sc2 = st.columns(2)
                sc1.markdown("<span style='color: #10B981; font-weight: 600; font-size: 0.85rem;'>Discount</span>", unsafe_allow_html=True)
                sc2.markdown(f"<span style='float: right; font-weight: 700; color: #10B981; font-size: 0.85rem;'>-₹{discount}</span>", unsafe_allow_html=True)
            
            st.divider()
            
            tc1, tc2 = st.columns(2)
            tc1.markdown("<p class='price-tag' style='font-size: 1.2rem;'>Total</p>", unsafe_allow_html=True)
            tc2.markdown(f"<p class='price-tag' style='font-size: 1.5rem; float: right;'>₹{total}</p>", unsafe_allow_html=True)
            
            st.write("<br>", unsafe_allow_html=True)
            
            if st.button("Complete Order", use_container_width=True, type="primary"):
                # Micro-interaction: Progress bar + success state
                progress_text = "Processing payment securely..."
                my_bar = st.progress(0, text=progress_text)
                
                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                
                my_bar.empty()
                st.balloons()
                st.success("Order Placed Successfully! Your food is being prepared.", icon="🎉")
                
                time.sleep(1.5)
                
                order = {
                    "id": f"ORD-{int(time.time())}",
                    "date": datetime.now().isoformat(),
                    "items": cart,
                    "total": total,
                    "status": "Processing"
                }
                
                try:
                    with open("data/orders.json", "r") as file:
                        orders = json.load(file)
                except:
                    orders = []
                    
                orders.append(order)
                with open("data/orders.json", "w") as file:
                    json.dump(orders, file, indent=4)
                    
                st.session_state.cart = []
                st.session_state.current_view = "Profile"
                st.rerun() 
