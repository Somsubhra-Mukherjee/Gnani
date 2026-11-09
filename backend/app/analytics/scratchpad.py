import threading
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class MemoEntry(BaseModel):
    id: int
    timestamp: str
    query: str
    category: str
    details: str
    formula: Optional[str] = None
    data_points: Dict[str, Any] = {}
    balance_sheet: Optional[Dict[str, Any]] = None

class ExecutiveScratchpad:
    """
    Stateful session scratchpad for executive computations and scenario modeling.
    Maintains intermediate variables across conversational queries and aggregates
    the working memo for instant PDF export.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self._entries: List[MemoEntry] = []
        self._counter: int = 1
        self._variables: Dict[str, Any] = {
            # Default baseline metrics for Fresh Organic Paneer 500g across key markets
            "last_product": "Fresh Organic Paneer 500g",
            "last_sku": "PRD-DAIRY-01",
            # Gujarat (West Region / Ahmedabad)
            "guj_prod_cost": 188.80,
            "guj_trans_cost": 24.50,
            "guj_landed_cost": 213.30,
            "guj_price": 240.00,
            "guj_volume": 18200,
            "guj_revenue": 4368000.00,
            "guj_cogs": 3882060.00,
            "guj_profit": 485940.00,
            "guj_margin_pct": 11.12,
            # West Bengal (East Region / Kolkata)
            "wb_prod_cost": 182.50,
            "wb_trans_cost": 25.60,
            "wb_landed_cost": 208.10,
            "wb_price": 245.00,
            "wb_volume": 24500,
            "wb_revenue": 6002500.00,
            "wb_cogs": 5098450.00,
            "wb_profit": 904050.00,
            "wb_margin_pct": 15.06,
        }

    def set_variable(self, key: str, value: Any):
        with self._lock:
            self._variables[key] = value

    def get_variable(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._variables.get(key, default)

    def add_entry(
        self,
        query: str,
        category: str,
        details: str,
        formula: Optional[str] = None,
        data_points: Optional[Dict[str, Any]] = None,
        balance_sheet: Optional[Dict[str, Any]] = None
    ) -> MemoEntry:
        with self._lock:
            now_str = datetime.now().strftime("%H:%M:%S")
            entry = MemoEntry(
                id=self._counter,
                timestamp=now_str,
                query=query,
                category=category,
                details=details,
                formula=formula,
                data_points=data_points or {},
                balance_sheet=balance_sheet
            )
            self._counter += 1
            self._entries.append(entry)
            return entry

    def get_entries(self) -> List[MemoEntry]:
        with self._lock:
            return list(self._entries)

    def clear(self):
        with self._lock:
            self._entries.clear()
            self._counter = 1

scratchpad = ExecutiveScratchpad()
