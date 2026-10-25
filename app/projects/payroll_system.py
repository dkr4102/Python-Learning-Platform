"""
Project 2: Employee Payroll Processing System
Calculates base salary, overtime premiums, tax brackets, benefits, and net salary.
"""
from typing import Dict, Any

def process_payroll(
    employee_name: str,
    role: str,
    hours_worked: float,
    hourly_rate: float,
    health_insurance: float = 45.0,
    pension_rate: float = 0.05
) -> Dict[str, Any]:
    """
    Compute itemized payroll statement.
    """
    if hours_worked < 0 or hourly_rate < 0:
        return {"success": False, "error": "Hours worked and hourly rate must be non-negative."}

    regular_hours = min(hours_worked, 40.0)
    overtime_hours = max(0.0, hours_worked - 40.0)

    base_pay = regular_hours * hourly_rate
    overtime_rate = hourly_rate * 1.5
    overtime_pay = overtime_hours * overtime_rate
    gross_pay = base_pay + overtime_pay

    # Progressive tax calculation
    # Tier 1: 0 - 800 -> 8%
    # Tier 2: 800 - 1500 -> 12%
    # Tier 3: > 1500 -> 18%
    if gross_pay <= 800.0:
        tax = gross_pay * 0.08
        tax_bracket = "8% Standard Tier"
    elif gross_pay <= 1500.0:
        tax = (800.0 * 0.08) + ((gross_pay - 800.0) * 0.12)
        tax_bracket = "12% Intermediate Tier"
    else:
        tax = (800.0 * 0.08) + (700.0 * 0.12) + ((gross_pay - 1500.0) * 0.18)
        tax_bracket = "18% Senior Tier"

    pension_deduction = gross_pay * pension_rate
    total_deductions = tax + health_insurance + pension_deduction
    net_pay = max(0.0, gross_pay - total_deductions)

    return {
        "success": True,
        "employee_name": employee_name or "Anonymous Employee",
        "role": role,
        "regular_hours": regular_hours,
        "overtime_hours": overtime_hours,
        "hourly_rate": hourly_rate,
        "base_pay": round(base_pay, 2),
        "overtime_pay": round(overtime_pay, 2),
        "gross_pay": round(gross_pay, 2),
        "tax": round(tax, 2),
        "tax_bracket": tax_bracket,
        "health_insurance": round(health_insurance, 2),
        "pension_deduction": round(pension_deduction, 2),
        "total_deductions": round(total_deductions, 2),
        "net_pay": round(net_pay, 2)
    }
