import streamlit as st
from core_logic import PipeSpecifications

st.set_page_config(page_title="کنترل خط اسپیرال", layout="wide")

# استایل اختصاصی برای تم تیره، اعداد مشکی پررنگ و قاب یکپارچه
st.markdown("""
<style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    
    /* کادر یکپارچه اصلی شامل ورودی‌ها و کشوی خروجی */
    div[data-testid="stForm"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 15px;
    }

    /* تنظیم ورودی‌ها: پس‌زمینه روشن و فونت مشکی مشکی */
    div[data-baseweb="input"] { 
        background-color: #ffffff !important; 
        border: 1px solid #94a3b8 !important;
        border-radius: 6px !important; 
    }
    input { 
        color: #000000 !important; 
        font-weight: 900 !important; 
        font-size: 1rem !important; 
    }
    label { 
        font-size: 0.8rem !important; 
        color: #cbd5e1 !important; 
        font-weight: 700 !important; 
        white-space: nowrap;
    }

    /* استایل کشو برای تطابق با قاب یکپارچه */
    .stExpander {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        margin-top: 15px;
    }

    /* کارت‌های خروجی محاسباتی */
    .kpi-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 8px;
        text-align: center;
    }
    .kpi-title { color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 2px; }
    .kpi-value { color: #38bdf8; font-size: 1.15rem; font-weight: 800; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; color: #f8fafc; margin-bottom: 15px;'>⚙️ مرکز کنترل و تنظیمات خط اسپیرال</h4>", unsafe_allow_html=True)

# قاب یکپارچه اصلی با st.form
with st.form("main_control_panel", clear_on_submit=False):
    # ۷ ورودی در یک ردیف
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

    with c1:
        D = st.number_input("قطر D (mm)", value=1800.0, step=10.0)
    with c2:
        t = st.number_input("ضخامت t (mm)", value=14.2, step=0.1)
    with c3:
        W = st.number_input("عرض W (mm)", value=1500.0, step=10.0)
    with c4:
        L = st.number_input("طول L (mm)", value=12020.0, step=10.0)
    with c5:
        limit = st.number_input("حد T (mm)", value=300.0, step=10.0)
    with c6:
        lead = st.number_input("پرت سر (mm)", value=400.0, step=10.0)
    with c7:
        tail = st.number_input("پرت ته (mm)", value=300.0, step=10.0)

    # دکمه به‌روزرسانی برای تغییر فرم
    submitted = st.form_submit_button("اعمال تغییرات", use_container_width=True)

    # فراخوانی ایمن منطق محاسباتی
    try:
        specs = PipeSpecifications(
            outer_diameter=D,
            wall_thickness=t,
            strip_width=W,
            standard_length=L,
            t_joint_limit=limit,
            default_lead_crop=lead,
            default_tail_crop=tail
        )
    except TypeError:
        specs = PipeSpecifications(
            outer_diameter=D,
            wall_thickness=t,
            strip_width=W,
            standard_length=L,
            t_joint_limit=limit
        )

    # کشوی خروجی‌های محاسباتی - پیش‌فرض بسته (expanded=False)
    with st.expander("📊 داده‌های محاسبه‌شده هندسی (کلیک کنید)", expanded=False):
        k1, k2, k3, k4, k5 = st.columns(5)
        
        k1.markdown(f"<div class='kpi-card'><div class='kpi-title'>زاویه هلیکس (α)</div><div class='kpi-value' style='color:#4ade80;'>{specs.helix_angle_deg:.2f}°</div></div>", unsafe_allow_html=True)
        k2.markdown(f"<div class='kpi-card'><div class='kpi-title'>محیط متوسط (C)</div><div class='kpi-value'>{specs.perimeter:.1f} mm</div></div>", unsafe_allow_html=True)
        k3.markdown(f"<div class='kpi-card'><div class='kpi-title'>گام جوش (P)</div><div class='kpi-value'>{specs.weld_pitch:.1f} mm</div></div>", unsafe_allow_html=True)
        k4.markdown(f"<div class='kpi-card'><div class='kpi-title'>قطر متوسط (D_m)</div><div class='kpi-value'>{specs.mean_diameter:.1f} mm</div></div>", unsafe_allow_html=True)
        
        strip_ratio = specs.pipe_length_to_strip_length(1000.0) / 1000.0
        k5.markdown(f"<div class='kpi-card'><div class='kpi-title'>ضریب مصرف ورق</div><div class='kpi-value' style='color:#facc15;'>{strip_ratio:.3f} m/m</div></div>", unsafe_allow_html=True)
