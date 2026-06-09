import streamlit as st
import pandas as pd
from datetime import date
from database.db import get_db
from database.models import Employee, Overtime
from components.cards import section_card, empty_state, success_toast, danger_toast, stat_pills, warning_toast
from components.layout import render_topbar
from components.theme import COLORS


def show():
    render_topbar("الأوفر تايم", "⏱", "الأوفر تايم")
    tab1, tab2, tab3 = st.tabs(["➕ إضافة أوفر تايم", "📋 السجلات والتقارير", "✏️ تعديل / حذف"])
    with tab1: _add_overtime()
    with tab2: _list_overtime()
    with tab3: _edit_delete_overtime()


def _add_overtime():
    section_card("إضافة سجل أوفر تايم", "➕", COLORS['warning'])
    db = get_db()
    try:
        employees = db.query(Employee).filter(Employee.status == 'Active').all()
        if not employees:
            empty_state("لا يوجد موظفون نشطون", "👥")
            return
        emp_options = {f"{e.code} — {e.name}": e.id for e in employees}
    finally:
        db.close()

    with st.form("add_overtime_form", clear_on_submit=True):
        selected   = st.selectbox("👤 الموظف", list(emp_options.keys()))
        col1, col2 = st.columns(2)
        ot_date    = col1.date_input("📅 التاريخ", value=date.today())
        hours      = col2.number_input("⏱ الساعات", min_value=0.0, max_value=24.0, step=0.5, value=2.0)
        rate       = col1.number_input("💵 معدل الساعة (ج.م)", min_value=0.0, step=5.0, value=50.0)
        amount     = hours * rate
        col2.metric("المبلغ الإجمالي", f"{amount:,.2f} ج.م")
        notes      = st.text_input("📝 ملاحظات", placeholder="اختياري")
        submitted  = st.form_submit_button("💾 حفظ", type="primary", use_container_width=True)
        if submitted:
            if hours <= 0:
                st.error("الساعات يجب أن تكون أكبر من صفر.")
                return
            db2 = get_db()
            try:
                db2.add(Overtime(
                    employee_id=emp_options[selected],
                    date=ot_date, hours=hours,
                    rate_per_hour=rate, amount=hours * rate, notes=notes
                ))
                db2.commit()
                success_toast(f"تم حفظ الأوفر تايم بنجاح. المبلغ: {hours*rate:,.2f} ج.م ✅")
                st.rerun()
            except Exception as e:
                db2.rollback()
                danger_toast(f"خطأ: {e}")
            finally:
                db2.close()


def _list_overtime():
    section_card("سجلات الأوفر تايم", "📋", COLORS['primary'])
    col1, col2 = st.columns(2)
    start = col1.date_input("من تاريخ", value=date.today().replace(day=1))
    end   = col2.date_input("إلى تاريخ", value=date.today())

    if start > end:
        st.error("تاريخ البداية يجب أن يكون قبل تاريخ النهاية.")
        return

    db = get_db()
    try:
        records = db.query(Overtime).filter(
            Overtime.date >= start, Overtime.date <= end
        ).order_by(Overtime.date.desc()).all()

        if not records:
            empty_state("لا توجد سجلات أوفر تايم في هذه الفترة", "⏱")
            return

        employees = {e.id: e for e in db.query(Employee).all()}
        data = [{
            'الموظف':     employees[r.employee_id].name if r.employee_id in employees else '—',
            'القسم':      employees[r.employee_id].department if r.employee_id in employees else '—',
            'التاريخ':    str(r.date),
            'الساعات':    r.hours,
            'معدل الساعة': r.rate_per_hour,
            'الإجمالي':  r.amount,
            'ملاحظات':    r.notes or ''
        } for r in records]
        df = pd.DataFrame(data)

        stat_pills([
            ("📋", "عدد السجلات",   str(len(df)),                       COLORS['primary']),
            ("⏱",  "إجمالي الساعات", f"{df['الساعات'].sum():.1f} ساعة", COLORS['warning']),
            ("💰", "إجمالي المبلغ",  f"{df['الإجمالي'].sum():,.0f} ج.م", COLORS['success']),
        ])
        st.dataframe(df, use_container_width=True, hide_index=True)

        # ── Dept summary chart ─────────────────────────────────────────
        if len(df) > 0:
            dept_sum = df.groupby('القسم')['الإجمالي'].sum().reset_index()
            st.bar_chart(dept_sum.set_index('القسم'))
    except Exception as e:
        danger_toast(f"خطأ في تحميل السجلات: {e}")
    finally:
        db.close()


def _edit_delete_overtime():
    section_card("تعديل / حذف سجل أوفر تايم", "✏️", COLORS['danger'])

    db_r = get_db()
    try:
        records   = db_r.query(Overtime).order_by(Overtime.date.desc()).limit(100).all()
        employees = {e.id: e for e in db_r.query(Employee).all()}
        if not records:
            empty_state("لا توجد سجلات", "⏱")
            return
        options = {
            f"{employees[r.employee_id].name if r.employee_id in employees else '—'} — {r.date} — {r.hours}ساعة": r.id
            for r in records
        }
        rec_map = {r.id: {'emp_id': r.employee_id, 'date': r.date,
                          'hours': float(r.hours), 'rate': float(r.rate_per_hour),
                          'notes': r.notes or ''}
                   for r in records}
        emp_list    = db_r.query(Employee).filter(Employee.status == 'Active').all()
        emp_options = {f"{e.code} — {e.name}": e.id for e in emp_list}
    finally:
        db_r.close()

    selected = st.selectbox("اختر سجلاً", list(options.keys()))
    rec_id   = options[selected]
    rv       = rec_map[rec_id]

    emp_names   = list(emp_options.keys())
    current_emp = next((k for k, v in emp_options.items() if v == rv['emp_id']), emp_names[0] if emp_names else "")

    with st.form("edit_ot_form"):
        sel_emp  = st.selectbox("الموظف", emp_names,
                                index=emp_names.index(current_emp) if current_emp in emp_names else 0)
        col1, col2 = st.columns(2)
        ot_date  = col1.date_input("التاريخ", value=rv['date'])
        hours    = col2.number_input("الساعات", value=rv['hours'], min_value=0.0, step=0.5)
        rate     = col1.number_input("معدل الساعة", value=rv['rate'], min_value=0.0, step=5.0)
        notes    = st.text_input("ملاحظات", value=rv['notes'])
        confirm_del = st.checkbox("⚠️ تأكيد الحذف")
        cs, cd   = st.columns(2)
        save     = cs.form_submit_button("💾 تحديث", type="primary",   use_container_width=True)
        delete   = cd.form_submit_button("🗑️ حذف",  type="secondary", use_container_width=True)

        if save:
            db_w = get_db()
            try:
                obj = db_w.query(Overtime).filter(Overtime.id == rec_id).first()
                if obj:
                    obj.employee_id = emp_options[sel_emp]
                    obj.date = ot_date; obj.hours = hours
                    obj.rate_per_hour = rate; obj.amount = hours * rate; obj.notes = notes
                    db_w.commit()
                    success_toast("تم تحديث السجل بنجاح.")
                    st.rerun()
            except Exception as e:
                db_w.rollback()
                danger_toast(f"خطأ: {e}")
            finally:
                db_w.close()

        if delete:
            if not confirm_del:
                warning_toast("يرجى تأكيد الحذف أولاً.")
            else:
                db_d = get_db()
                try:
                    obj = db_d.query(Overtime).filter(Overtime.id == rec_id).first()
                    if obj:
                        db_d.delete(obj)
                        db_d.commit()
                        success_toast("تم حذف السجل.")
                        st.rerun()
                except Exception as e:
                    db_d.rollback()
                    danger_toast(f"خطأ في الحذف: {e}")
                finally:
                    db_d.close()
