"""
Project 6: Customer Record Management Application
Zero-configuration SQLite CRUD engine with SQL injection defense and MySQL connection guidelines.
"""
import sqlite3
from typing import Dict, Any, List
from app.config import DATA_DIR

CRM_DB_PATH = DATA_DIR / "crm_database.db"

class CustomerCRM:
    def __init__(self, db_path: str = str(CRM_DB_PATH)):
        self.db_path = db_path
        self._mem_conn = None
        if self.db_path == ":memory:":
            self._mem_conn = sqlite3.connect(":memory:", check_same_thread=False)
            self._mem_conn.row_factory = sqlite3.Row
        self._init_schema()

    def _get_connection(self):
        if self._mem_conn:
            return self._mem_conn
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS crm_customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    tier TEXT DEFAULT 'Standard',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

            # Seed default records if empty
            cur.execute("SELECT COUNT(*) FROM crm_customers")
            if cur.fetchone()[0] == 0:
                defaults = [
                    ("Aarav Sharma", "aarav@marwadi.edu", "+91 98765 43210", "Premium"),
                    ("Priya Patel", "priya@marwadi.edu", "+91 98765 12345", "Enterprise"),
                    ("Rohan Mehta", "rohan@marwadi.edu", "+91 98765 67890", "Standard"),
                    ("Sneha Joshi", "sneha@marwadi.edu", "+91 98765 99887", "Standard")
                ]
                cur.executemany("INSERT INTO crm_customers (name, email, phone, tier) VALUES (?, ?, ?, ?)", defaults)
                conn.commit()

    def create_customer(self, name: str, email: str, phone: str = "", tier: str = "Standard") -> Dict[str, Any]:
        if not name or not email:
            return {"success": False, "error": "Customer Name and Email are mandatory."}

        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO crm_customers (name, email, phone, tier) VALUES (?, ?, ?, ?)",
                    (name.strip(), email.strip().lower(), phone.strip(), tier)
                )
                conn.commit()
                return {"success": True, "id": cur.lastrowid, "message": f"Customer '{name}' registered successfully."}
        except sqlite3.IntegrityError:
            return {"success": False, "error": f"A customer with email '{email}' already exists in the database."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_customers(self, search: str = "") -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cur = conn.cursor()
            if search.strip():
                term = f"%{search.strip().lower()}%"
                cur.execute(
                    "SELECT * FROM crm_customers WHERE LOWER(name) LIKE ? OR LOWER(email) LIKE ? OR LOWER(tier) LIKE ? ORDER BY id DESC",
                    (term, term, term)
                )
            else:
                cur.execute("SELECT * FROM crm_customers ORDER BY id DESC")

            rows = cur.fetchall()
            return [dict(row) for row in rows]

    def update_customer(self, cust_id: int, name: str, email: str, phone: str, tier: str) -> Dict[str, Any]:
        try:
            with self._get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "UPDATE crm_customers SET name = ?, email = ?, phone = ?, tier = ? WHERE id = ?",
                    (name.strip(), email.strip().lower(), phone.strip(), tier, cust_id)
                )
                conn.commit()
                if cur.rowcount == 0:
                    return {"success": False, "error": f"Customer ID {cust_id} not found."}
                return {"success": True, "message": f"Customer #{cust_id} updated successfully."}
        except sqlite3.IntegrityError:
            return {"success": False, "error": f"Email '{email}' is already in use by another customer."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete_customer(self, cust_id: int) -> Dict[str, Any]:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM crm_customers WHERE id = ?", (cust_id,))
            conn.commit()
            if cur.rowcount == 0:
                return {"success": False, "error": f"Customer ID {cust_id} not found."}
            return {"success": True, "message": f"Customer #{cust_id} removed from database."}
