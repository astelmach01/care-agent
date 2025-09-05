import json
from pathlib import Path

def parse_data_sheet():
	"""Parses the data_sheet.txt file and converts it into a structured JSON knowledge base."""
	input_path = Path(__file__).parent.parent / "data_sheet.txt"
	output_path = Path(__file__).parent.parent / "data" / "knowledge_base.json"

	if not input_path.exists():
		print(f"Error: {input_path} not found.")
		return

	output_path.parent.mkdir(exist_ok=True)

	knowledge_base = {
		"providers": [],
		"appointments_info": {},
		"accepted_insurances": [],
		"self_pay_rates": {}
	}

	with open(input_path, 'r') as f:
		lines = [line.strip() for line in f if line.strip()]

	current_provider = None
	current_department = None
	section = None

	for line in lines:
		if line == 'Provider Directory':
			section = 'providers'
			continue
		elif line == 'Appointments:':
			section = 'appointments'
			continue
		elif line == 'Accepted Insurances:':
			section = 'insurances'
			continue
		elif line == 'Self-pay:':
			section = 'self_pay'
			continue

		if section == 'providers':
			if line.startswith('- ') and ':' not in line:
				if current_provider:
					if current_department:
						current_provider['departments'].append(current_department)
					knowledge_base['providers'].append(current_provider)

				provider_name = line[2:].strip()
				current_provider = {"name": provider_name, "departments": []}
				current_department = None
			elif line.startswith('- certification:'):
				current_provider['certification'] = line.split(':', 1)[1].strip()
			elif line.startswith('- specialty:'):
				current_provider['specialty'] = line.split(':', 1)[1].strip()
			elif line.startswith('- department:'):
				if current_department:
					current_provider['departments'].append(current_department)
				current_department = {}
			elif current_department is not None:
				if line.startswith('- name:'):
					current_department['name'] = line.split(':', 1)[1].strip()
				elif line.startswith('- phone:'):
					current_department['phone'] = line.split(':', 1)[1].strip()
				elif line.startswith('- address:'):
					current_department['address'] = line.split(':', 1)[1].strip()
				elif line.startswith('- hours:'):
					current_department['hours'] = line.split(':', 1)[1].strip()

	# Append the last processed provider and department
	if current_provider:
		if current_department:
			current_provider['departments'].append(current_department)
		knowledge_base['providers'].append(current_provider)

	# Simplified parsing for other sections
	knowledge_base['appointments_info'] = {
		"types": {
			"new": {"duration_minutes": 30, "arrival_minutes_early": 30},
			"established": {"duration_minutes": 15, "arrival_minutes_early": 10},
			"established_patient_threshold_years": 5
		}
	}
	knowledge_base['accepted_insurances'] = [
		"Medicaid", "United Health Care", "Blue Cross Blue Shield of North Carolina", "Aetna", "Cigna"
	]
	knowledge_base['self_pay_rates'] = {
		"Primary Care": 150, "Orthopedics": 300, "Surgery": 1000
	}

	with open(output_path, 'w') as f:
		json.dump(knowledge_base, f, indent=2)

	print(f"Successfully created {output_path}")

if __name__ == '__main__':
	parse_data_sheet()