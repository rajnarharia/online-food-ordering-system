import streamlit as st
import json
import pandas as pd
import plotly.express as px

def render_admin():
    st.markdown("<h2 class='hero-title' style='font-size: 2.5rem; margin-bottom: 24px;'>Dashboard</h2>", unsafe_allow_html=True)
    
    with open("data/orders.json", "r") as file:
        orders = json.load(file)
        
    total_rev = sum(o["total"] for o in orders)
    total_orders = len(orders)
    
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        with st.container(border=True):
            st.markdown("<p class='stat-label'>Total Revenue</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='stat-value'>₹{total_rev}</p>", unsafe_allow_html=True)
            st.markdown("<p style='color: #10B981; font-size: 0.8rem; font-weight: 600; margin-top: 8px;'>↑ 12% vs last week</p>", unsafe_allow_html=True)
    with c2:
        with st.container(border=True):
            st.markdown("<p class='stat-label'>Total Orders</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='stat-value'>{total_orders}</p>", unsafe_allow_html=True)
            st.markdown("<p style='color: #10B981; font-size: 0.8rem; font-weight: 600; margin-top: 8px;'>↑ 8% vs last week</p>", unsafe_allow_html=True)
    with c3:
        with st.container(border=True):
            st.markdown("<p class='stat-label'>Active Users</p>", unsafe_allow_html=True)
            st.markdown("<p class='stat-value'>2.4k</p>", unsafe_allow_html=True)
            st.markdown("<p style='color: #10B981; font-size: 0.8rem; font-weight: 600; margin-top: 8px;'>↑ 5% vs last week</p>", unsafe_allow_html=True)
            
    st.write("<br>", unsafe_allow_html=True)
    st.markdown("<p class='card-title'>Revenue Trends</p>", unsafe_allow_html=True)
    
    # Chart styling dynamically
    accent = "#E23744" if st.session_state.theme == "Light" else "#FF5A5F"
    font_color = "#64748B" if st.session_state.theme == "Light" else "#94A3B8"
    
    dates = pd.date_range(end=pd.Timestamp.today(), periods=7)
    revenue = [1200, 1500, 1100, 1800, 2100, 1700, total_rev]
    df = pd.DataFrame({'Date': dates, 'Revenue': revenue})
    
    fig = px.line(df, x='Date', y='Revenue')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(showgrid=False, color=font_color),
        yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.1)', color=font_color)
    )
    fig.update_traces(line_color=accent, line_width=3)
    
    st.plotly_chart(fig, use_container_width=True)
