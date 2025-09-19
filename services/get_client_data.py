import requests

class ClientData:
    def __init__(self, cui):
        self.cui = cui
        self.url = f"https://api.opencorporates.com/v0.4/companies/ro/{self.cui}"

    def get_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            company = data.get("results", {}).get("company", {})
            name = company.get("name")
            number = company.get("company_number")
            address = company.get("registered_address")

            print("Company Name:", name)
            print("Company Number:", number)
            print("Registered Address:", address)

            return [name, number, address]
        else:
            print("Error:", response.status_code, response.text)
            return None
