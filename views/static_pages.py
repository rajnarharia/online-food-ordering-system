import streamlit as st

def render_about():
    st.markdown("<div class='element-container'>", unsafe_allow_html=True)
    
    st.write("<br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; max-width: 800px; margin: 0 auto 64px auto;">
            <h1 style="font-size: 48px; font-weight: 700; margin-bottom: 24px; letter-spacing: -2px;">Quality food.<br>Zero friction.</h1>
            <p style="color: #9CA3AF; font-size: 18px; line-height: 1.6;">
                We build infrastructure that connects premium culinary experiences with modern logistics.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("<h3 style='font-weight: 600; margin-bottom: 16px;'>Our Mission</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #9CA3AF; line-height: 1.6;'>To elevate the standard of food delivery by focusing on uncompromising quality, seamless user experience, and robust logistics infrastructure.</p>", unsafe_allow_html=True)
    with c2:
        st.markdown("<h3 style='font-weight: 600; margin-bottom: 16px;'>Contact</h3>", unsafe_allow_html=True)
        st.markdown(
            """
            <p style='color: #9CA3AF; line-height: 1.6;'>
                <strong>HQ</strong><br>
                San Francisco, CA<br>
                contact@foodie.com
            </p>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)
