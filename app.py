import streamlit as st
from core_logic import PipeSpecifications

# تنظیمات پایه و ظاهر صنعتی
st.set_page_config(
    page_title="سیستم مانیتورینگ کارخانه لوله‌سازی اسپیرال",
    page_icon="⚙️",
    layout="wide"
)

# استایل بصری فاخر و متراکم (Dark Industrial Theme)
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    
    /* کارت‌های شاخص مهندسی */
    .kpi-card {
        background: linear-gradient(135deg, #1f2430 0%, #161922 100%);
        border: 1px solid #2e3545;
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .kpi-title { color: #8a99ad; font-size: 0.85rem; font-weight: bold; margin-bottom: 4px; }
    .kpi-value { color: #ffffff; font-size: 1.4rem; font-weight: 800; font-family: monospace; }
    .kpi-unit { color: #00d26a; font-size: 0.85rem; margin-left: 3px; }
</style>
""", unsafe_allow_html=True)

# سربرگ اصلی
st.markdown("<h2 style='text-align: center; color: #f0f2f6; margin-bottom: 0px;'>🏭 مرکز مانیتورینگ و کنترل خطوط اسپیرال</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8a99ad; font-size: 0.9rem; margin-bottom: 25px;'>تنظیمات پایه و محاسبات هندسی محض</p>", unsafe_allow_html=True)

# پانل تنظیمات ثابت (فشرده در ۷ ستون یکنواخت)
with st.expander("🛠️ تنظیمات پارامترهای ثابت خط (کلیک برای ویرایش)", expanded=True):
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    
    D = c1.number_input("قطر خارجی (mm)", value=1800.0, step=10.0, key="D_val")
    t = c2.number_input("ضخامت (mm)", value=14.2, step=0.1, key="t_val")
    W = c3.number_input("عرض ورق (mm)", value=1500.0, step=10.0, key="W_val")
    L = c4.number_input("طول شاخه (mm)", value=12020.0, step=10.0, key="L_val")
    limit = c5.number_input("حد مجاز T (mm)", value=300.0, step=10.0, key="Limit_val")
    
    # اضافه شدن دو متغیر پیش‌فرض پرت سر و ته
    default_lead = c6.number_input("پرت سر کلاف (mm)", value=400.0, step=10.0, key="lead_val")
    default_tail = c7.number_input("پرت ته کلاف (mm)", value=300.0, step=10.0, key="tail_val")

# ساخت شیء هندسی بر اساس ورودی‌ها
specs = PipeSpecifications(
    outer_diameter=D,
    wall_thickness=t,
    strip_width=W,
    standard_length=L,
    t_joint_limit=limit,
    default_lead_crop=default_lead,
    default_tail_crop=default_tail
)

st.divider()

# نمایش کارت‌های شاخص مهندسی در یک نوار شیک
st.markdown("### 📊 خروجی‌های محاسباتی پایه")
k1, k2, k3, k4, k5 = st.columns(5)

k1.markdown(f"""
<div class='kpi-card' style='border-left: 4px solid #00d26a;'>
    <div class='kpi-title'>زاویه هلیکس (α)</div>
    <div class='kpi-value'>{specs.helix_angle_deg:.2f}<span class='kpi-unit'>°</span></div>
</div>
""", unsafe_allow_html=True)

k2.markdown(f"""
<div class='kpi-card' style='border-left: 4px solid #00b4d8;'>
    <div class='kpi-title'>محیط متوسط (C)</div>
    <div class='kpi-value'>{specs.perimeter:.1f}<span class='kpi-unit'>mm</span></div>
</div>
""", unsafe_allow_html=True)

k3.markdown(f"""
<div class='kpi-card' style='border-left: 4px solid #00b4d8;'>
    <div class='kpi-title'>گام جوش (P)</div>
    <div class='kpi-value'>{specs.weld_pitch:.1f}<span class='kpi-unit'>mm</span></div>
</div>
""", unsafe_allow_html=True)

k4.markdown(f"""
<div class='kpi-card' style='border-left: 4px solid #00b4d8;'>
    <div class='kpi-title'>قطر متوسط (D_m)</div>
    <div class='kpi-value'>{specs.mean_diameter:.1f}<span class='kpi-unit'>mm</span></div>
</div>
""", unsafe_allow_html=True)

strip_ratio = specs.pipe_length_to_strip_length(1000.0) / 1000.0
k5.markdown(f"""
<div class='kpi-card' style='border-left: 4px solid #fcd535;'>
    <div class='kpi-title'>ضریب مصرف ورق</div>
    <div class='kpi-value'>{strip_ratio:.3f}<span class='kpi-unit'>m/m</span></div>
</div>
""", unsafe_allow_html=True)
