import streamlit as st
from core_logic import PipeSpecifications

st.set_page_config(page_title="کنترل خط اسپیرال", layout="wide")

# استایل اختصاصی برای خوانایی ۱۰۰٪ متون و چیدمان شیک تیره
st.markdown("""
<style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    
    /* تنظیم ورودی‌ها برای خوانایی کامل روی موبایل */
    div[data-baseweb="input"] { 
        background-color: #1e293b !important; 
        border: 1px solid #475569 !important;
        border-radius: 6px !important; 
    }
    input { color: #38bdf8 !important; font-weight: bold !important; font-size: 0.95rem !important; }
    label { font-size: 0.8rem !important; color: #cbd5e1 !important; font-weight: 700 !important; }

    /* استایل نوار بازشونده محاسبات */
    .stExpander {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }

    /* کارت‌های خروجی محاسباتی */
    .kpi-card {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 10px;
        text-align: center;
        margin-top: 5px;
    }
    .kpi-title { color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 4px; }
    .kpi-value { color: #38bdf8; font-size: 1.15rem; font-weight: 800; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; color: #f8fafc; margin-bottom: 20px;'>⚙️ پارامترهای ثابت و محاسبات هندسی خط</h4>", unsafe_allow_html=True)

# ۱. پارامترهای ثابت در ردیف‌های منظم و خوانا
c1, c2, c3, c4 = st.columns(4)
with c1:
    D = st.number_input("قطر خارجی D (mm)", value=1800.0, step=10.0)
    limit = st.number_input("حد مجاز T (mm)", value=300.0, step=10.0)
with c2:
    t = st.number_input("ضخامت t (mm)", value=14.2, step=0.1)
    lead = st.number_input("پرت سر کلاف (mm)", value=400.0, step=10.0)
with c3:
    W = st.number_input("عرض ورق W (mm)", value=1500.0, step=10.0)
    tail = st.number_input("پرت ته کلاف (mm)", value=300.0, step=10.0)
with c4:
    L = st.number_input("طول شاخه L (mm)", value=12020.0, step=10.0)

# فراخوانی ایمن کلاس (اگر متغیرهای پرت در core_logic نباشد هم برنامه کرش نمی‌کند)
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

st.markdown("<br>", unsafe_allow_html=True)

# ۲. نوار رنگی بازشونده با کلیک برای مشاهده محاسبات
with st.expander("📊 **مشاهده داده‌های محاسبه‌شده هندسی (کلیک کنید)**", expanded=True):
    k1, k2, k3, k4, k5 = st.columns(5)
    
    k1.markdown(f"<div class='kpi-card'><div class='kpi-title'>زاویه هلیکس (α)</div><div class='kpi-value' style='color:#4ade80;'>{specs.helix_angle_deg:.2f}°</div></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi-card'><div class='kpi-title'>محیط متوسط (C)</div><div class='kpi-value'>{specs.perimeter:.1f} mm</div></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi-card'><div class='kpi-title'>گام جوش (P)</div><div class='kpi-value'>{specs.weld_pitch:.1f} mm</div></div>", unsafe_allow_html=True)
    k4.markdown(f"<div class='kpi-card'><div class='kpi-title'>قطر متوسط (D_m)</div><div class='kpi-value'>{specs.mean_diameter:.1f} mm</div></div>", unsafe_allow_html=True)
    
    strip_ratio = specs.pipe_length_to_strip_length(1000.0) / 1000.0
    k5.markdown(f"<div class='kpi-card'><div class='kpi-title'>ضریب مصرف ورق</div><div class='kpi-value' style='color:#facc15;'>{strip_ratio:.3f} m/m</div></div>", unsafe_allow_html=True)
