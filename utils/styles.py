import streamlit as st

def load_css():
    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #1E1B4B 0%, #0F172A 40%, #020617 100%);
        color: #F8FAFC;
        font-family: 'Segoe UI', sans-serif;
    }

    .main-title {
        text-align: center;
        font-size: 3.2rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-top: 10px;
        margin-bottom: 8px;
        letter-spacing: 0.5px;
    }

    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #94A3B8;
        margin-bottom: 30px;
    }

    .neo-card {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 24px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.28);
        backdrop-filter: blur(16px);
    }

    .feature-card {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 22px;
        padding: 24px;
        min-height: 250px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.28);
        transition: all 0.25s ease;
        margin-bottom: 12px;
    }

    .feature-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 16px 45px rgba(99,102,241,0.22);
    }

    .algo-badge {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        background: linear-gradient(135deg, #4F46E5, #7C3AED);
        color: white;
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 18px;
    }

    .feature-title {
        font-size: 1.55rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 14px;
    }

    .feature-desc {
        color: #CBD5E1;
        font-size: 1rem;
        line-height: 1.7;
    }

    .section-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 16px;
    }

    .desc-text {
        color: #CBD5E1;
        font-size: 1rem;
        line-height: 1.8;
    }

    .ready-box {
        background: rgba(30, 41, 59, 0.72);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 20px;
        padding: 26px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 10px 28px rgba(0,0,0,0.24);
    }

    .ready-box h3 {
        color: #F8FAFC;
        margin-bottom: 10px;
        font-size: 1.5rem;
    }

    .ready-box p {
        color: #94A3B8;
        font-size: 1rem;
    }

    .soft-card {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 24px;
        margin-top: 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.22);
    }

    .metric-title {
        color: #94A3B8;
        font-size: 0.95rem;
        margin-bottom: 6px;
        margin-top: 10px;
    }

    .metric-value {
        color: #F8FAFC;
        font-size: 1.7rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .footer-note {
        text-align: center;
        color: #64748B;
        margin-top: 40px;
        margin-bottom: 20px;
        font-size: 0.95rem;
    }

    .stButton > button {
        width: 100%;
        border-radius: 16px;
        border: none;
        padding: 0.8rem 1rem;
        font-weight: 700;
        font-size: 1rem;
        background: linear-gradient(135deg, #4F46E5, #7C3AED);
        color: white;
        box-shadow: 0 10px 24px rgba(99,102,241,0.32);
        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 30px rgba(99,102,241,0.42);
    }

    .stSlider label, .stSelectbox label {
        color: #E2E8F0 !important;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)