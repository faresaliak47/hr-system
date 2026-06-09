import streamlit as st
import pandas as pd
from datetime import date
from database.db import get_db
from database.models import Employee, Attendance
from services.attendance_service import process_attendance, get_attendance_matrix
from components.cards import (section_card, empty_state, info_banner,
                               success_toast, danger_toast, stat_pills)
from components.layout import render_topbar
from components.theme import COLORS, MONTH_NAMES


def show():
    render_topbar("الحضور والغياب", "📅", "الحضور والغياب")
    tab1, tab2, tab3 = st.tabs(["📝 إدخال الحضور", "🗂️ مصفوفة الحضور", "📋 سجلات الحضور"])
    with tab1: _input_attendance()
    with tab2: _attendance_matrix()
    with tab3: _attendance_records()


def _input_attendance():
    section_card("إدخال الحضور اليومي", "📝", COLORS['primary'])
    info_banner(
        "السطر الأول: التاريخ بصيغة DD/MM/YYYY<br>باقي الأسطر: أسماء الموظفين (سطر لكل موظف)<br>يمكن إضافة بادئات مثل «م» أو «أ» قبل الاسم",
        "📋", COLORS['primary']
    )

    sample = f"""{date.today().strftime('%d/%m/%Y')}
م محمد عبدالجواد
م محمد التوني
شريف ابو العزم
شحاته رزق
عادل عربي"""

    text = st.text_area(
        "📋 أدخل بيانات الحضور:",
        placeholder=sample,
        height=200,
        help="السطر الأول تاريخ، ثم الأسماء"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        submitted = st.button("💾 حفظ الحضور", type="primary", use_container_width=True)

    if submitted:
        if not text.strip():
            st.error("الرجاء إدخال بيانات الحضور.")
            return
        with st.spinner("جاري معالجة بيانات الحضور..."):
            try:
                result = process_attendance(text)
            except Exception as e:
                danger_toast(f"خطأ في المعالجة: {e}")
                return

        if result['success']:
            success_toast(f"تم حفظ حضور يوم {result['date']} بنجاح!")

            stat_pills([
                ("✅", "تم الحفظ",        str(result['saved']),         COLORS['success']),
                ("🔁", "مكرر (تجاهل)",   str(result['duplicates']),    COLORS['warning']),
                ("⚠️","غير متطابق",      str(len(result['unmatched'])), COLORS['danger']),
            ])

            if result['matched']:
                with st.expander(f"✅ الموظفون المطابقون ({len(result['matched'])})", expanded=False):
                    cols = st.columns(3)
                    for i, name in enumerate(result['matched']):
                        cols[i % 3].markdown(f"""
<div style="background:{COLORS['success']}12;border:1px solid {COLORS['success']}30;
            border-radius:8px;padding:8px 12px;margin:3px 0;
            font-size:13px;color:{COLORS['success']};font-weight:600;">
  ✓ {name}
</div>""", unsafe_allow_html=True)

            if result['unmatched']:
                with st.expander(f"⚠️ أسماء غير متطابقة ({len(result['unmatched'])})", expanded=True):
                    info_banner("هذه الأسماء لم يتم العثور عليها في قاعدة بيانات الموظفين النشطين.", "⚠️", COLORS['warning'])
                    cols = st.columns(3)
                    for i, name in enumerate(result['unmatched']):
                        cols[i % 3].markdown(f"""
<div style="background:{COLORS['warning']}12;border:1px solid {COLORS['warning']}30;
            border-radius:8px;padding:8px 12px;margin:3px 0;
            font-size:13px;color:{COLORS['warning']};font-weight:600;">
  ⚠ {name}
</div>""", unsafe_allow_html=True)
        else:
            for err in result['errors']:
                danger_toast(err)


def _attendance_matrix():
    section_card("مصفوفة الحضور الشهرية", "🗂️", COLORS['secondary'])

    col1, col2, col3 = st.columns(3)
    month = col1.selectbox(
        "الشهر", list(range(1, 13)),
        index=date.today().month - 1,
        format_func=lambda m: MONTH_NAMES[m - 1]
    )
    year = col2.number_input("السنة", min_value=2020, max_value=2030, value=date.today().year)

    db = get_db()
    try:
        depts = ['الكل'] + sorted([d[0] for d in db.query(Employee.department).distinct() if d[0]])
    finally:
        db.close()

    dept = col3.selectbox("القسم", depts)
    dept_filter = None if dept == 'الكل' else dept

    if st.button("🔄 عرض المصفوفة", type="primary"):
        with st.spinner("جاري تحميل المصفوفة..."):
            try:
                matrix = get_attendance_matrix(int(month), int(year), dept_filter)
            except Exception as e:
                danger_toast(f"خطأ في تحميل المصفوفة: {e}")
                return

        if matrix.empty:
            empty_state("لا توجد بيانات حضور لهذه الفترة", "📅",
                        "أدخل بيانات الحضور من تبويب «إدخال الحضور»")
            return

        day_cols      = [c for c in matrix.columns if c.isdigit()]
        total_present = matrix['إجمالي الحضور'].sum()
        total_possible = len(matrix) * len(day_cols)
        pct = (total_present / total_possible * 100) if total_possible else 0

        stat_pills([
            ("👥", "عدد الموظفين",       str(len(matrix)),     COLORS['primary']),
            ("📅", "أيام الشهر",         str(len(day_cols)),   COLORS['info']),
            ("📊", "نسبة الحضور الكلية", f"{pct:.1f}%",        COLORS['success'] if pct >= 80 else COLORS['warning']),
            ("✅", "إجمالي أيام الحضور", str(int(total_present)), COLORS['success']),
        ])

        st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
        st.dataframe(matrix, use_container_width=True, hide_index=True, height=400)
        success_toast(f"مصفوفة {MONTH_NAMES[int(month)-1]} {int(year)} — {len(matrix)} موظف")


def _attendance_records():
    section_card("سجلات الحضور", "📋", COLORS['info'])

    col1, col2 = st.columns(2)
    start = col1.date_input("من تاريخ", value=date.today().replace(day=1))
    end   = col2.date_input("إلى تاريخ", value=date.today())

    if start > end:
        st.error("تاريخ البداية يجب أن يكون قبل تاريخ النهاية.")
        return

    if st.button("🔍 بحث", type="primary"):
        db = get_db()
        try:
            records = db.query(Attendance).filter(
                Attendance.attendance_date >= start,
                Attendance.attendance_date <= end
            ).order_by(Attendance.attendance_date.desc()).all()

            if not records:
                empty_state("لا توجد سجلات في هذه الفترة", "📅")
                return

            employees = {e.id: e for e in db.query(Employee).all()}
            data = [{
                'اسم الموظف': employees[r.employee_id].name if r.employee_id in employees else 'غير معروف',
                'القسم':      employees[r.employee_id].department if r.employee_id in employees else '—',
                'التاريخ':    str(r.attendance_date),
                'الحالة':     '✅ حاضر' if r.status == 1 else '❌ غائب'
            } for r in records]

            df      = pd.DataFrame(data)
            present = df[df['الحالة'].str.contains('حاضر')].shape[0]

            stat_pills([
                ("✅", "حاضر",   str(present),            COLORS['success']),
                ("❌", "غائب",   str(len(df) - present),  COLORS['danger']),
                ("📋", "الإجمالي", str(len(df)),           COLORS['primary']),
            ])

            st.dataframe(df, use_container_width=True, hide_index=True)
        except Exception as e:
            danger_toast(f"خطأ في تحميل السجلات: {e}")
        finally:
            db.close()
