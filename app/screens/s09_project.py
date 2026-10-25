"""
Screen 09: Project Workshop
Interactive practical application workbench implementing all 10 required project experiences.
"""
from nicegui import ui
from app.components.header import render_header
from app.components.footer import render_footer
from app.curriculum.loader import get_module
from app.database.connection import get_db
from app.database.crud import record_project_submission
from app.auth.guards import require_auth
import app.navigation.nav as nav

# Import practical application logic engines
from app.projects.smart_calculator import calculate
from app.projects.payroll_system import process_payroll
from app.projects.inventory_tracker import InventoryManager
from app.projects.grade_analyzer import analyze_student_grades
from app.projects.log_analyzer import parse_log_text, DEFAULT_SAMPLE_LOG
from app.projects.banking_system import BankLedgerSystem
from app.projects.customer_crm import CustomerCRM
from app.projects.weather_dashboard import get_weather_data
from app.projects.email_automator import render_email_template
from app.projects.sales_analytics import run_sales_analysis

# Global instances for stateful in-memory demo objects
inv_manager = InventoryManager()
bank_system = BankLedgerSystem()
crm_system = CustomerCRM()

def render_project_screen(initial_module_id: int = 1):
    with get_db() as db:
        auth = require_auth(db, active_route=f"/projects?module={initial_module_id}")
        if not auth:
            return
        user, learner = auth
        learner_id = learner.id
        learner_name = learner.name

    render_header(active_route="/projects")

    with ui.column().classes("w-full max-w-6xl mx-auto px-4 sm:px-6 py-10 gap-8"):
        # Header banner
        with ui.row().classes("w-full justify-between items-end flex-wrap gap-4"):
            with ui.column().classes("gap-1"):
                ui.label("PRACTICAL PROJECT WORKSHOP").classes("text-xs font-semibold uppercase tracking-widest text-[#6E8098]")
                ui.label("Functional Application Implementations").classes("font-serif text-4xl text-[#161616]")
                ui.label("Test and evaluate all 10 required real-world applications designed for Marwadi University evaluation.").classes("text-sm text-[#5E5A55]")

        # Tab navigation for all 8 modules + activities
        tab_titles = [
            (1, "Mod 1: Smart Calculator"),
            (2, "Mod 2: Payroll System"),
            (3, "Mod 3: Inventory & Grades"),
            (4, "Mod 4: Log File Analyzer"),
            (5, "Mod 5: Banking System"),
            (6, "Mod 6: Customer CRM (SQLite)"),
            (7, "Mod 7: Weather API & Email"),
            (8, "Mod 8: Sales Analytics")
        ]

        with ui.tabs().classes("w-full bg-[#EFEAE2] rounded-lg p-1 border border-[#E2DCD2]") as tabs:
            tab_refs = {}
            for m_id, label in tab_titles:
                tab_refs[m_id] = ui.tab(label).classes("text-xs font-medium normal-case")

        # Pick starting tab
        active_tab = tab_refs.get(initial_module_id, tab_refs[1])

        with ui.tab_panels(tabs, value=active_tab).classes("w-full bg-transparent p-0 mt-6"):
            # ==========================================
            # TAB 1: Smart Calculator (Module 1)
            # ==========================================
            with ui.tab_panel(tab_refs[1]):
                with ui.card().classes("pip-card w-full p-8 gap-6"):
                    with ui.row().classes("w-full justify-between items-center"):
                        with ui.column().classes("gap-0.5"):
                            ui.label("MODULE 1 PROJECT").classes("text-[10px] font-bold text-[#6E8098] font-mono uppercase")
                            ui.label("Smart Calculator Engine").classes("font-serif text-2xl text-[#161616]")
                        ui.label("Arithmetic • Scientific • Percentages").classes("text-xs bg-[#EFEAE2] text-[#5E5A55] px-2.5 py-1 rounded")

                    ui.label("Perform mathematical calculations with built-in validation preventing ZeroDivisionError and domain errors.").classes("text-xs text-[#5E5A55]")

                    with ui.row().classes("w-full gap-4 flex-wrap md:flex-nowrap"):
                        num1_in = ui.number("First Operand (Number 1)", value=25.0).classes("flex-1 text-sm")
                        op_select = ui.select(
                            label="Operation",
                            options={
                                "+": "Addition (+)",
                                "-": "Subtraction (-)",
                                "*": "Multiplication (×)",
                                "/": "True Division (/)",
                                "//": "Floor Division (//)",
                                "%": "Modulo (%)",
                                "^": "Power (^)",
                                "sqrt": "Square Root (√)",
                                "discount": "Percentage Discount (%)"
                            },
                            value="+"
                        ).classes("w-56 text-sm")
                        num2_in = ui.number("Second Operand (Number 2)", value=5.0).classes("flex-1 text-sm")

                    calc_result_box = ui.column().classes("w-full bg-[#F5F2EC] border border-[#E2DCD2] rounded p-4 gap-1")
                    with calc_result_box:
                        calc_out = ui.label("Result: Click 'Execute Calculation' below.").classes("font-mono text-sm text-[#161616]")

                    def run_calc():
                        n1 = float(num1_in.value or 0.0)
                        n2 = float(num2_in.value or 0.0)
                        op = op_select.value
                        res = calculate(op, n1, n2)
                        if res["success"]:
                            calc_out.set_text(f"✓ {res['formatted']}")
                            calc_out.classes(replace="text-[#2D6A4F] font-bold")
                            # Record project completion
                            with get_db() as db_session:
                                record_project_submission(db_session, learner_id, 1, "proj-smart-calc", "Smart Calculator", res["formatted"], 5)
                            ui.notify("Calculation executed successfully! Project completed.", color="positive")
                        else:
                            calc_out.set_text(f"✗ {res['error']}")
                            calc_out.classes(replace="text-[#9D3A3A] font-bold")

                    ui.button("Execute Calculation ▶", on_click=run_calc).classes("btn-blue text-xs font-semibold self-start")

            # ==========================================
            # TAB 2: Employee Payroll (Module 2)
            # ==========================================
            with ui.tab_panel(tab_refs[2]):
                with ui.card().classes("pip-card w-full p-8 gap-6"):
                    with ui.row().classes("w-full justify-between items-center"):
                        with ui.column().classes("gap-0.5"):
                            ui.label("MODULE 2 PROJECT").classes("text-[10px] font-bold text-[#6E8098] font-mono uppercase")
                            ui.label("Employee Payroll Processing System").classes("font-serif text-2xl text-[#161616]")
                        ui.label("Overtime 1.5x • Progressive Tax • Deductions").classes("text-xs bg-[#EFEAE2] text-[#5E5A55] px-2.5 py-1 rounded")

                    with ui.row().classes("w-full gap-4 flex-wrap md:flex-nowrap"):
                        emp_name = ui.input("Employee Name", value="Aarav Sharma").classes("flex-1 text-sm")
                        emp_role = ui.select(["Software Engineer", "Systems Architect", "QA Analyst", "Data Scientist"], value="Software Engineer").classes("w-48 text-sm")
                        emp_hours = ui.number("Hours Worked This Week", value=46.0).classes("w-40 text-sm")
                        emp_rate = ui.number("Hourly Rate ($/hr)", value=35.0).classes("w-40 text-sm")

                    payroll_report_card = ui.column().classes("w-full bg-[#F5F2EC] border border-[#E2DCD2] rounded p-5 gap-3")
                    with payroll_report_card:
                        pr_summary = ui.label("Configure employee hours and rate, then click 'Process Payroll'.").classes("text-xs text-[#5E5A55]")

                    def run_payroll():
                        h = float(emp_hours.value or 0.0)
                        r = float(emp_rate.value or 0.0)
                        res = process_payroll(emp_name.value, emp_role.value, h, r)
                        if res["success"]:
                            payroll_report_card.clear()
                            with payroll_report_card:
                                with ui.row().classes("w-full justify-between items-center pb-2 border-b border-[#E2DCD2]"):
                                    ui.label(f"PAYSLIP: {res['employee_name']} ({res['role']})").classes("font-bold text-xs text-[#23342B] font-mono")
                                    ui.label(f"Net Pay: ${res['net_pay']:,.2f}").classes("font-serif text-xl font-bold text-[#2D6A4F]")
                                with ui.row().classes("w-full justify-between text-xs text-[#5E5A55] flex-wrap gap-4"):
                                    ui.label(f"Regular Pay (40 hrs @ ${res['hourly_rate']}): ${res['base_pay']:,.2f}")
                                    ui.label(f"Overtime Pay ({res['overtime_hours']} hrs @ 1.5x): ${res['overtime_pay']:,.2f}")
                                    ui.label(f"Gross Pay: ${res['gross_pay']:,.2f}").classes("font-semibold text-[#161616]")
                                with ui.row().classes("w-full justify-between text-xs text-[#8C857D] flex-wrap gap-4"):
                                    ui.label(f"Income Tax ({res['tax_bracket']}): -${res['tax']:,.2f}")
                                    ui.label(f"Health Insurance: -${res['health_insurance']:,.2f}")
                                    ui.label(f"Pension (5%): -${res['pension_deduction']:,.2f}")
                                    ui.label(f"Total Deductions: -${res['total_deductions']:,.2f}").classes("font-semibold text-[#9D3A3A]")

                            with get_db() as db_session:
                                record_project_submission(db_session, learner_id, 2, "proj-payroll-system", "Employee Payroll System", f"Net Pay: ${res['net_pay']}", 5)
                            ui.notify("Payroll statement processed & recorded!", color="positive")
                        else:
                            ui.notify(res["error"], color="negative")

                    ui.button("Process Payroll Statement ▶", on_click=run_payroll).classes("btn-blue text-xs font-semibold self-start")

            # ==========================================
            # TAB 3: Inventory & Grades (Module 3)
            # ==========================================
            with ui.tab_panel(tab_refs[3]):
                with ui.card().classes("pip-card w-full p-8 gap-6"):
                    with ui.row().classes("w-full justify-between items-center"):
                        with ui.column().classes("gap-0.5"):
                            ui.label("MODULE 3 PROJECT & COMPANION ACTIVITY").classes("text-[10px] font-bold text-[#6E8098] font-mono uppercase")
                            ui.label("Inventory Tracker & Student Grade Analyzer").classes("font-serif text-2xl text-[#161616]")
                        ui.label("Data Structures • Dicts • Sets • Lists").classes("text-xs bg-[#EFEAE2] text-[#5E5A55] px-2.5 py-1 rounded")

                    # Section 1: Inventory Management Tracker
                    ui.label("1. Warehouse Inventory Catalog").classes("font-serif text-lg font-bold text-[#23342B]")
                    inv_metrics = inv_manager.get_summary_metrics()
                    with ui.row().classes("w-full gap-4"):
                        ui.label(f"Total SKUs: {inv_metrics['total_skus']}").classes("text-xs font-mono bg-[#EFEAE2] px-3 py-1 rounded")
                        ui.label(f"Total Valuation: ${inv_metrics['total_valuation']:,.2f}").classes("text-xs font-mono bg-[#EFEAE2] px-3 py-1 rounded font-bold text-[#2D6A4F]")
                        ui.label(f"Reorder Alerts: {inv_metrics['low_stock_count']} items").classes("text-xs font-mono bg-[#EFEAE2] px-3 py-1 rounded text-[#B4692C]")

                    # Inventory Items Table
                    inv_table_container = ui.column().classes("w-full")
                    def render_inv_table():
                        inv_table_container.clear()
                        items = inv_manager.search_items()
                        with inv_table_container:
                            with ui.row().classes("w-full justify-between bg-[#1A1E1C] text-white text-[11px] font-mono p-2.5 rounded-t"):
                                ui.label("SKU").classes("w-24")
                                ui.label("ITEM NAME").classes("flex-1")
                                ui.label("CATEGORY").classes("w-28")
                                ui.label("PRICE").classes("w-20 text-right")
                                ui.label("STOCK").classes("w-24 text-right")
                            for it in items:
                                row_bg = "bg-[#FBF8F3]" if not it["low_stock"] else "bg-[#FFF5F5]"
                                with ui.row().classes(f"w-full justify-between items-center text-xs p-2.5 border-b border-[#E2DCD2] {row_bg}"):
                                    ui.label(it["sku"]).classes("w-24 font-mono font-bold")
                                    ui.label(it["name"]).classes("flex-1")
                                    ui.label(it["category"]).classes("w-28 text-[#5E5A55]")
                                    ui.label(f"${it['price']:.2f}").classes("w-20 text-right font-mono")
                                    stock_text = f"{it['stock']} (Low!)" if it["low_stock"] else str(it["stock"])
                                    stock_color = "text-[#9D3A3A] font-bold" if it["low_stock"] else "text-[#161616]"
                                    ui.label(stock_text).classes(f"w-24 text-right font-mono {stock_color}")
                    render_inv_table()

                    # Add item inputs
                    with ui.row().classes("w-full gap-3 items-end pt-2"):
                        new_sku = ui.input("SKU", value="SKU-006").classes("w-28 text-xs")
                        new_name = ui.input("Item Name", value="Wireless Mouse").classes("flex-1 text-xs")
                        new_cat = ui.input("Category", value="Hardware").classes("w-32 text-xs")
                        new_price = ui.number("Price ($)", value=29.99).classes("w-24 text-xs")
                        new_stock = ui.number("Stock", value=15).classes("w-24 text-xs")
                        def add_inv():
                            inv_manager.add_or_update_item(new_sku.value, new_name.value, new_cat.value, float(new_price.value or 0), int(new_stock.value or 0))
                            render_inv_table()
                            with get_db() as db_session:
                                record_project_submission(db_session, learner_id, 3, "proj-inventory-tracker", "Inventory Management Tracker", f"SKU {new_sku.value} saved", 5)
                            ui.notify("Item saved to inventory!", color="positive")
                        ui.button("+ Add / Update", on_click=add_inv).classes("btn-blue text-xs")

                    # Section 2: Student Grade Analyzer Activity
                    ui.separator().classes("bg-[#E2DCD2] my-2")
                    ui.label("2. Student Grade Analyzer Activity").classes("font-serif text-lg font-bold text-[#23342B]")
                    sample_records = [
                        {"name": "Aarav Sharma", "score": 92.5},
                        {"name": "Priya Patel", "score": 96.0},
                        {"name": "Rohan Mehta", "score": 74.0},
                        {"name": "Sneha Joshi", "score": 88.0},
                        {"name": "Vikram Desai", "score": 62.0}
                    ]
                    grade_res = analyze_student_grades(sample_records)
                    with ui.row().classes("w-full justify-between bg-[#F5F2EC] p-4 rounded border border-[#E2DCD2] flex-wrap gap-4 text-xs"):
                        ui.label(f"Cohort Size: {grade_res['total_students']}")
                        ui.label(f"Class Average: {grade_res['class_average']}%").classes("font-bold text-[#23342B]")
                        ui.label(f"Cohort GPA: {grade_res['cohort_gpa']} / 4.0").classes("font-bold text-[#2D6A4F]")
                        ui.label(f"Top: {grade_res['highest']['name']} ({grade_res['highest']['score']}%)")
                        ui.label(f"Lowest: {grade_res['lowest']['name']} ({grade_res['lowest']['score']}%)")

                    def certify_grade_analyzer():
                        with get_db() as db_session:
                            record_project_submission(
                                db_session, learner_id, 3, "proj-grade-analyzer",
                                "Student Grade Analyzer",
                                f"Validated {grade_res['total_students']} records; average {grade_res['class_average']}%",
                                len(get_module(3).lessons),
                            )
                        ui.notify("Grade Analyzer evidence recorded.", color="positive")

                    ui.button("Validate Grade Analyzer Evidence ✓", on_click=certify_grade_analyzer).classes("btn-blue text-xs self-start")

            # ==========================================
            # TAB 4: Log File Analyzer (Module 4)
            # ==========================================
            with ui.tab_panel(tab_refs[4]):
                with ui.card().classes("pip-card w-full p-8 gap-6"):
                    with ui.row().classes("w-full justify-between items-center"):
                        with ui.column().classes("gap-0.5"):
                            ui.label("MODULE 4 PROJECT").classes("text-[10px] font-bold text-[#6E8098] font-mono uppercase")
                            ui.label("Log File Telemetry Analyzer").classes("font-serif text-2xl text-[#161616]")
                        ui.label("File Parsing • Regex • Exception Handling").classes("text-xs bg-[#EFEAE2] text-[#5E5A55] px-2.5 py-1 rounded")

                    ui.label("Paste server or application logs to parse timestamps, extract log levels, detect anomalies, and compute error rates.").classes("text-xs text-[#5E5A55]")

                    log_input = ui.textarea(value=DEFAULT_SAMPLE_LOG.strip()).classes("w-full font-mono text-xs bg-[#1A1E1C] text-[#E8EFEA] p-4 rounded border border-[#2D3330]").props("rows=8")

                    log_report_box = ui.column().classes("w-full bg-[#F5F2EC] border border-[#E2DCD2] rounded p-5 gap-3")
                    with log_report_box:
                        ui.label("Click 'Analyze Log File' to parse entries.").classes("text-xs text-[#5E5A55]")

                    def run_log_analysis():
                        res = parse_log_text(log_input.value)
                        log_report_box.clear()
                        with log_report_box:
                            with ui.row().classes("w-full justify-between items-center pb-2 border-b border-[#E2DCD2]"):
                                ui.label(f"EVENTS AUDITED: {res['valid_events_count']} entries").classes("font-mono font-bold text-xs text-[#23342B]")
                                ui.label(f"Error Rate: {res['error_rate_percentage']}%").classes("font-serif text-lg font-bold text-[#9D3A3A]")
                            with ui.row().classes("w-full gap-4 text-xs font-mono"):
                                ui.label(f"INFO: {res['counts']['INFO']}").classes("text-[#2D6A4F]")
                                ui.label(f"WARNING: {res['counts']['WARNING']}").classes("text-[#B4692C]")
                                ui.label(f"ERROR: {res['counts']['ERROR']}").classes("text-[#9D3A3A] font-bold")
                                ui.label(f"CRITICAL: {res['counts']['CRITICAL']}").classes("text-[#9D3A3A] font-bold")

                            if res["critical_alerts"]:
                                ui.label("CRITICAL ALERT TELEMETRY:").classes("text-[10px] font-bold text-[#9D3A3A] font-mono mt-2")
                                for ca in res["critical_alerts"]:
                                    ui.label(f"[{ca['timestamp']}] {ca['component']}: {ca['message']}").classes("text-xs bg-white p-2 rounded border border-[#E2DCD2] text-[#9D3A3A]")

                        with get_db() as db_session:
                            record_project_submission(db_session, learner_id, 4, "proj-log-analyzer", "Log File Analyzer", f"Audited {res['valid_events_count']} events with error rate {res['error_rate_percentage']}%", 5)
                        ui.notify("Log audit completed and recorded!", color="positive")

                    ui.button("Analyze Log File ▶", on_click=run_log_analysis).classes("btn-blue text-xs font-semibold self-start")

            # ==========================================
            # TAB 5: Banking Management (Module 5)
            # ==========================================
            with ui.tab_panel(tab_refs[5]):
                with ui.card().classes("pip-card w-full p-8 gap-6"):
                    with ui.row().classes("w-full justify-between items-center"):
                        with ui.column().classes("gap-0.5"):
                            ui.label("MODULE 5 PROJECT").classes("text-[10px] font-bold text-[#6E8098] font-mono uppercase")
                            ui.label("Banking Account Management System").classes("font-serif text-2xl text-[#161616]")
                        ui.label("OOP • Inheritance • Ledgers • Encapsulation").classes("text-xs bg-[#EFEAE2] text-[#5E5A55] px-2.5 py-1 rounded")

                    # Live Account Balances Display
                    acc_display = ui.row().classes("w-full gap-4 flex-wrap md:flex-nowrap")
                    def render_bank_accounts():
                        acc_display.clear()
                        with acc_display:
                            for num, acc in bank_system.accounts.items():
                                acc_type = "Savings Account" if "SA" in num else "Checking Account"
                                with ui.card().classes("pip-card flex-1 p-5 gap-2 bg-[#FBF8F3] border border-[#E2DCD2]"):
                                    with ui.row().classes("justify-between items-center"):
                                        ui.label(num).classes("text-xs font-mono font-bold text-[#23342B]")
                                        ui.label(acc_type).classes("text-[10px] text-[#8C857D] font-mono")
                                    ui.label(acc.holder_name).classes("font-serif text-lg text-[#161616]")
                                    ui.label(f"${acc.balance:,.2f}").classes("font-serif text-2xl font-bold text-[#2D6A4F]")
                    render_bank_accounts()

                    # Transaction Actions
                    with ui.row().classes("w-full gap-4 items-end flex-wrap md:flex-nowrap pt-2"):
                        tx_from = ui.select(options={"SA-2401": "SA-2401 (Aarav)", "CA-8802": "CA-8802 (Priya)"}, value="SA-2401", label="From Account").classes("flex-1 text-xs")
                        tx_to = ui.select(options={"CA-8802": "CA-8802 (Priya)", "SA-2401": "SA-2401 (Aarav)"}, value="CA-8802", label="To Account").classes("flex-1 text-xs")
                        tx_amount = ui.number("Transfer Amount ($)", value=100.0).classes("w-44 text-xs")

                        def do_transfer():
                            amt = float(tx_amount.value or 0.0)
                            res = bank_system.transfer(tx_from.value, tx_to.value, amt)
                            if res["success"]:
                                render_bank_accounts()
                                with get_db() as db_session:
                                    record_project_submission(db_session, learner_id, 5, "proj-banking-system", "Banking Account Management System", res["message"], 5)
                                ui.notify(res["message"], color="positive")
                            else:
                                ui.notify(res["error"], color="negative")

                        ui.button("Execute Transfer ▶", on_click=do_transfer).classes("btn-blue text-xs font-semibold")

            # ==========================================
            # TAB 6: Customer CRM (Module 6)
            # ==========================================
            with ui.tab_panel(tab_refs[6]):
                with ui.card().classes("pip-card w-full p-8 gap-6"):
                    with ui.row().classes("w-full justify-between items-center"):
                        with ui.column().classes("gap-0.5"):
                            ui.label("MODULE 6 PROJECT").classes("text-[10px] font-bold text-[#6E8098] font-mono uppercase")
                            ui.label("Customer Record Management Application").classes("font-serif text-2xl text-[#161616]")
                        ui.label("SQLite Backend • Parameterized CRUD • MySQL Path").classes("text-xs bg-[#EFEAE2] text-[#5E5A55] px-2.5 py-1 rounded")

                    # Search and Add Form
                    with ui.row().classes("w-full gap-3 items-end"):
                        search_crm_in = ui.input("Search by Name or Email", placeholder="Filter records...").classes("flex-1 text-xs")
                        add_name = ui.input("Customer Name", value="Kavita Rao").classes("w-40 text-xs")
                        add_email = ui.input("Email", value="kavita@marwadi.edu").classes("w-48 text-xs")
                        add_tier = ui.select(["Standard", "Premium", "Enterprise"], value="Premium").classes("w-32 text-xs")

                        def add_crm_cust():
                            res = crm_system.create_customer(add_name.value, add_email.value, tier=add_tier.value)
                            if res["success"]:
                                render_crm_table()
                                with get_db() as db_session:
                                    record_project_submission(db_session, learner_id, 6, "proj-customer-crm", "Customer CRM Application", res["message"], 5)
                                ui.notify(res["message"], color="positive")
                            else:
                                ui.notify(res["error"], color="negative")

                        ui.button("+ Register", on_click=add_crm_cust).classes("btn-blue text-xs")

                    crm_table_box = ui.column().classes("w-full")
                    def render_crm_table():
                        crm_table_box.clear()
                        customers = crm_system.list_customers(search_crm_in.value)
                        with crm_table_box:
                            with ui.row().classes("w-full justify-between bg-[#1A1E1C] text-white text-[11px] font-mono p-2.5 rounded-t"):
                                ui.label("ID").classes("w-12")
                                ui.label("NAME").classes("w-44")
                                ui.label("EMAIL").classes("flex-1")
                                ui.label("TIER").classes("w-28")
                                ui.label("ACTIONS").classes("w-24 text-right")
                            for c in customers:
                                with ui.row().classes("w-full justify-between items-center text-xs p-2.5 border-b border-[#E2DCD2] bg-[#FBF8F3]"):
                                    ui.label(f"#{c['id']}").classes("w-12 font-mono text-[#8C857D]")
                                    ui.label(c["name"]).classes("w-44 font-semibold")
                                    ui.label(c["email"]).classes("flex-1 text-[#5E5A55]")
                                    ui.label(c["tier"]).classes("w-28 font-mono text-xs text-[#23342B]")
                                    del_btn = ui.button("Delete").props("flat size=sm").classes("text-[#9D3A3A] text-xs")
                                    del_btn.on_click(lambda cid=c["id"]: [crm_system.delete_customer(cid), render_crm_table(), ui.notify(f"Customer #{cid} deleted.")])
                    render_crm_table()
                    search_crm_in.on_value_change(lambda: render_crm_table())

            # ==========================================
            # TAB 7: Weather API & Email (Module 7)
            # ==========================================
            with ui.tab_panel(tab_refs[7]):
                with ui.card().classes("pip-card w-full p-8 gap-6"):
                    with ui.row().classes("w-full justify-between items-center"):
                        with ui.column().classes("gap-0.5"):
                            ui.label("MODULE 7 PROJECT & COMPANION TOOL").classes("text-[10px] font-bold text-[#6E8098] font-mono uppercase")
                            ui.label("Weather API Dashboard & Email Automation Tool").classes("font-serif text-2xl text-[#161616]")
                        ui.label("REST APIs • JSON Ingestion • MIME Templates").classes("text-xs bg-[#EFEAE2] text-[#5E5A55] px-2.5 py-1 rounded")

                    # Section 1: Weather API Dashboard
                    ui.label("1. Meteorological REST Ingestion").classes("font-serif text-lg font-bold text-[#23342B]")
                    with ui.row().classes("items-end gap-3"):
                        city_in = ui.select(
                            options=["Rajkot", "Ahmedabad", "Mumbai", "Delhi", "London", "Tokyo", "San Francisco"],
                            value="Rajkot",
                            label="Target City"
                        ).classes("w-60 text-xs")
                        weather_card = ui.column().classes("w-full bg-[#F5F2EC] border border-[#E2DCD2] rounded p-5 gap-2")

                    def update_weather():
                        w = get_weather_data(city_in.value)
                        weather_card.clear()
                        with weather_card:
                            with ui.row().classes("w-full justify-between items-center"):
                                with ui.column().classes("gap-0"):
                                    ui.label(w["city"]).classes("font-serif text-2xl text-[#161616]")
                                    ui.label(f"Source: {w['source']}").classes("text-[10px] font-mono text-[#8C857D]")
                                ui.label(f"{w['temperature_c']}°C").classes("font-serif text-3xl font-bold text-[#23342B]")
                            with ui.row().classes("w-full gap-4 text-xs text-[#5E5A55]"):
                                ui.label(f"Wind Velocity: {w['wind_speed_kmh']} km/h")
                                ui.label(f"Humidity: {w['humidity_pct']}%")
                                ui.label(f"Condition: {w['condition']}")

                        with get_db() as db_session:
                            record_project_submission(db_session, learner_id, 7, "proj-weather-dashboard", "Weather API Dashboard", f"{w['city']}: {w['temperature_c']}°C", 5)

                    update_weather()
                    city_in.on_value_change(lambda: update_weather())

                    # Section 2: Email Automation Tool
                    ui.separator().classes("bg-[#E2DCD2] my-2")
                    ui.label("2. Email Automation Tool (MIME Template Generator)").classes("font-serif text-lg font-bold text-[#23342B]")
                    email_preview_box = ui.column().classes("w-full bg-[#1A1E1C] text-[#E8EFEA] font-mono text-xs p-4 rounded border border-[#2D3330] gap-1")
                    
                    email_res = render_email_template("PROGRESS_ALERT", learner_name, "student@marwadi.edu")
                    with email_preview_box:
                        ui.label(f"To: {email_res['to']}").classes("text-[#A3E635]")
                        ui.label(f"Subject: {email_res['subject']}").classes("text-[#DCC9A3] font-bold")
                        ui.label(f"Status: {email_res['safe_mode']}").classes("text-[#8C857D]")
                        ui.label("-" * 50).classes("text-[#2D3330]")
                        ui.label(email_res["body"]).classes("whitespace-pre-wrap text-[#E8EFEA]")

                    def certify_email_preview():
                        with get_db() as db_session:
                            record_project_submission(
                                db_session, learner_id, 7, "proj-email-automation",
                                "Email Automation Tool",
                                f"Safe preview rendered for {email_res['to']}; no email sent",
                                len(get_module(7).lessons),
                            )
                        ui.notify("Safe email preview evidence recorded; nothing was sent.", color="positive")

                    ui.button("Record Safe Preview Evidence ✓", on_click=certify_email_preview).classes("btn-blue text-xs self-start")

            # ==========================================
            # TAB 8: Sales Analytics (Module 8)
            # ==========================================
            with ui.tab_panel(tab_refs[8]):
                with ui.card().classes("pip-card w-full p-8 gap-6"):
                    with ui.row().classes("w-full justify-between items-center"):
                        with ui.column().classes("gap-0.5"):
                            ui.label("MODULE 8 CAPSTONE PROJECT").classes("text-[10px] font-bold text-[#6E8098] font-mono uppercase")
                            ui.label("Sales Analytics Dashboard").classes("font-serif text-2xl text-[#161616]")
                        ui.label("Pandas DataFrames • Matplotlib • Groupby").classes("text-xs bg-[#EFEAE2] text-[#5E5A55] px-2.5 py-1 rounded")

                    analytics_data = run_sales_analysis()

                    with ui.row().classes("w-full gap-4 flex-wrap md:flex-nowrap"):
                        ui.label(f"Total Revenue: ${analytics_data['total_revenue']:,.2f}").classes("text-xs font-mono bg-[#EFEAE2] px-3 py-1.5 rounded font-bold text-[#2D6A4F]")
                        ui.label(f"Total Units Sold: {analytics_data['total_units']}").classes("text-xs font-mono bg-[#EFEAE2] px-3 py-1.5 rounded")
                        ui.label(f"Top Category: {analytics_data['top_category']}").classes("text-xs font-mono bg-[#EFEAE2] px-3 py-1.5 rounded text-[#23342B] font-bold")
                        ui.label(f"Top Region: {analytics_data['top_region']}").classes("text-xs font-mono bg-[#EFEAE2] px-3 py-1.5 rounded")

                    # Display Matplotlib Rendered Chart Base64
                    with ui.element("div").classes("w-full bg-[#FBF8F3] border border-[#E2DCD2] rounded-lg p-4 flex justify-center"):
                        ui.image(f"data:image/png;base64,{analytics_data['chart_png_base64']}").classes("max-w-full h-auto rounded")

                    def confirm_analytics():
                        with get_db() as db_session:
                            record_project_submission(db_session, learner_id, 8, "proj-sales-analytics", "Sales Analytics Dashboard", f"Generated visual analytics. Revenue: ${analytics_data['total_revenue']}", 5)
                        ui.notify("Sales Analytics milestone confirmed & recorded!", color="positive")

                    ui.button("Confirm & Record Capstone Analytics ▶", on_click=confirm_analytics).classes("btn-blue text-xs font-semibold self-start")

    render_footer()
