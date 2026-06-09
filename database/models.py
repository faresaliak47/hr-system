from sqlalchemy import Column, Integer, String, Float, Date, Text, UniqueConstraint, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id           = Column(Integer, primary_key=True, autoincrement=True)
    username     = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name    = Column(String(100), nullable=False)
    role         = Column(String(20), default='viewer')   # admin | hr | accountant | viewer
    is_active    = Column(Boolean, default=True)
    created_at   = Column(DateTime, default=datetime.utcnow)


class Employee(Base):
    __tablename__ = 'employees'
    id          = Column(Integer, primary_key=True, autoincrement=True)
    code        = Column(String(20), unique=True, nullable=False)
    name        = Column(String(100), nullable=False)
    job_title   = Column(String(100))
    department  = Column(String(100))
    salary      = Column(Float, default=0.0)
    daily_rate  = Column(Float, default=0.0)
    phone       = Column(String(20))
    national_id = Column(String(20))
    area        = Column(String(100))
    hire_date   = Column(Date)
    status      = Column(String(20), default='Active')


class Attendance(Base):
    __tablename__ = 'attendance'
    id              = Column(Integer, primary_key=True, autoincrement=True)
    employee_id     = Column(Integer, nullable=False)
    attendance_date = Column(Date, nullable=False)
    status          = Column(Integer, default=1)
    __table_args__  = (UniqueConstraint('employee_id', 'attendance_date', name='uq_emp_date'),)


class Overtime(Base):
    __tablename__ = 'overtime'
    id           = Column(Integer, primary_key=True, autoincrement=True)
    employee_id  = Column(Integer, nullable=False)
    date         = Column(Date, nullable=False)
    hours        = Column(Float, default=0.0)
    rate_per_hour = Column(Float, default=0.0)
    amount       = Column(Float, default=0.0)
    notes        = Column(Text)


class Advance(Base):
    __tablename__ = 'advances'
    id          = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, nullable=False)
    date        = Column(Date, nullable=False)
    amount      = Column(Float, default=0.0)
    notes       = Column(Text)


class PayrollCache(Base):
    __tablename__ = 'payroll_cache'
    id              = Column(Integer, primary_key=True, autoincrement=True)
    employee_id     = Column(Integer, nullable=False)
    month           = Column(Integer, nullable=False)
    year            = Column(Integer, nullable=False)
    attendance_days = Column(Integer, default=0)
    daily_rate      = Column(Float, default=0.0)
    base_salary     = Column(Float, default=0.0)
    overtime        = Column(Float, default=0.0)
    advances        = Column(Float, default=0.0)
    net_salary      = Column(Float, default=0.0)
    __table_args__  = (UniqueConstraint('employee_id', 'month', 'year', name='uq_payroll'),)
