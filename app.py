import streamlit as st
from core_logic import PipeSpecifications

st.set_page_config(page_title="کنترل خط اسپیرال", layout="wide")

# استایل تم تیره و فشرده
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #e2e8f0; }
    .block-container { padding-top: 1rem; padding-bottom: 0.5rem; }
    
    /* فشرده‌سازی ورودی‌ها برای جا شدن در یک ردیف */
    div[data-baseweb="input"] { height: 36px; background-color: #1e293b; border-radius: 4px; }
    input { color: #ffffff !important; font-weight: bold; font-size: 0.85rem !important; }
    label { font-size: 0.75rem !important; color: #94a3b8 !important; font-weight: 600 !important; white-space: nowrap; }

    /* کارت‌های خروجی محاسباتی */
    .kpi-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 10px;
        text-align: center;
    }
    .kpi-title { color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 4px; }
    .kpi-value { color: #38bdf8; font-size: 1.2rem; font-weight: 800; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; color: #f8fafc; margin-bottom: 15px;'>⚙️ پارامترهای ثابت و محاسبات هندسی خط</h4>", unsafe_allow_html=True)

# ۱. تمام ۷ پارامتر ورودی در یک ردیف منظم
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

specs = PipeSpecifications(
    outer_diameter=D,
    wall_thickness=t,
    strip_width=W,
    standard_length=L,
    t_joint_limit=limit,
    default_lead_crop=lead,
    default_tail_crop=tail
)

st.write("")

# ۲. نوار با رنگ متفاوت و فلش بازشونده برای داده‌های محاسبه‌شده
with st.expander("📊 **مشاهده داده‌های محاسبه‌شده هندسی (کلیک کنید)**", expanded=True):
    k1, k2, k3, k4, k5 = st.columns(5)
    
    k1.markdown(f"<div class='kpi-card'><div class='kpi-title'>زاویه هلیکس (α)</div><div class='kpi-value' style='color:#4ade80;'>{specs.helix_angle_deg:.2f}°</div></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi-card'><div class='kpi-title'>محیط متوسط (C)</div><div class='kpi-value'>{specs.perimeter:.1f} mm</div></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi-card'><div class='kpi-title'>گام جوش (P)</div><div class='kpi-value'>{specs.weld_pitch:.1f} mm</div></div>", unsafe_allow_html=True)
    k4.markdown(f"<div class='kpi-card'><div class='kpi-title'>قطر متوسط (D_m)</div><div class='kpi-value'>{specs.mean_diameter:.1f} mm</div></div>", unsafe_allow_html=True)
    
    strip_ratio = specs.pipe_length_to_strip_length(1000.0) / 1000.0
    k5.markdown(f"<div class='kpi-card'><div class='kpi-title'>ضریب مصرف ورق</div><div class='kpi-value' style='color:#facc15;'>{strip_ratio:.3f} m/m</div></div>", unsafe_allow_html=True)
