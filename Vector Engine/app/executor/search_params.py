from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class SearchParams:
    top_k: int = 10
    radius: Optional[float] = None   # similarity threshold
    filters: Optional[Dict[str, Any]] = None
