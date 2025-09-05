import httpx
from models.models import Patient

class PatientService:
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url

    async def get_patient(self, patient_id: int) -> Patient:
        """Fetches patient data from the external patient API."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_base_url}/patient/{patient_id}")
            response.raise_for_status()
            return Patient(**response.json())