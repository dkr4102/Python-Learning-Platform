"""
Automated unit tests for all 10 required practical applications.
"""
from app.projects.smart_calculator import calculate
from app.projects.payroll_system import process_payroll
from app.projects.inventory_tracker import InventoryManager
from app.projects.grade_analyzer import analyze_student_grades
from app.projects.log_analyzer import parse_log_text
from app.projects.banking_system import BankLedgerSystem
from app.projects.customer_crm import CustomerCRM
from app.projects.weather_dashboard import get_weather_data
from app.projects.email_automator import render_email_template
from app.projects.sales_analytics import run_sales_analysis

def test_smart_calculator_operations():
    assert calculate("+", 10, 5)["result"] == 15.0
    assert calculate("*", 4, 3)["result"] == 12.0
    assert calculate("sqrt", 16)["result"] == 4.0
    assert calculate("discount", 100, 15)["result"] == 85.0
    # Zero division safeguard
    div_zero = calculate("/", 10, 0)
    assert div_zero["success"] is False
    assert "ZeroDivisionError" in div_zero["error"]

def test_payroll_system():
    res = process_payroll("Aarav Sharma", "Engineer", 45.0, 30.0)
    assert res["success"] is True
    assert res["base_pay"] == 1200.0  # 40 * 30
    assert res["overtime_hours"] == 5.0
    assert res["overtime_pay"] == 225.0  # 5 * (30 * 1.5)
    assert res["gross_pay"] == 1425.0
    assert res["net_pay"] > 0

def test_inventory_and_grades():
    inv = InventoryManager()
    add_res = inv.add_or_update_item("SKU-999", "Test Widget", "Hardware", 19.99, 10)
    assert add_res["success"] is True
    metrics = inv.get_summary_metrics()
    assert metrics["total_skus"] >= 5

    grades = analyze_student_grades([{"name": "Aarav", "score": 90}, {"name": "Priya", "score": 80}])
    assert grades["success"] is True
    assert grades["class_average"] == 85.0

def test_log_file_analyzer():
    sample = "2026-10-24 10:00:00 [ERROR] DB: Connection refused.\n2026-10-24 10:00:05 [INFO] Web: 200 OK."
    res = parse_log_text(sample)
    assert res["valid_events_count"] == 2
    assert res["counts"]["ERROR"] == 1
    assert res["counts"]["INFO"] == 1
    assert len(res["critical_alerts"]) == 1

def test_banking_ledger_system():
    bank = BankLedgerSystem()
    res = bank.transfer("SA-2401", "CA-8802", 200.0)
    assert res["success"] is True
    assert bank.accounts["SA-2401"].balance == 1300.0
    assert bank.accounts["CA-8802"].balance == 1050.0

def test_customer_crm_crud():
    crm = CustomerCRM(db_path=":memory:")
    c_id = crm.create_customer("Test User", "test@marwadi.edu", "+91 90000 00000", "Standard")
    assert c_id["success"] is True
    customers = crm.list_customers("Test")
    assert len(customers) >= 1
    upd = crm.update_customer(customers[0]["id"], "Test User Upd", "test@marwadi.edu", "+91 90000 00000", "Premium")
    assert upd["success"] is True

def test_weather_and_email_automation():
    weather = get_weather_data("Rajkot")
    assert "temperature_c" in weather
    assert "city" in weather

    email = render_email_template("PROGRESS_ALERT", "Aarav", "aarav@marwadi.edu")
    assert email["success"] is True
    assert "PROGRESS REPORT" in email["subject"].upper()
    assert "raw_mime" in email

def test_sales_analytics():
    analysis = run_sales_analysis()
    assert analysis["success"] is True
    assert analysis["total_revenue"] > 0
    assert len(analysis["chart_png_base64"]) > 100
