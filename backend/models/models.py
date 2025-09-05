from pydantic import BaseModel, Field
from typing import List, Optional

class Department(BaseModel):
    name: str
    phone: str
    address: str
    hours: str

class Provider(BaseModel):
    name: str
    certification: str
    specialty: str
    departments: List[Department]

class Appointment(BaseModel):
    date: str
    time: str
    provider: str
    status: str

class Patient(BaseModel):
    id: int
    name: str
    dob: str
    pcp: str
    ehrId: str
    referred_providers: List[dict]
    appointments: List[Appointment]