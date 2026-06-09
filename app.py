import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from database.db import init_db, get_db
from database.models import Employee, Attendance, Overtime, Advance, User
from services.auth import is_logged_in, logout, needs_setup, can_access, ROLE_LABELS
from datetime import date, timedelta
import random

# ── Page config ─────────────────────────────────────────────
st.set_page_config(
    page_title='Odoo Mini HR Pro',
    page_icon='👥',
    layout='wide',
    initial_sidebar_state='expanded'
)

from components.theme import inject_global_css
inject_global_css()

# ── Init DB (seed handled inside db layer now) ─────────────
init_db()

# ─────────────────────────────────────────────
# SESSION HELPERS
# ─────────────────────────────────────────────
import hashlib

_APP_SECRET = "hrpro-session-v1"


def _make_token(user_id: int, secret: str) -> str:
    return hashlib.sha256(f"{user_id}:{secret}".encode()).hexdigest()[:24]


def _restore_session_if_needed():
    if st.session_state.get('logged_in'):
        return

    params = st.query_params
    token = params.get("_sid", "")
    uid = params.get("_uid", "")

    if not token or not uid:
        return

    try:
        user_id = int(uid)
    except ValueError:
        return

    expected = _make_token(user_id, _APP_SECRET)

    if token != expected:
        st.query_params.clear()
        return

    db = get_db()
    try:
        user = db.query(User).filter(
            User.id == user_id,
            User.is_active == True
        ).first()

        if user:
            st.session_state.update({
                "logged_in": True,
                "user_id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "user_role": user.role
            })
    finally:
        db.close()


def _write_session_token():
    user_id = st.session_state.get('user_id')
    if not user_id:
        return

    token = _make_token(user_id, _APP_SECRET)
    st.query_params["_sid"] = token
    st.query_params["_uid"] = str(user_id)


def _clear_session_token():
    st.query_params.clear()


# ─────────────────────────────────────────────
# IMPORTANT: DO NOT SEED HERE ANYMORE
# ─────────────────────────────────────────────
# ❌ seed_data() REMOVED FROM HERE
# (Handled inside init_db safely)


_restore_session_if_needed()

# ── Setup wizard ─────────────────────────────
if needs_setup():
    from pages.setup_wizard import show_setup_wizard
    show_setup_wizard()
    st.stop()

# ── Auth ─────────────────────────────────────
if not is_logged_in():
    from pages.login import show_login
    show_login()
    st.stop()

_write_session_token()

# ── Sidebar + Routing ────────────────────────
from components.layout import render_sidebar, NAV_LABELS, NAV_ITEMS
from components.theme import COLORS

selected = render_sidebar(
    extra_items=[("⚙️", "إدارة المستخدمين", "user_management")]
    if can_access('user_management') else []
)

with st.sidebar:
    st.markdown("<div style='height:60px;'></div>", unsafe_allow_html=True)

    role_label = ROLE_LABELS.get(
        st.session_state.get('user_role', 'viewer'),
        '👁️ مشاهد'
    )

    st.markdown(f"""
    <div style="padding:10px 16px;font-size:11px;color:#9a7daa;text-align:center;">
      {role_label}
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 تسجيل الخروج", use_container_width=True):
        _clear_session_token()
        logout()
        st.rerun()


# ─────────────────────────────────────────────
# ROUTING
# ─────────────────────────────────────────────
PAGE_KEYS = [item[2] for item in NAV_ITEMS]


def page_allowed(idx: int) -> bool:
    return can_access(PAGE_KEYS[idx])


if selected == NAV_LABELS[0]:
    from pages import dashboard; dashboard.show()

elif selected == NAV_LABELS[1]:
    if page_allowed(1):
        from pages import employees; employees.show()
    else:
        st.warning("⛔ ليس لديك صلاحية الوصول لهذا القسم.")

elif selected == NAV_LABELS[2]:
    if page_allowed(2):
        from pages import attendance; attendance.show()
    else:
        st.warning("⛔ ليس لديك صلاحية الوصول لهذا القسم.")

elif selected == NAV_LABELS[3]:
    if page_allowed(3):
        from pages import overtime; overtime.show()
    else:
        st.warning("⛔ ليس لديك صلاحية الوصول لهذا القسم.")

elif selected == NAV_LABELS[4]:
    if page_allowed(4):
        from pages import advances; advances.show()
    else:
        st.warning("⛔ ليس لديك صلاحية الوصول لهذا القسم.")

elif selected == NAV_LABELS[5]:
    if page_allowed(5):
        from pages import payroll; payroll.show()
    else:
        st.warning("⛔ ليس لديك صلاحية الوصول لهذا القسم.")

elif selected == NAV_LABELS[6]:
    if page_allowed(6):
        from pages import reports; reports.show()
    else:
        st.warning("⛔ ليس لديك صلاحية الوصول لهذا القسم.")

elif selected and "إدارة المستخدمين" in selected:
    if can_access('user_management'):
        from pages import user_management; user_management.show()
    else:
        st.warning("⛔ ليس لديك صلاحية الوصول لهذا القسم.")