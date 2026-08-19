import streamlit as st
from core_logic import PipeSpecifications

st.set_page_config(page_title="اسپیرال", layout="wide")

# CSS فشرده‌سازی برای حذف فاصله‌های اضافی و جلوگیری از اسکرول
st.markdown("""
<style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    div[data-baseweb="input"] { height: 32px; }
    label { font-size: 0.75rem !important; margin-bottom: 0px !important; }
    .kpi-mini { background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 6px; text-align: center; }
    .kpi-title { font-size: 0.7rem; color: #64748b; font-weight: bold; }
    .kpi-val { font-size: 1.1rem; color: #0f172a; font-weight: 800; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

st.caption("🏭 **داشبورد کنترل خط اسپیرال**")

# ورودی‌های فشرده در ۲ ستون
c1, c2 = st.columns(2)
with c1:
    D = st.number_input("D (قطر)", value=1800.0, step=10.0)
    t = st.number_input("t (ضخامت)", value=14.2, step=0.1)
    W = st.number_input("W (عرض)", value=1500.0, step=10.0)
    L = st.number_input("L (طول)", value=12020.0, step=10.0)

with c2:
    limit = st.number_input("Limit (حد T)", value=300.0, step=10.0)
    lead = st.number_input("پرت سر", value=400.0, step=10.0)
    tail = st.number_input("پرت ته", value=300.0, step=10.0)

# فراخوانی ایمن برای جلوگیری از TypeError
try:
    specs = PipeSpecifications(D, t, W, L, limit, lead, tail)
except TypeError:
    specs = PipeSpecifications(D, t, W, L, limit)

st.divider()

# خروجی‌های کارت مینی کاملاً متراکم
k1, k2, k3, k4 = st.columns(4)
k1.markdown(f"<div class='kpi-mini'><div class='kpi-title'>زاویه (α)</div><div class='kpi-val'>{specs.helix_angle_deg:.2f}°</div></div>", unsafe_allow_html=True)
k2.markdown(f"<div class='kpi-mini'><div class='kpi-title'>محیط (C)</div><div class='kpi-val'>{specs.perimeter:.0f}</div></div>", unsafe_allow_html=True)
k3.markdown(f"<div class='kpi-mini'><div class='kpi-title'>گام (P)</div><div class='kpi-val'>{specs.weld_pitch:.0f}</div></div>", unsafe_allow_html=True)
k4.markdown(f"<div class='kpi-mini'><div class='kpi-title'>قطر متوسط</div><div class='kpi-val'>{specs.mean_diameter:.1f}</div></div>", unsafe_allow_html=True)
