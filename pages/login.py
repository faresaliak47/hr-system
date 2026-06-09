"""Login page for HR Pro authentication."""
import streamlit as st
from services.auth import login
from components.theme import COLORS


def show_login():
    """Render the login page — no default credentials shown."""
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown(f"""
<div style="text-align:center;padding:32px 0 24px;">
  <div style="background:linear-gradient(135deg,{COLORS['primary']},{COLORS['primary_light']});
              border-radius:20px;width:72px;height:72px;
              display:flex;align-items:center;justify-content:center;
              font-size:34px;margin:0 auto 16px;
              box-shadow:0 8px 24px {COLORS['primary']}55;">👥</div>
  <div style="font-size:24px;font-weight:900;color:{COLORS['text']};letter-spacing:-0.5px;">HR Pro</div>
  <div style="font-size:13px;color:{COLORS['text_muted']};margin-top:4px;">نظام إدارة الموارد البشرية</div>
</div>
""", unsafe_allow_html=True)

        st.markdown(f"""
<div style="background:{COLORS['surface']};border-radius:16px;padding:28px 24px 8px;
            border:1px solid {COLORS['border']};box-shadow:0 4px 24px {COLORS['shadow']};
            margin-bottom:16px;">
  <div style="font-size:16px;font-weight:700;color:{COLORS['text']};margin-bottom:16px;text-align:center;">
    🔐 تسجيل الدخول
  </div>
</div>
""", unsafe_allow_html=True)

        with st.form("login_form"):
            username  = st.text_input("اسم المستخدم", placeholder="أدخل اسم المستخدم")
            password  = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور")
            submitted = st.form_submit_button("🔑 دخول", type="primary", use_container_width=True)

            if submitted:
                if not username.strip() or not password:
                    st.error("يرجى إدخال اسم المستخدم وكلمة المرور.")
                elif login(username.strip(), password):
                    st.success(f"أهلاً {st.session_state.get('full_name', username)}! 👋")
                    st.rerun()
                else:
                    st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة.")
