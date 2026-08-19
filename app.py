import streamlit as st
from core_logic import PipeSpecifications, FactoryManager

st.set_page_config(
    page_title="سیستم مانیتورینگ کارخانه لوله‌سازی اسپیرال",
    page_icon="⚙️",
    layout="wide"
)

# --- استایل بصری اختصاصی (Industrial Dark UI) ---
st.markdown("""
<style>
    /* پس‌زمینه اصلی و کارت‌ها */
    .main { background-color: #0e1117; }
    
    .stCard {
        background-color: #1e222d;
        border: 1px solid #2e3545;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
    }
    
    /* استایل کارت‌های شاخص مهندسی (KPI) */
    .kpi-box {
        background: linear-gradient(135deg, #1f2430 0%, #161922 100%);
        border-left: 4px solid #00d26a;
        border-radius: 6px;
        padding: 12px 16px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .kpi-title { color: #8a99ad; font-size: 0.85rem; font-weight: bold; margin-bottom: 4px; }
    .kpi-value { color: #ffffff; font-size: 1.5rem; font-weight: 800; font-family: monospace; }
    .kpi-unit { color: #00d26a; font-size: 0.9rem; margin-left: 3px; }
    
    /* هشدار رنگی زاویه هلیکس */
    .helix-badge-ok { background-color: #00d26a1f; color: #00d26a; border: 1px solid #00d26a; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
    .helix-badge-warn { background-color: #fcd5351f; color: #fcd535; border: 1px solid #fcd535; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

if "factory" not in st.session_state:
    st.session_state.factory = FactoryManager()

# سربرگ متراکم صنعتی
st.markdown("<h2 style='text-align: center; color: #f0f2f6; margin-bottom: 0px;'>🏭 مرکز مانیتورینگ و کنترل خطوط اسپیرال</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8a99ad; font-size: 0.9rem;'>سیستم یکپارچه محاسبات هندسی، کلاف جاری و T-Joint</p>", unsafe_allow_html=True)

# تب‌های فشرده خطوط
tab_line1, tab_line2, tab_line3 = st.tabs(["🔴 خط ۱ (سایز سنگین)", "🔵 خط ۲ (سایز متوسط)", "🟢 خط ۳ (سایز سبک)"])

lines_config = [
    {"tab": tab_line1, "name": "خط ۱", "default_D": 1800.0, "default_t": 14.2, "default_W": 1500.0},
    {"tab": tab_line2, "name": "خط ۲", "default_D": 1200.0, "default_t": 10.0, "default_W": 1250.0},
    {"tab": tab_line3, "name": "خط ۳", "default_D": 600.0, "default_t": 6.0, "default_W": 1000.0},
]

for config in lines_config:
    with config["tab"]:
        # پانل ورودی متراکم در یک نوار افقی ۴ تایی (برای جلوگیری از اسکرول)
        with st.expander(f"🛠️ تنظیمات پارامترهای {config['name']} (کلیک برای ویرایش)", expanded=True):
            c1, c2, c3, c4, c5 = st.columns(5)
            D = c1.number_input("قطر (D)", value=config["default_D"], step=10.0, key=f"D_{config['name']}")
            t = c2.number_input("ضخامت (t)", value=config["default_t"], step=0.1, key=f"t_{config['name']}")
            W = c3.number_input("عرض ورق (W)", value=config["default_W"], step=10.0, key=f"W_{config['name']}")
            L = c4.number_input("طول شاخه (L)", value=12020.0, step=10.0, key=f"L_{config['name']}")
            limit = c5.number_input("حد مجاز T", value=300.0, step=10.0, key=f"Limit_{config['name']}")

        specs = PipeSpecifications(outer_diameter=D, wall_thickness=t, strip_width=W, standard_length=L, t_joint_limit=limit)
        st.session_state.factory.update_or_create_line(config["name"], specs)

        # ارزیابی وضعیت زاویه هلیکس
        helix_angle = specs.helix_angle_deg
        is_helix_safe = 40.0 <= helix_angle <= 55.0
        status_html = "<span class='helix-badge-ok'>ایمن / استاندارد</span>" if is_helix_safe else "<span class='helix-badge-warn'>نیازمند بررسی زاویه</span>"

        # داشبورد KPI فشرده با کارت‌های شیشه‌ای صنعتی
        st.markdown(f"#### 📊 داشبورد هندسی {config['name']} | وضعیت: {status_html}", unsafe_allow_html=True)
        
        k1, k2, k3, k4, k5 = st.columns(5)
        
        k1.markdown(f"""
        <div class='kpi-box' style='border-left-color: {"#00d26a" if is_helix_safe else "#fcd535"};'>
            <div class='kpi-title'>زاویه هلیکس (α)</div>
            <div class='kpi-value'>{helix_angle:.2f}<span class='kpi-unit'>°</span></div>
        </div>
        """, unsafe_allow_html=True)

        k2.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-title'>محیط متوسط (C)</div>
            <div class='kpi-value'>{specs.perimeter:.1f}<span class='kpi-unit'>mm</span></div>
        </div>
        """, unsafe_allow_html=True)

        k3.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-title'>گام جوش (P)</div>
            <div class='kpi-value'>{specs.weld_pitch:.1f}<span class='kpi-unit'>mm</span></div>
        </div>
        """, unsafe_allow_html=True)

        k4.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-title'>قطر متوسط (D_m)</div>
            <div class='kpi-value'>{specs.mean_diameter:.1f}<span class='kpi-unit'>mm</span></div>
        </div>
        """, unsafe_allow_html=True)

        # ضریب تبدیل دقیق ورق به لوله (نمایش متریژ واقعی)
        strip_ratio = specs.pipe_length_to_strip_length(1000.0) / 1000.0
        k5.markdown(f"""
        <div class='kpi-box' style='border-left-color: #00b4d8;'>
            <div class='kpi-title'>ضریب مصرف ورق</div>
            <div class='kpi-value'>{strip_ratio:.3f}<span class='kpi-unit'>m/m</span></div>
        </div>
        """, unsafe_allow_html=True)
