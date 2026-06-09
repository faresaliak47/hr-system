import streamlit as st
from datetime import date
from services.excel_export import export_full_report
from components.cards import section_card, info_banner, success_toast, danger_toast, stat_pills
from components.layout import render_topbar
from components.theme import COLORS, MONTH_NAMES


def show():
    render_topbar("التقارير والتصدير", "📈", "التقارير")

    section_card("تصدير تقرير شامل", "📥", COLORS['primary'])

    col1, col2, col3 = st.columns([2, 2, 1])
    month = col1.selectbox(
        "الشهر", list(range(1, 13)),
        index=date.today().month - 1,
        format_func=lambda m: MONTH_NAMES[m - 1]
    )
    year  = col2.number_input("السنة", min_value=2020, max_value=2030, value=date.today().year)

    # Contents preview — using st.columns instead of raw HTML grid
    section_card("محتويات ملف Excel", "📋", COLORS['info'])
    sheets = [
        ("1️⃣", "الموظفون",        "بيانات جميع الموظفين",             COLORS['primary']),
        ("2️⃣", "سجلات الحضور",   "تفاصيل حضور وغياب الشهر",         COLORS['info']),
        ("3️⃣", "مصفوفة الحضور",  "جدول يومي لكل موظف",              COLORS['secondary']),
        ("4️⃣", "الأوفر تايم",    "ساعات وقيم الوقت الإضافي",        COLORS['warning']),
        ("5️⃣", "السلف",           "سجلات السلف المدفوعة",             COLORS['danger']),
        ("6️⃣", "مسير الرواتب",   "ملخص رواتب مع إجماليات وخصومات",  COLORS['success']),
    ]
    r1, r2 = st.columns(2)
    for i, (num, name, desc, color) in enumerate(sheets):
        col = r1 if i % 2 == 0 else r2
        col.markdown(f"""
<div style="background:{color}08;border-radius:10px;padding:12px 16px;
            border:1px solid {color}22;border-right:3px solid {color};margin-bottom:8px;">
  <div style="font-weight:700;color:{COLORS['text']};font-size:13px;">{num} {name}</div>
  <div style="font-size:11px;color:{COLORS['text_muted']};margin-top:2px;">{desc}</div>
</div>
""", unsafe_allow_html=True)

    with col3:
        st.markdown("<div style='margin-top:26px;'></div>", unsafe_allow_html=True)
        generate = st.button("📥 إنشاء", type="primary", use_container_width=True)

    if generate:
        with st.spinner("جاري إنشاء التقرير الشامل..."):
            try:
                data      = export_full_report(int(month), int(year))
                month_str = str(month).zfill(2)
                filename  = f"HR_Report_{month_str}_{int(year)}.xlsx"

                st.success(f"✅ تم إنشاء التقرير بنجاح! — {filename} — {MONTH_NAMES[int(month)-1]} {int(year)}")

                st.download_button(
                    label=f"⬇️ تحميل {filename}",
                    data=data,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    type="primary"
                )

                stat_pills([
                    ("📊", "الأوراق المُصدَّرة", "6",                                        COLORS['primary']),
                    ("📅", "الفترة",              f"{MONTH_NAMES[int(month)-1]} {int(year)}", COLORS['info']),
                ])

            except Exception as e:
                danger_toast(f"خطأ في إنشاء التقرير: {e}")
