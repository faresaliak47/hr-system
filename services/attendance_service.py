import re
from datetime import date, datetime
from database.db import get_db
from database.models import Employee, Attendance
import pandas as pd


def normalize_name(name: str) -> str:
    """Remove prefixes and normalize Arabic name for matching."""
    name = name.strip()
    prefixes = ['م ', 'م. ', 'أ. ', 'أ ', 'د. ', 'د ', 'مهندس ', 'دكتور ']
    for p in prefixes:
        if name.startswith(p):
            name = name[len(p):]
    return name.strip()


def parse_attendance_text(text: str):
    """Parse attendance plain text. Returns (date, names_list, errors)."""
    lines = [l.strip() for l in text.strip().splitlines()]
    lines = [l for l in lines if l]
    if not lines:
        return None, [], ['النص فارغ']
    date_line = lines[0]
    att_date = None
    for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y'):
        try:
            att_date = datetime.strptime(date_line, fmt).date()
            break
        except ValueError:
            continue
    if att_date is None:
        return None, [], [f'تنسيق التاريخ غير صحيح: {date_line}']
    names = list(dict.fromkeys([normalize_name(l) for l in lines[1:] if l.strip()]))
    return att_date, names, []


def process_attendance(text: str):
    """Process attendance text and save to DB. Returns result dict."""
    att_date, names, errors = parse_attendance_text(text)
    if errors:
        return {'success': False, 'errors': errors}
    db = get_db()
    try:
        employees = db.query(Employee).filter(Employee.status == 'Active').all()
        emp_map = {normalize_name(e.name): e for e in employees}
        matched = []
        unmatched = []
        saved = 0
        duplicates = 0
        for name in names:
            emp = emp_map.get(name)
            if emp is None:
                for en, ev in emp_map.items():
                    if name in en or en in name:
                        emp = ev
                        break
            if emp:
                existing = db.query(Attendance).filter(
                    Attendance.employee_id == emp.id,
                    Attendance.attendance_date == att_date
                ).first()
                if existing:
                    duplicates += 1
                else:
                    att = Attendance(employee_id=emp.id, attendance_date=att_date, status=1)
                    db.add(att)
                    saved += 1
                matched.append(emp.name)
            else:
                unmatched.append(name)
        db.commit()
        return {
            'success': True,
            'date': att_date,
            'matched': matched,
            'unmatched': unmatched,
            'saved': saved,
            'duplicates': duplicates
        }
    except Exception as e:
        db.rollback()
        return {'success': False, 'errors': [str(e)]}
    finally:
        db.close()


def get_attendance_matrix(month: int, year: int, department: str = None, employee_id: int = None) -> pd.DataFrame:
    """Generate attendance matrix for a given month/year."""
    import calendar
    db = get_db()
    try:
        days_in_month = calendar.monthrange(year, month)[1]
        query = db.query(Employee)
        if department:
            query = query.filter(Employee.department == department)
        if employee_id:
            query = query.filter(Employee.id == employee_id)
        employees = query.filter(Employee.status == 'Active').all()
        if not employees:
            return pd.DataFrame()
        emp_ids = [e.id for e in employees]
        from sqlalchemy import and_
        start_date = date(year, month, 1)
        end_date = date(year, month, days_in_month)
        records = db.query(Attendance).filter(
            Attendance.employee_id.in_(emp_ids),
            Attendance.attendance_date >= start_date,
            Attendance.attendance_date <= end_date
        ).all()
        att_set = {(r.employee_id, r.attendance_date.day): r.status for r in records}
        rows = []
        for emp in employees:
            row = {'كود الموظف': emp.code, 'اسم الموظف': emp.name}
            for d in range(1, days_in_month + 1):
                row[str(d)] = att_set.get((emp.id, d), 0)
            row['إجمالي الحضور'] = sum(att_set.get((emp.id, d), 0) for d in range(1, days_in_month + 1))
            rows.append(row)
        return pd.DataFrame(rows)
    finally:
        db.close()
