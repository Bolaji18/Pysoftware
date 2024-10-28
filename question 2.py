import requests
import csv
import pandas as pd
from tabulate import tabulate


API_KEY = "ssfdsjfksjdhfgjfgvjdshgvshgkjsdlgvkjsdgjkl"
BASE_URL = "https://pysoftware.com/v1"
CSV_FILE = "customer_addresses.csv"


HEADERS = {
    "X-API-KEY": API_KEY
}

def get_total_customers():
    """Retrieve the total number of customers."""
    response = requests.get(f"{BASE_URL}/customer_numbers", headers=HEADERS)
    response.raise_for_status()  # Raise an error if the request failed
    return int(response.text)  # Convert response to an integer

def get_customer_address(customer_number):
    """Retrieve the address of a specific customer."""
    url = f"{BASE_URL}/address_inventory/{customer_number}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def clean_address(address):
    """Validate and clean address fields."""
 
    cleaned_address = {
        "id": address.get("id", None),
        "first_name": str(address.get("first_name", "")),
        "last_name": str(address.get("last_name", "")),
        "street": str(address.get("street", "")),
        "postcode": str(address.get("postcode", "")),
        "state": str(address.get("state", "")),
        "country": str(address.get("country", "")),
        "lat": float(address.get("lat", 0.0)),
        "lon": float(address.get("lon", 0.0))
    }
    return cleaned_address

def save_addresses_to_csv(addresses):
    """Write all addresses to a CSV file."""
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=addresses[0].keys())
        writer.writeheader()
        writer.writerows(addresses)
    return CSV_FILE

def main():
    try:
      
        total_customers = get_total_customers()
        
  
        addresses = []
        for customer_number in range(1, total_customers + 1):
            address = get_customer_address(customer_number)
            cleaned_address = clean_address(address)
            addresses.append(cleaned_address)
    
        csv_path = save_addresses_to_csv(addresses)
        print(f"Addresses saved to {csv_path}")

       
        df = pd.DataFrame(addresses)
        print(tabulate(df, headers="keys", tablefmt="grid"))

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Execute the script
if __name__ == "__main__":
    main()
