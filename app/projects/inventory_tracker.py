"""
Project 3: Inventory Management Tracker
Dictionary-backed catalog engine with stock level tracking and reorder alerts.
"""
from typing import Dict, Any, List

class InventoryManager:
    def __init__(self):
        self.inventory: Dict[str, Dict[str, Any]] = {
            "SKU-001": {"name": "Mechanical Keyboard (Cherry MX)", "category": "Hardware", "price": 89.99, "stock": 18},
            "SKU-002": {"name": "4K Ultra-Wide Monitor", "category": "Hardware", "price": 349.50, "stock": 3},
            "SKU-003": {"name": "USB-C Multiport Dock", "category": "Accessories", "price": 45.00, "stock": 2},
            "SKU-004": {"name": "Ergonomic Mesh Chair", "category": "Furniture", "price": 199.00, "stock": 11},
            "SKU-005": {"name": "Python Programming Textbook", "category": "Books", "price": 42.00, "stock": 25}
        }

    def add_or_update_item(self, sku: str, name: str, category: str, price: float, stock: int) -> Dict[str, Any]:
        if not sku or not name:
            return {"success": False, "error": "SKU and Item Name are required."}
        if price < 0 or stock < 0:
            return {"success": False, "error": "Price and Stock quantity cannot be negative."}

        self.inventory[sku.upper()] = {
            "name": name,
            "category": category or "General",
            "price": float(price),
            "stock": int(stock)
        }
        return {"success": True, "message": f"Item '{name}' ({sku.upper()}) saved successfully."}

    def remove_item(self, sku: str) -> Dict[str, Any]:
        sku_clean = sku.upper()
        if sku_clean in self.inventory:
            removed = self.inventory.pop(sku_clean)
            return {"success": True, "message": f"Removed SKU '{sku_clean}' ({removed['name']})."}
        return {"success": False, "error": f"SKU '{sku_clean}' not found in inventory."}

    def search_items(self, query: str = "") -> List[Dict[str, Any]]:
        q = query.lower().strip()
        results = []
        for sku, item in self.inventory.items():
            if not q or q in sku.lower() or q in item["name"].lower() or q in item["category"].lower():
                results.append({
                    "sku": sku,
                    "name": item["name"],
                    "category": item["category"],
                    "price": item["price"],
                    "stock": item["stock"],
                    "low_stock": item["stock"] < 5
                })
        return results

    def get_summary_metrics(self) -> Dict[str, Any]:
        total_items = len(self.inventory)
        total_units = sum(item["stock"] for item in self.inventory.values())
        total_valuation = sum(item["stock"] * item["price"] for item in self.inventory.values())
        low_stock_items = [
            {"sku": sku, "name": item["name"], "stock": item["stock"]}
            for sku, item in self.inventory.items()
            if item["stock"] < 5
        ]

        # Category breakdown
        cat_valuation: Dict[str, float] = {}
        for item in self.inventory.values():
            cat = item["category"]
            cat_valuation[cat] = cat_valuation.get(cat, 0.0) + (item["stock"] * item["price"])

        return {
            "total_skus": total_items,
            "total_units": total_units,
            "total_valuation": round(total_valuation, 2),
            "low_stock_count": len(low_stock_items),
            "low_stock_alerts": low_stock_items,
            "category_valuation": {k: round(v, 2) for k, v in cat_valuation.items()}
        }
