import streamlit as st

def inject_custom_css():
    st.markdown(
        """
        <style>
        /* ========================================================================= */
        /* WORLD-CLASS SAAS DESIGN SYSTEM (Vercel/Linear/Stripe Aesthetic)           */
        /* ========================================================================= */
        
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        :root {
            --bg: #0F172A;
            --card-bg: #1E293B;
            --accent: #F59E0B;
            --accent-hover: #D97706;
            --success: #22C55E;
            --warning: #FACC15;
            --text-main: #FFFFFF;
            --text-secondary: #9CA3AF;
            --border-color: rgba(255, 255, 255, 0.08);
            --radius: 24px;
            --shadow-sm: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            --shadow-md: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
            --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
            --font-main: 'Inter', sans-serif;
        }

        /* ------------------------------------------------------------------------- */
        /* GLOBAL RESET & TYPOGRAPHY                                                 */
        /* ------------------------------------------------------------------------- */
        html, body, [class*="css"] {
            font-family: var(--font-main) !important;
            color: var(--text-main) !important;
            background-color: var(--bg) !important;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        /* Streamlit UI Erasure */
        #MainMenu, footer { display: none !important; }
        header[data-testid="stHeader"] { display: none !important; }
        [data-testid="stDecoration"], [data-testid="stToolbar"], .stDeployButton { display: none !important; }
        
        /* Master Layout Container */
        .block-container {
            padding-top: 5rem !important; /* Space for floating navbar */
            padding-bottom: 8rem !important;
            max-width: 1400px !important; /* Wider canvas for SaaS look */
            margin: 0 auto !important;
        }

        /* ------------------------------------------------------------------------- */
        /* COMPONENT LIBRARY                                                         */
        /* ------------------------------------------------------------------------- */
        
        /* Premium Cards */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: var(--card-bg) !important;
            border-radius: var(--radius) !important;
            border: 1px solid var(--border-color) !important;
            box-shadow: var(--shadow-sm) !important;
            padding: 24px !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-4px) !important;
            box-shadow: var(--shadow-md) !important;
            border-color: rgba(255, 255, 255, 0.15) !important;
        }

        /* High-End Images */
        img {
            border-radius: 16px !important;
            object-fit: cover !important;
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover img {
            transform: scale(1.05); /* Image zoom on hover */
        }

        /* Typography Hierarchy (Strict Apple/Stripe rules) */
        .hero-title {
            font-size: 64px;
            font-weight: 700;
            line-height: 1.1;
            letter-spacing: -0.04em;
            color: var(--text-main);
            margin: 0 0 16px 0;
        }
        .section-title {
            font-size: 36px;
            font-weight: 600;
            letter-spacing: -0.02em;
            color: var(--text-main);
            margin: 0 0 32px 0;
        }
        .card-title {
            font-size: 22px;
            font-weight: 600;
            letter-spacing: -0.01em;
            color: var(--text-main);
            margin: 16px 0 8px 0;
        }
        .body-text {
            font-size: 16px;
            font-weight: 400;
            line-height: 1.5;
            color: var(--text-secondary);
        }
        .small-text {
            font-size: 14px;
            font-weight: 400;
            color: var(--text-secondary);
        }

        /* Inputs & Search (Vercel Style) */
        .stTextInput input, .stSelectbox > div > div {
            background-color: rgba(255,255,255,0.03) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 12px !important;
            color: var(--text-main) !important;
            padding: 12px 16px !important;
            transition: all 0.2s ease !important;
            font-size: 16px !important;
            font-family: var(--font-main) !important;
        }
        .stTextInput input:focus, .stSelectbox > div > div:focus-within {
            border-color: var(--text-secondary) !important;
            background-color: rgba(255,255,255,0.06) !important;
            box-shadow: none !important;
        }

        /* Modern Buttons */
        div[data-testid="stButton"] button {
            border-radius: 12px !important;
            font-weight: 500 !important;
            font-size: 16px !important;
            border: 1px solid var(--border-color) !important;
            background-color: rgba(255,255,255,0.05) !important;
            color: var(--text-main) !important;
            transition: all 0.2s ease !important;
            min-height: 44px !important;
            width: 100% !important;
        }
        div[data-testid="stButton"] button:hover {
            border-color: rgba(255,255,255,0.2) !important;
            background-color: rgba(255,255,255,0.1) !important;
        }
        div[data-testid="stButton"] button:active {
            transform: scale(0.98) !important;
        }
        
        /* Primary Action Button */
        div[data-testid="stButton"] button[kind="primary"] {
            background-color: var(--accent) !important;
            border: none !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover {
            background-color: var(--accent-hover) !important;
            box-shadow: 0 4px 12px rgba(255, 90, 95, 0.4) !important;
            transform: translateY(-1px) !important;
        }
        div[data-testid="stButton"] button[kind="primary"]:active {
            transform: scale(0.98) !important;
        }

        /* Universal Tags / Badges */
        .badge {
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: inline-block;
        }
        .badge-success { background: rgba(34, 197, 94, 0.15); color: var(--success); }
        .badge-warning { background: rgba(250, 204, 21, 0.15); color: var(--warning); }
        .badge-accent { background: rgba(255, 90, 95, 0.15); color: var(--accent); }

        /* Minimal Dividers */
        hr {
            border: 0 !important;
            height: 1px !important;
            background-color: var(--border-color) !important;
            margin: 2rem 0 !important;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg); }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.25); }

        </style>
        """,
        unsafe_allow_html=True
    )
