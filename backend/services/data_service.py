import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from models.models import Provider

class DataService:
    def __init__(self, knowledge_base_path: Path):
        with open(knowledge_base_path, 'r') as f:
            self._db = json.load(f)
        self._providers = [Provider(**p) for p in self._db.get("providers", [])]

    def find_providers(self, name: Optional[str] = None, specialty: Optional[str] = None) -> List[Provider]:
        """Finds providers by name and/or specialty."""
        results = self._providers
        if name:
            results = [p for p in results if name.lower() in p.name.lower()]
        if specialty:
            results = [p for p in results if specialty.lower() in p.specialty.lower()]
        return results

    def get_insurance_info(self) -> Dict[str, Any]:
        """Returns accepted insurances and self-pay rates."""
        return {
            "accepted": self._db.get("accepted_insurances", []),
            "self_pay": self._db.get("self_pay_rates", {})
        }

    def get_appointment_rules(self) -> Dict[str, Any]:
        return self._db.get("appointments_info", {})