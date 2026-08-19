import streamlit as st
from core_logic import PipeSpecifications

# تنظیمات پایه
st.set_page_config(
    page_title="سیستم مانیتورینگ کارخانه لوله‌سازی اسپیرال",
    page_icon="⚙️",
    layout="wide"
)

# CSS اختصاصی برای رنگ‌بندی استاندارد، متراکم و کاملاً خوانا
st.markdown("""
<style>
    /* تنظیم فونت و رنگ‌های استاندارد صنعتی */
    html, body, [class*="css"] {
        font-family: 'Tahoma', 'Segoe UI', sans-serif;
    }
    
    .main-title {
        text-align: center;
        color: #1a252c;
        font-weight: 800;
        font-size: 1.8rem;
        margin-bottom: 5px;
    }
    
    .sub-title {
        text-align: center;
        color: #5a6a85;
        font-size: 0.95rem;
        margin-bottom: 20px;
    }

    /* کارت‌های شاخص مهندسی (KPI) */
    .kpi-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-right: 4px solid #0284c7;
        border-radius: 8px;
        padding: 12px 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    .kpi-title { color: #64748b; font-size: 0.8rem; font-weight: 700; margin-bottom: 6px; }
    .kpi-value { color: #0f172a; font-size: 1.35rem; font-weight: 800; font-family: monospace; }
    .kpi-unit { color: #0284c7; font-size: 0.85rem; font-weight: 600; margin-left: 2px; }
</style>
""", unsafe_allow_html=True)

# سربرگ برنامه
st.markdown("<div class='main-title'>🏭 مرکز مانیتورینگ و کنترل خطوط اسپیرال</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>تنظیمات پایه و محاسبات هندسی محض</div>", unsafe_allow_html=True)

# پانل ورودی‌های ثابت (فشرده و استاندارد)
with st.expander("🛠️ تنظیمات پارامترهای ثابت خط", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        D = st.number_input("قطر خارجی (D - mm)", value=1800.0, step=10.0, key="D_val")
        t = st.number_input("ضخامت ورق (t - mm)", value=14.2, step=0.1, key="t_val")
        W = st.number_input("عرض ورق (W - mm)", value=1500.0, step=10.0, key="W_val")
        L = st.number_input("طول شاخه استاندارد (L - mm)", value=12020.0, step=10.0, key="L_val")
        
    with col2:
        limit = st.number_input("حد مجاز T (Limit - mm)", value=300.0, step=10.0, key="Limit_val")
        default_lead = st.number_input("پیش‌فرض پرت سر کلاف (mm)", value=400.0, step=10.0, key="lead_val")
        default_tail = st.number_input("پیش‌فرض پرت ته کلاف (mm)", value=300.0, step=10.0, key="tail_val")

# فراخوانی کلاس محاسباتی
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

# نمایش کارت‌های خروجی
st.markdown("##### 📊 خروجی‌های محاسباتی هندسی")
k1, k2, k3, k4, k5 = st.columns(5)

k1.markdown(f"""
<div class='kpi-card' style='border-right-color: #10b981;'>
    <div class='kpi-title'>زاویه هلیکس (α)</div>
    <div class='kpi-value'>{specs.helix_angle_deg:.2f}<span class='kpi-unit'>°</span></div>
</div>
""", unsafe_allow_html=True)

k2.markdown(f"""
<div class='kpi-card'>
    <div class='kpi-title'>محیط متوسط (C)</div>
    <div class='kpi-value'>{specs.perimeter:.1f}<span class='kpi-unit'>mm</span></div>
</div>
""", unsafe_allow_html=True)

k3.markdown(f"""
<div class='kpi-card'>
    <div class='kpi-title'>گام جوش (P)</div>
    <div class='kpi-value'>{specs.weld_pitch:.1f}<span class='kpi-unit'>mm</span></div>
</div>
""", unsafe_allow_html=True)

k4.markdown(f"""
<div class='kpi-card'>
    <div class='kpi-title'>قطر متوسط (D_m)</div>
    <div class='kpi-value'>{specs.mean_diameter:.1f}<span class='kpi-unit'>mm</span></div>
</div>
""", unsafe_allow_html=True)

strip_ratio = specs.pipe_length_to_strip_length(1000.0) / 1000.0
k5.markdown(f"""
<div class='kpi-card' style='border-right-color: #f59e0b;'>
    <div class='kpi-title'>ضریب مصرف ورق</div>
    <div class='kpi-value'>{strip_ratio:.3f}<span class='kpi-unit'>m/m</span></div>
</div>
""", unsafe_allow_html=True)
