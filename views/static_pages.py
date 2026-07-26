import streamlit as st

def render_about():
    # Hero for About
    st.markdown(
        """
        <div style='text-align: center; padding: 40px 0;'>
            <h1 class='hero-title' style='font-size: 56px; margin-bottom: 16px;'>Redefining Food Delivery.</h1>
            <p class='body-text' style='max-width: 600px; margin: 0 auto; font-size: 18px;'>We connect you with the best local restaurants, offering a seamless, premium, and lightning-fast delivery experience.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.write("<br><br>", unsafe_allow_html=True)
    
    # Mission and Vision Grid
    c1, c2 = st.columns(2, gap="large")
    with c1:
        with st.container(border=True):
            st.markdown("<h3 class='card-title' style='color: #FF5A5F;'>Our Mission</h3>", unsafe_allow_html=True)
            st.markdown("<p class='body-text'>To elevate the standard of online food delivery by providing a world-class platform that empowers both local chefs and hungry customers with transparency, speed, and quality.</p>", unsafe_allow_html=True)
    with c2:
        with st.container(border=True):
            st.markdown("<h3 class='card-title' style='color: #22C55E;'>Our Vision</h3>", unsafe_allow_html=True)
            st.markdown("<p class='body-text'>A world where accessing premium, hot, and delicious meals is as simple as a single tap, backed by an intelligent and sustainable logistics network.</p>", unsafe_allow_html=True)

    st.write("<br><br><br>", unsafe_allow_html=True)
    
    # Values
    st.markdown("<h2 class='section-title' style='text-align: center;'>Our Values</h2>", unsafe_allow_html=True)
    v1, v2, v3 = st.columns(3)
    
    values = [
        {"icon": "⚡", "title": "Velocity", "desc": "We build fast and deliver faster. Speed is a feature."},
        {"icon": "🛡️", "title": "Trust", "desc": "Transparent pricing, real-time tracking, and verified reviews."},
        {"icon": "✨", "title": "Excellence", "desc": "We obsess over every pixel in our app and every ingredient in our boxes."}
    ]
    
    for i, col in enumerate([v1, v2, v3]):
        with col:
            st.markdown(
                f"""
                <div style='text-align: center; padding: 24px;'>
                    <div style='font-size: 40px; margin-bottom: 16px;'>{values[i]['icon']}</div>
                    <h3 class='card-title' style='font-size: 20px;'>{values[i]['title']}</h3>
                    <p class='body-text' style='font-size: 14px;'>{values[i]['desc']}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
    st.write("<br><br>", unsafe_allow_html=True)
    
    # Contact & FAQ layout
    c3, c4 = st.columns([1, 1], gap="large")
    
    with c3:
        st.markdown("<h3 class='card-title'>Get in Touch</h3>", unsafe_allow_html=True)
        st.markdown("<p class='body-text'>Have questions or need support? Our team is available 24/7.</p>", unsafe_allow_html=True)
        st.text_input("Name", placeholder="Jane Doe")
        st.text_input("Email", placeholder="jane@example.com")
        st.text_area("Message", placeholder="How can we help?")
        if st.button("Send Message", type="primary"):
            import json
            import os
            from datetime import datetime
            
            try:
                if not os.path.exists("data/messages.json"):
                    with open("data/messages.json", "w") as f:
                        json.dump([], f)
                with open("data/messages.json", "r") as f:
                    msgs = json.load(f)
            except Exception:
                msgs = []
                
            msgs.append({"date": datetime.now().isoformat()})
            try:
                with open("data/messages.json", "w") as f:
                    json.dump(msgs, f, indent=4)
            except Exception:
                pass
                
            st.toast("Message sent successfully!", icon="✅")
            
    with c4:
        st.markdown("<h3 class='card-title'>Frequently Asked Questions</h3>", unsafe_allow_html=True)
        with st.expander("What are your delivery hours?", expanded=True):
            st.write("We deliver 24/7 in supported metropolitan areas. Check the app for local restaurant availability.")
        with st.expander("How does the AI Assistant work?"):
            st.write("Our AI analyzes your taste preferences and dietary requirements to suggest the perfect meal.")
        with st.expander("Do you offer corporate plans?"):
            st.write("Yes! We offer bulk ordering and corporate accounts. Contact our sales team for details.")
            
    st.write("<br><br>", unsafe_allow_html=True)
    
    # Map (Placeholder)
    st.markdown("<h3 class='card-title'>Headquarters</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='width: 100%; height: 300px; background: rgba(255,255,255,0.02); border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center; flex-direction: column;'>
            <span style='font-size: 32px;'>🗺️</span>
            <span style='color: #9CA3AF; margin-top: 12px; font-weight: 500;'>Silicon Valley, CA</span>
        </div>
        """, 
        unsafe_allow_html=True
    )
