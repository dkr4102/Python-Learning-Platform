"""
Project 5: Banking Account Management System
Object-Oriented financial engine with account hierarchies, encapsulation, and transaction audits.
"""
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import List, Dict, Any

class InsufficientFundsError(Exception):
    pass

class InvalidTransactionError(Exception):
    pass

class BaseAccount(ABC):
    def __init__(self, account_number: str, holder_name: str, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise InvalidTransactionError("Initial balance cannot be negative.")
        self.account_number = account_number
        self.holder_name = holder_name
        self._balance = float(initial_balance)
        self._ledger: List[Dict[str, Any]] = []
        self._record_transaction("OPEN_ACCOUNT", initial_balance, "Account opened")

    @property
    def balance(self) -> float:
        return self._balance

    def _record_transaction(self, tx_type: str, amount: float, description: str):
        self._ledger.append({
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "type": tx_type,
            "amount": amount,
            "balance_after": self._balance,
            "description": description
        })

    def deposit(self, amount: float, description: str = "Deposit") -> float:
        if amount <= 0:
            raise InvalidTransactionError("Deposit amount must be positive.")
        self._balance += amount
        self._record_transaction("DEPOSIT", amount, description)
        return self._balance

    @abstractmethod
    def withdraw(self, amount: float, description: str = "Withdrawal") -> float:
        pass

    def get_ledger(self) -> List[Dict[str, Any]]:
        return list(self._ledger)


class SavingsAccount(BaseAccount):
    def __init__(self, account_number: str, holder_name: str, initial_balance: float = 500.0, interest_rate: float = 0.04):
        super().__init__(account_number, holder_name, initial_balance)
        self.interest_rate = interest_rate

    def withdraw(self, amount: float, description: str = "Savings Withdrawal") -> float:
        if amount <= 0:
            raise InvalidTransactionError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise InsufficientFundsError(f"Insufficient funds: available ${self._balance:.2f}, requested ${amount:.2f}")
        self._balance -= amount
        self._record_transaction("WITHDRAW", -amount, description)
        return self._balance

    def apply_monthly_interest(self) -> float:
        interest = self._balance * (self.interest_rate / 12.0)
        self._balance += interest
        self._record_transaction("INTEREST", interest, f"Monthly compound interest @ {self.interest_rate*100:.1f}% APR")
        return interest


class CheckingAccount(BaseAccount):
    def __init__(self, account_number: str, holder_name: str, initial_balance: float = 200.0, overdraft_limit: float = 500.0):
        super().__init__(account_number, holder_name, initial_balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount: float, description: str = "Checking Withdrawal") -> float:
        if amount <= 0:
            raise InvalidTransactionError("Withdrawal amount must be positive.")
        available = self._balance + self.overdraft_limit
        if amount > available:
            raise InsufficientFundsError(f"Overdraft exceeded: available with limit ${available:.2f}, requested ${amount:.2f}")
        self._balance -= amount
        self._record_transaction("WITHDRAW", -amount, description)
        return self._balance


class BankLedgerSystem:
    def __init__(self):
        self.accounts: Dict[str, BaseAccount] = {
            "SA-2401": SavingsAccount("SA-2401", "Aarav Sharma", 1500.0, 0.045),
            "CA-8802": CheckingAccount("CA-8802", "Priya Patel", 850.0, 300.0)
        }

    def transfer(self, from_acc_num: str, to_acc_num: str, amount: float) -> Dict[str, Any]:
        if from_acc_num not in self.accounts or to_acc_num not in self.accounts:
            return {"success": False, "error": "One or both account numbers not found."}
        if from_acc_num == to_acc_num:
            return {"success": False, "error": "Cannot transfer to the same account."}

        source = self.accounts[from_acc_num]
        dest = self.accounts[to_acc_num]

        try:
            source.withdraw(amount, f"Transfer to {to_acc_num}")
            dest.deposit(amount, f"Transfer from {from_acc_num}")
            return {
                "success": True,
                "message": f"Successfully transferred ${amount:.2f} from {from_acc_num} to {to_acc_num}.",
                "from_balance": source.balance,
                "to_balance": dest.balance
            }
        except (InsufficientFundsError, InvalidTransactionError) as e:
            return {"success": False, "error": str(e)}
