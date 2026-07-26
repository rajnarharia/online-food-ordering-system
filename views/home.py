import streamlit as st

def render_home():
    c1, c2 = st.columns([1.1, 1], gap="large")
    
    with c1:
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='hero-title'>Craving it? <br><span>Get it.</span></div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='hero-subtitle'>The fastest way to get your favorite meals delivered fresh and piping hot. Zero hassle, total satisfaction.</div>",
            unsafe_allow_html=True
        )
        
        b1, b2 = st.columns([1, 1])
        with b1:
            if st.button("Order Now", type="primary", use_container_width=True):
                st.session_state.current_view = "Menu"
                st.rerun()
        with b2:
            if st.button("Track Order", use_container_width=True):
                st.session_state.current_view = "Cart"
                st.rerun()
                
        st.write("<br><br>", unsafe_allow_html=True)
        
        m1, m2, m3 = st.columns(3)
        m1.markdown("<p class='stat-label'>Delivery Rating</p><p class='stat-value'>4.9<span style='color: #F59E0B; font-size: 1.5rem;'>★</span></p>", unsafe_allow_html=True)
        m2.markdown("<p class='stat-label'>Active Users</p><p class='stat-value'>50k<span style='color: #E23744; font-size: 1.5rem;'>+</span></p>", unsafe_allow_html=True)
        m3.markdown("<p class='stat-label'>Avg Time</p><p class='stat-value'>24<span style='color: #E23744; font-size: 1.5rem;'>m</span></p>", unsafe_allow_html=True)
        
    with c2:
        st.write("<br>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=1000", use_container_width=True)
        
        with st.container(border=True):
            sc1, sc2 = st.columns(2)
            sc1.markdown("<div style='text-align: center; font-weight: 700; color: #F59E0B;'>★ 4.9 Top Rated</div>", unsafe_allow_html=True)
            sc2.markdown("<div style='text-align: center; font-weight: 700; color: #10B981;'>🛵 Lightning Fast</div>", unsafe_allow_html=True)
