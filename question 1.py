import json


SERIAL_RANGE = ["C25CTW00000000001470", "C25CTW00000000001471", "C25CTW00000000001472",
                "C25CTW00000000001473", "C25CTW00000000001474", "C25CTW00000000001475",
                "C25CTW00000000001476", "C25CTW00000000001477", "C25CTW00000000001478"]


EXPECTED_SCHEMA = {
    "comment": str,
    "Internet_hubs": list
}

def validate_and_assign_serials(data):
    
    if not isinstance(data, dict):
        raise ValueError("Input data is not a valid JSON object or dictionary.")

 
    for key in EXPECTED_SCHEMA:
        if key not in data:
            raise ValueError(f"Missing key '{key}' in JSON data.")
        if not isinstance(data[key], EXPECTED_SCHEMA[key]):
            raise TypeError(f"Key '{key}' has incorrect data type.")

  
    hubs = data.get("Internet_hubs", [])
    for hub in hubs:
        if not isinstance(hub, dict) or "id" not in hub or "serial_number" not in hub:
            raise ValueError("Each hub must contain 'id' and 'serial_number' keys.")

  
    hubs_sorted = sorted(hubs, key=lambda hub: int(hub["id"][-1]) if hub["id"][-1].isdigit() else 0, reverse=True)
    
    for i, hub in enumerate(hubs_sorted):
        if i < len(SERIAL_RANGE):
            hub["serial_number"] = SERIAL_RANGE[len(SERIAL_RANGE) - 1 - i]
    
    # Return both original and updated JSON objects
    updated_data = data.copy()
    updated_data["Internet_hubs"] = hubs_sorted

    return data, updated_data

# Test data
input_data = {
    "comment": "Do NOT commit local changes to this file to source control",
    "Internet_hubs": [
        {"id": "men1", "serial_number": "C25CTW00000000001470"},
        {"id": "mn1", "serial_number": "<serial number here>"},
        {"id": "mn2", "serial_number": "<serial number here>"},
        {"id": "mn3", "serial_number": "<serial number here>"},
        {"id": "mn4", "serial_number": "<serial number here>"},
        {"id": "mn5", "serial_number": "<serial number here>"},
        {"id": "mn6", "serial_number": "<serial number here>"},
        {"id": "mn7", "serial_number": "<serial number here>"},
        {"id": "mn8", "serial_number": "<serial number here>"},
        {"id": "mn9", "serial_number": "<serial number here>"}
    ]
}

# Function call and output
original_data, updated_data = validate_and_assign_serials(input_data)
print("Original Data:", json.dumps(original_data, indent=4))
print("Updated Data:", json.dumps(updated_data, indent=4))

