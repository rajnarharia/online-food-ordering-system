import streamlit as st

def inject_custom_css():
    theme = st.session_state.get("theme", "Dark")
    
    # Ultra-Premium "Midnight Gourmet" Design System
    if theme == "Light":
        bg_color = "#F8FAFC" 
        card_bg = "rgba(255, 255, 255, 0.6)"
        text_main = "#0F172A"
        text_muted = "#64748B"
        border_color = "rgba(0, 0, 0, 0.05)"
        accent_1 = "#F43F5E" # Rose
        accent_2 = "#FB923C" # Orange
    else:
        bg_color = "#0B0C10" # Very deep luxury black-blue
        card_bg = "rgba(22, 24, 32, 0.55)" # Deep frost
        text_main = "#F8FAFC"
        text_muted = "#94A3B8"
        border_color = "rgba(255, 255, 255, 0.04)"
        accent_1 = "#FF4B2B" # Vibrant Red-Orange
        accent_2 = "#FF416C" # Vibrant Pink

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap');

        /* Master Reset */
        html, body, [class*="css"] {{
            font-family: 'Manrope', sans-serif !important;
            color: {text_main} !important;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        /* Dynamic Luxury Background */
        .stApp {{
            background-color: {bg_color} !important;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(255, 75, 43, 0.03) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(255, 65, 108, 0.03) 0%, transparent 40%),
                linear-gradient(180deg, rgba(11, 12, 16, 0.9) 0%, rgba(11, 12, 16, 1) 100%) !important;
            background-attachment: fixed !important;
        }}

        /* Hide Default UI & Streamlit Branding Completely */
        #MainMenu, footer {{display: none !important;}}
        header[data-testid="stHeader"] {{ display: none !important; }}
        [data-testid="stDecoration"], [data-testid="stToolbar"], .stDeployButton {{ display: none !important; }}

        /* Animations */
        @keyframes fadeSlideUp {{
            0% {{ opacity: 0; transform: translateY(40px) scale(0.97); filter: blur(5px); }}
            100% {{ opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }}
        }}
        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        @keyframes floatEffect {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}

        /* Layout Container */
        .block-container {{
            padding-top: 3.5rem !important;
            padding-bottom: 7rem !important;
            max-width: 1300px !important;
            animation: fadeSlideUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        }}

        /* Ultra-Premium Glass Cards */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: {card_bg} !important;
            backdrop-filter: blur(28px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
            border-radius: 24px !important;
            border: 1px solid {border_color} !important;
            box-shadow: 0 8px 32px -8px rgba(0,0,0,0.4) !important;
            transition: all 0.5s cubic-bezier(0.25, 1, 0.5, 1) !important;
            padding: 24px !important;
            position: relative;
            overflow: hidden;
        }}
        
        /* Inner lighting for cards */
        div[data-testid="stVerticalBlockBorderWrapper"]::before {{
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 24px;
            padding: 1px;
            background: linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0) 50%);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            pointer-events: none;
        }}

        div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
            transform: translateY(-8px) scale(1.01) !important;
            box-shadow: 0 20px 40px -10px rgba(0,0,0,0.6), 0 0 20px rgba(255, 75, 43, 0.05) !important;
            border-color: rgba(255, 255, 255, 0.1) !important;
        }}

        /* Images - Michelin Star Style */
        img {{
            border-radius: 18px !important;
            object-fit: cover !important;
            transition: transform 0.8s cubic-bezier(0.25, 1, 0.5, 1), filter 0.8s ease !important;
            filter: brightness(0.9) contrast(1.1) saturate(1.1);
        }}
        div[data-testid="stVerticalBlockBorderWrapper"]:hover img {{
            transform: scale(1.08);
            filter: brightness(1.05) contrast(1.15) saturate(1.2);
        }}
        
        /* Modern Inputs & Selects */
        .stTextInput input, .stSelectbox > div > div {{
            background-color: rgba(255,255,255,0.02) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 16px !important;
            color: {text_main} !important;
            padding: 14px 18px !important;
            transition: all 0.3s ease !important;
            font-weight: 500 !important;
            font-size: 1rem !important;
        }}
        .stTextInput input:focus, .stSelectbox > div > div:focus-within {{
            border-color: {accent_1} !important;
            background-color: rgba(255,255,255,0.04) !important;
            box-shadow: 0 0 0 4px rgba(255, 75, 43, 0.15) !important;
        }}

        /* Secondary Buttons */
        div[data-testid="stButton"] button {{
            border-radius: 100px !important; /* Pill shape for luxury */
            font-weight: 700 !important;
            font-size: 1rem !important;
            letter-spacing: 0.02em !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            background: rgba(255,255,255,0.03) !important;
            backdrop-filter: blur(10px) !important;
            color: {text_main} !important;
            transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1) !important;
            height: 54px !important;
            width: 100% !important;
            text-transform: uppercase !important;
        }}
        div[data-testid="stButton"] button:hover {{
            border-color: rgba(255,255,255,0.3) !important;
            transform: translateY(-4px) !important;
            background: rgba(255,255,255,0.08) !important;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3) !important;
        }}
        
        /* The "Wow" Primary Button */
        div[data-testid="stButton"] button[kind="primary"] {{
            background: linear-gradient(135deg, {accent_1}, {accent_2}, {accent_1}) !important;
            background-size: 200% 200% !important;
            border: none !important;
            color: #FFFFFF !important;
            box-shadow: 0 10px 30px -5px rgba(255, 75, 43, 0.4), inset 0 -3px 0 rgba(0,0,0,0.1) !important;
            animation: gradientShift 6s ease infinite !important;
            transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }}
        div[data-testid="stButton"] button[kind="primary"]:hover {{
            box-shadow: 0 15px 40px -5px rgba(255, 75, 43, 0.6), inset 0 -3px 0 rgba(0,0,0,0.1) !important;
            transform: translateY(-4px) scale(1.02) !important;
        }}

        /* Typography - Fine Dining Elegance */
        .hero-title {{
            font-family: 'Playfair Display', serif;
            font-size: 5.5rem;
            font-weight: 700;
            line-height: 1.1;
            letter-spacing: -0.02em;
            color: {text_main};
            margin-bottom: 20px;
        }}
        .hero-title span {{
            background: linear-gradient(135deg, {accent_1}, {accent_2});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'Manrope', sans-serif;
            font-weight: 800;
            font-style: italic;
            display: inline-block;
        }}
        .hero-subtitle {{
            font-size: 1.3rem;
            color: {text_muted};
            line-height: 1.7;
            margin-bottom: 48px;
            font-weight: 400;
            max-width: 550px;
            letter-spacing: 0.01em;
        }}
        .card-title {{
            font-family: 'Playfair Display', serif;
            font-size: 1.6rem;
            font-weight: 700;
            color: {text_main};
            margin: 18px 0 6px 0;
            line-height: 1.2;
        }}
        .card-meta {{
            font-size: 0.95rem;
            color: {text_muted};
            font-weight: 500;
            margin-bottom: 24px;
            line-height: 1.5;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .price-tag {{
            font-size: 2rem;
            font-weight: 800;
            color: {text_main};
            letter-spacing: -0.03em;
        }}
        .rating-tag {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #F59E0B;
            background: rgba(245, 158, 11, 0.08);
            border: 1px solid rgba(245, 158, 11, 0.2);
            padding: 6px 14px;
            border-radius: 100px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        
        /* Data Stats */
        .stat-label {{
            font-size: 0.85rem;
            font-weight: 600;
            color: {text_muted};
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 0.15em;
        }}
        .stat-value {{
            font-size: 3.5rem;
            font-family: 'Playfair Display', serif;
            font-weight: 700;
            margin: 4px 0 0 0;
            line-height: 1;
            background: linear-gradient(135deg, #FFFFFF, #94A3B8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        /* High-End Badges */
        .pill-veg, .pill-discount {{
            padding: 6px 14px;
            border-radius: 100px;
            font-weight: 800;
            font-size: 0.75rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .pill-veg {{
            background: rgba(16, 185, 129, 0.15);
            color: #34D399;
            border-color: rgba(16, 185, 129, 0.3);
        }}
        .pill-discount {{
            background: rgba(255, 75, 43, 0.15);
            color: #FF4B2B;
            border-color: rgba(255, 75, 43, 0.3);
            box-shadow: 0 0 15px rgba(255, 75, 43, 0.2);
        }}
        
        /* Polished Custom Scrollbar */
        ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        ::-webkit-scrollbar-thumb {{
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
        }}
        ::-webkit-scrollbar-thumb:hover {{ background: rgba(255,255,255,0.2); }}

        /* Elegant Dividers */
        hr {{
            border: 0 !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent) !important;
            margin: 4rem 0 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
