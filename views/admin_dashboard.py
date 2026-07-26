import streamlit as st

def render_admin():
    st.markdown(
        """
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px;'>
            <h1 class='section-title' style='margin: 0;'>Analytics Dashboard</h1>
            <div style='display: flex; gap: 12px;'>
                <button style='background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #FFF; padding: 8px 16px; border-radius: 8px; font-weight: 500; font-family: "Inter", sans-serif; font-size: 14px;'>Last 7 Days ▾</button>
                <button style='background: #FFFFFF; border: none; color: #000; padding: 8px 16px; border-radius: 8px; font-weight: 600; font-family: "Inter", sans-serif; font-size: 14px;'>Export CSV</button>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # KPI Metric Cards (Stripe / Vercel style)
    cols = st.columns(4)
    metrics = [
        {"label": "Total Revenue", "value": "$24,592.00", "trend": "+12.5%", "is_positive": True},
        {"label": "Active Orders", "value": "142", "trend": "+5.2%", "is_positive": True},
        {"label": "Customers", "value": "1,894", "trend": "+2.1%", "is_positive": True},
        {"label": "Avg Order Value", "value": "$42.50", "trend": "-1.4%", "is_positive": False}
    ]
    
    for i, metric in enumerate(metrics):
        with cols[i]:
            with st.container(border=True):
                trend_color = "#22C55E" if metric["is_positive"] else "#EF4444"
                st.markdown(f"<p class='small-text' style='margin: 0 0 8px 0; font-weight: 500;'>{metric['label']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 28px; font-weight: 700; color: #FFF; margin: 0 0 8px 0;'>{metric['value']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 12px; font-weight: 600; color: {trend_color}; margin: 0; display: inline-flex; align-items: center; background: {trend_color}15; padding: 2px 6px; border-radius: 4px;'>{metric['trend']} vs last week</p>", unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)

    # Charts and Tables layout
    c1, c2 = st.columns([2, 1], gap="large")
    
    with c1:
        st.markdown("<h3 class='card-title' style='font-size: 18px; margin-bottom: 24px;'>Revenue Overview</h3>", unsafe_allow_html=True)
        # We simulate a modern chart by using an image or styled blocks since native st.line_chart is hard to style perfectly
        # In a real app we'd use Plotly styled darkly, but here we'll use st.bar_chart as a placeholder that inherits dark mode nicely
        import pandas as pd
        import numpy as np
        chart_data = pd.DataFrame(
            np.random.randn(20, 1) + 5,
            columns=['Revenue']
        )
        st.bar_chart(chart_data, height=350, use_container_width=True)
        
    with c2:
        st.markdown("<h3 class='card-title' style='font-size: 18px; margin-bottom: 24px;'>Live Activity</h3>", unsafe_allow_html=True)
        activities = [
            {"user": "Alex M.", "action": "placed order #492", "time": "Just now"},
            {"user": "Sarah K.", "action": "left a 5-star review", "time": "2 min ago"},
            {"user": "James D.", "action": "placed order #491", "time": "12 min ago"},
            {"user": "Emily R.", "action": "created account", "time": "1 hr ago"},
            {"user": "Michael T.", "action": "placed order #490", "time": "2 hrs ago"}
        ]
        
        with st.container(border=True):
            for i, act in enumerate(activities):
                st.markdown(
                    f"""
                    <div style='display: flex; gap: 12px; margin-bottom: {16 if i < len(activities)-1 else 0}px;'>
                        <div style='width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.1); flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 600; color: #FFF;'>
                            {act['user'][0]}
                        </div>
                        <div>
                            <p style='margin: 0; font-size: 14px; color: #FFF; font-weight: 500;'><span style='color: #FF5A5F;'>{act['user']}</span> {act['action']}</p>
                            <p style='margin: 4px 0 0 0; font-size: 12px; color: #9CA3AF;'>{act['time']}</p>
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
