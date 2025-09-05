from datetime import datetime
from collections import defaultdict
from typing import Set, Tuple, Dict

class SchedulingService:
	def __init__(self):
		# In-memory calendar simulation: {(provider_name, date_str): {time_str}}
		self.calendar: Dict[Tuple[str, str], Set[str]] = defaultdict(set)

	def check_availability(self, provider_name: str, appointment_dt: datetime) -> bool:
		"""Checks if a time slot is available for a provider."""
		date_str = appointment_dt.strftime("%Y-%m-%d")
		time_str = appointment_dt.strftime("%H:%M")

		booked_times = self.calendar.get((provider_name, date_str), set())
		return time_str not in booked_times

	def book_appointment(self, provider_name: str, patient_name: str, appointment_dt: datetime) -> bool:
		"""Books an appointment if the slot is available."""
		if self.check_availability(provider_name, appointment_dt):
			date_str = appointment_dt.strftime("%Y-%m-%d")
			time_str = appointment_dt.strftime("%H:%M")
			self.calendar[(provider_name, date_str)].add(time_str)
			print(f"APPOINTMENT BOOKED: {patient_name} with {provider_name} on {date_str} at {time_str}")
			return True
		return False