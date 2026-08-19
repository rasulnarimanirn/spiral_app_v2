import streamlit as st
from core_logic import PipeSpecifications

# تنظیمات اولیه صفحه
st.set_page_config(
    page_title="سیستم مانیتورینگ خط لوله‌سازی اسپیرال",
    page_icon="⚙️",
    layout="wide"
)

# --- منوی جانبی (Sidebar): ورودی‌های ثابت پروژه ---
st.sidebar.header("⚙️ مشخصات پایه پروژه")

outer_diameter = st.sidebar.number_input("قطر خارجی (D - mm)", value=1800.0, step=10.0)
wall_thickness = st.sidebar.number_input("ضخامت ورق (t - mm)", value=14.2, step=0.1)
strip_width = st.sidebar.number_input("عرض ورق (W - mm)", value=1500.0, step=10.0)
standard_length = st.sidebar.number_input("طول شاخه استاندارد (L - mm)", value=12020.0, step=10.0)
t_joint_limit = st.sidebar.number_input("حد مجاز فاصله T (mm)", value=300.0, step=10.0)
steel_grade = st.sidebar.selectbox("گرید فولاد", ["API 5L X52", "API 5L X60", "ST37", "ST52"])

# فراخوانی موتور محاسباتی
pipe = PipeSpecifications(
    outer_diameter=outer_diameter,
    wall_thickness=wall_thickness,
    strip_width=strip_width,
    standard_length=standard_length,
    t_joint_limit=t_joint_limit
)

# --- صفحه اصلی: داشبورد مانیتورینگ ---
st.title("🖥️ مانیتورینگ خط تولید لوله اسپیرال")
st.caption(f"گرید فعال: **{steel_grade}** | محاسبه هندسی محض بر اساس استاندارد کارخانه‌ای")

st.divider()

# نمایش خروجی‌های اصلی در کارت‌های درشت و برجسته (KPI Metrics)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="زاویه هلیکس (α)", value=f"{pipe.helix_angle_deg:.2f}°")

with col2:
    st.metric(label="محیط متوسط (C)", value=f"{pipe.perimeter:.1f} mm")

with col3:
    st.metric(label="گام جوش (P)", value=f"{pipe.weld_pitch:.1f} mm")

with col4:
    st.metric(label="قطر متوسط (D_m)", value=f"{pipe.mean_diameter:.1f} mm")

st.divider()

# فضای باز و خلوت برای بخش‌های بعدی (کلاف جاری، T-Joint و ضایعات)
st.subheader("📊 وضعیت کلاف جاری")
st.info("این بخش در گام‌های بعدی برای مانیتورینگ کلاف استارت و پیش‌بینی‌ها تکمیل خواهد شد.")
