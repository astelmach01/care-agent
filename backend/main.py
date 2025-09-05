import os
from dotenv import load_dotenv
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, date, timedelta
import asyncio

import fastapi
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # Import CORS
from typing import Optional, List, Annotated

from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelMessage, UserPromptPart, TextPart

from models.models import Patient, Provider
from services.data_service import DataService
from services.patient_service import PatientService
from services.scheduling_service import SchedulingService

# --- Initialization ---
load_dotenv()

# --- Singleton Services & State ---
scheduling_service = SchedulingService()
chat_history: List[ModelMessage] = []

# --- FastAPI Application ---
app = fastapi.FastAPI()

# --- CORS Middleware ---
# This allows your React frontend to communicate with the backend
origins = [
    "http://localhost:3000",  # Default for create-react-app
    "http://localhost:5173",  # Default for Vite
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Dependency Injection Container ---
@dataclass
class CareCoordinatorDeps:
    data_service: DataService
    patient_service: PatientService
    scheduling_service: SchedulingService


# --- Agent Definition ---
agent = Agent[CareCoordinatorDeps, str](
    "openai:gpt-4.1",
    deps_type=CareCoordinatorDeps,
    output_type=str,
    instructions="""
    You are a helpful and efficient Care Coordinator Assistant for a nurse.
    Your primary goal is to help the nurse book appointments for patients and answer related questions.
    Be conversational, clear, and proactive.

    ***CRITICAL INSTRUCTION: You MUST use your tools to find information (like patient details) before asking the nurse. If you are given a patient ID, your FIRST step is always to use the `get_patient_details` tool.***

    When booking, always confirm the final details with the nurse.
    Format your responses using Markdown.
    Today's date is {today_date}.
    """.format(today_date=date.today().isoformat()),
)


# --- Tool Definitions (Unchanged) ---
@agent.tool
async def get_patient_details(
    ctx: RunContext[CareCoordinatorDeps], patient_id: int
) -> Patient:
    """Fetches all details for a specific patient by their ID, including referrals and past appointments."""
    print(f"--- Calling Tool: get_patient_details with patient_id={patient_id} ---")
    return await ctx.deps.patient_service.get_patient(patient_id)


@agent.tool
def find_providers(
    ctx: RunContext[CareCoordinatorDeps],
    name: Optional[str] = None,
    specialty: Optional[str] = None,
) -> List[Provider]:
    """Searches for healthcare providers by name and/or specialty to find their locations, hours, and contact info."""
    print(
        f"--- Calling Tool: find_providers with name='{name}' and specialty='{specialty}' ---"
    )
    return ctx.deps.data_service.find_providers(name, specialty)


@agent.tool
def check_insurance_and_rates(
    ctx: RunContext[CareCoordinatorDeps], insurance_provider: Optional[str] = None
) -> str:
    """Checks if an insurance is accepted and provides self-pay rates if it is not."""
    print(
        f"--- Calling Tool: check_insurance_and_rates with insurance_provider='{insurance_provider}' ---"
    )
    info = ctx.deps.data_service.get_insurance_info()
    accepted = info["accepted"]
    if insurance_provider and insurance_provider in accepted:
        return f"Yes, {insurance_provider} is an accepted insurance provider."
    else:
        rates_str = ", ".join([f"{s}: ${c}" for s, c in info["self_pay"].items()])
        if insurance_provider:
            return f"No, {insurance_provider} is not in the list of accepted providers. The self-pay rates are: {rates_str}."
        else:
            return f"The accepted insurance providers are: {', '.join(accepted)}. The self-pay rates are: {rates_str}."


@agent.tool
def book_appointment(
    ctx: RunContext[CareCoordinatorDeps],
    patient_id: int,
    provider_name: str,
    appointment_datetime_str: str,
    location_address: str,
) -> str:
    """
    Books an appointment for a patient with a specific provider at a given date, time, and location.
    The `appointment_datetime_str` must be in ISO format, e.g., 'YYYY-MM-DDTHH:MM:SS'.
    """
    print(
        f"--- Calling Tool: book_appointment for patient_id={patient_id} with {provider_name} ---"
    )
    try:
        appointment_dt = datetime.fromisoformat(appointment_datetime_str)
        patient = asyncio.run(ctx.deps.patient_service.get_patient(patient_id))

        is_available = ctx.deps.scheduling_service.check_availability(
            provider_name, appointment_dt
        )
        if not is_available:
            return f"Error: The time slot {appointment_dt.strftime('%Y-%m-%d %H:%M')} is already booked for {provider_name}. Please suggest another time."

        success = ctx.deps.scheduling_service.book_appointment(
            provider_name, patient.name, appointment_dt
        )
        if success:
            rules = ctx.deps.data_service.get_appointment_rules()
            threshold_years = rules["types"]["established_patient_threshold_years"]
            is_established = False
            for appt in patient.appointments:
                if appt.provider.lower() in provider_name.lower():
                    appt_date = datetime.strptime(appt.date, "%m/%d/%y")
                    if (datetime.now() - appt_date) < timedelta(
                        days=365 * threshold_years
                    ):
                        is_established = True
                        break

            appt_type = "ESTABLISHED" if is_established else "NEW"
            arrival_info = rules["types"]["established" if is_established else "new"][
                "arrival_minutes_early"
            ]

            return (
                f"Successfully booked a **{appt_type}** appointment for **{patient.name}** with **{provider_name}** "
                f"at **{location_address}** on **{appointment_dt.strftime('%A, %B %d, %Y at %I:%M %p')}**. "
                f"\n\nPlease advise the patient to arrive **{arrival_info} minutes early**."
            )
        else:
            return "Booking failed. The requested time slot may have just been taken. Please try another time."

    except Exception as e:
        return f"An error occurred during booking: {str(e)}. Please ensure the date/time format is correct (YYYY-MM-DDTHH:MM:SS) and all details are valid."


# --- API Endpoints ---


@app.get("/history")
async def get_history():
    display_history = [
        msg
        for msg in chat_history
        if (
            isinstance(msg.parts[0], UserPromptPart)
            or isinstance(msg.parts[0], TextPart)
        )
    ]
    return JSONResponse(content=[msg.model_dump() for msg in display_history])


@app.post("/reset")
async def reset():
    global chat_history, scheduling_service
    chat_history.clear()
    scheduling_service = SchedulingService()
    print("--- Conversation has been reset ---")
    return JSONResponse(content={"message": "Conversation reset successfully"})


@app.post("/chat")
async def chat(prompt: Annotated[str, fastapi.Form()]):
    global chat_history
    deps = CareCoordinatorDeps(
        data_service=DataService(
            Path(__file__).parent / "data" / "knowledge_base.json"
        ),
        patient_service=PatientService("http://127.0.0.1:5000"),
        scheduling_service=scheduling_service,
    )

    print(f"--- Running for prompt: {prompt[:50]}... ---")

    # Use agent.run for a complete, non-streamed response
    result = await agent.run(prompt, deps=deps, message_history=chat_history)

    # Update chat history
    chat_history.extend(result.new_messages())

    print(f"--- Run completed. Output: {result.output[:100]}... ---")

    # Return the final output as JSON
    return JSONResponse(content={"role": "assistant", "content": result.output})


if __name__ == "__main__":
    import uvicorn

    print("Starting Care Coordinator Assistant API on http://localhost:8000")
    print("Ensure the mock patient data API is running on http://127.0.0.1:5000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
