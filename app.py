import streamlit as st
from core_logic import PipeSpecifications, FactoryManager

# تنظیمات پایه صفحه
st.set_page_config(
    page_title="سیستم مانیتورینگ کارخانه لوله‌سازی اسپیرال",
    page_icon="⚙️",
    layout="wide"
)

# ایجاد شیء مدیریت کارخانه در حافظه برنامه (Session State)
if "factory" not in st.session_state:
    st.session_state.factory = FactoryManager()

st.title("🖥️ مدیریت و مانیتورینگ خطوط تولید اسپیرال")
st.caption("سیستم جامع محاسبات هندسی و کنترل تولید - مدیریت ۳ خط هم‌زمان")

# ایجاد تب‌های مجزا برای ۳ خط تولید
tab_line1, tab_line2, tab_line3 = st.tabs(["🔴 خط تولید ۱", "🔵 خط تولید ۲", "🟢 خط تولید ۳"])

lines_config = [
    {"tab": tab_line1, "name": "خط تولید ۱", "default_D": 1800.0, "default_t": 14.2, "default_W": 1500.0},
    {"tab": tab_line2, "name": "خط تولید ۲", "default_D": 1200.0, "default_t": 10.0, "default_W": 1250.0},
    {"tab": tab_line3, "name": "خط تولید ۳", "default_D": 600.0, "default_t": 6.0, "default_W": 1000.0},
]

for config in lines_config:
    with config["tab"]:
        st.subheader(f"تنظیمات و وضعیت {config['name']}")
        
        # بخش ورودی‌های هر خط در ۲ ستون خلوت
        col_in1, col_in2 = st.columns(2)
        
        with col_in1:
            outer_diameter = st.number_input(
                f"قطر خارجی (D - mm) - {config['name']}",
                value=config["default_D"],
                step=10.0,
                key=f"D_{config['name']}"
            )
            wall_thickness = st.number_input(
                f"ضخامت ورق (t - mm) - {config['name']}",
                value=config["default_t"],
                step=0.1,
                key=f"t_{config['name']}"
            )
            strip_width = st.number_input(
                f"عرض ورق (W - mm) - {config['name']}",
                value=config["default_W"],
                step=10.0,
                key=f"W_{config['name']}"
            )

        with col_in2:
            standard_length = st.number_input(
                f"طول شاخه استاندارد (L - mm) - {config['name']}",
                value=12020.0,
                step=10.0,
                key=f"L_{config['name']}"
            )
            t_joint_limit = st.number_input(
                f"حد مجاز فاصله T (mm) - {config['name']}",
                value=300.0,
                step=10.0,
                key=f"Limit_{config['name']}"
            )
            steel_grade = st.selectbox(
                f"گرید فولاد - {config['name']}",
                ["API 5L X52", "API 5L X60", "ST37", "ST52"],
                key=f"Grade_{config['name']}"
            )

        # ثبت مشخصات خط در مدیریت کارخانه
        specs = PipeSpecifications(
            outer_diameter=outer_diameter,
            wall_thickness=wall_thickness,
            strip_width=strip_width,
            standard_length=standard_length,
            t_joint_limit=t_joint_limit
        )
        st.session_state.factory.update_or_create_line(config["name"], specs)

        st.divider()

        # نمایش خروجی‌های هندسی خط در کارت‌های شاخص درشت
        st.markdown("### 📐 خروجی‌های هندسی و زاویه هلیکس")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        with kpi1:
            st.metric("زاویه هلیکس (α)", f"{specs.helix_angle_deg:.2f}°")

        with kpi2:
            st.metric("محیط متوسط (C)", f"{specs.perimeter:.1f} mm")

        with kpi3:
            st.metric("گام جوش (P)", f"{specs.weld_pitch:.1f} mm")

        with kpi4:
            st.metric("قطر متوسط (D_m)", f"{specs.mean_diameter:.1f} mm")

        st.divider()
        st.info(f"اطلاعات {config['name']} ثبت شد. در گام بعدی بخش مانیتورینگ کلاف جاری و ضایعات این خط اضافه می‌شود.")
