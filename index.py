import requests
from bs4 import BeautifulSoup
import json

def fetch_schema(url):
    try:
        # Fetch the page content
        response = requests.get(url)
        response.raise_for_status()  # Check for errors
        page_content = response.text

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(page_content, 'html.parser')

        # Extract JSON-LD schema data
        schema_data = []
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                schema_json = json.loads(script.string)
                schema_data.append(schema_json)
            except json.JSONDecodeError:
                continue  # Skip malformed JSON

        # Extract Microdata schema
        microdata = []
        for tag in soup.find_all(True, {'itemscope': True}):
            schema_dict = {}
            for itemprop in tag.find_all(True, {'itemprop': True}):
                schema_dict[itemprop['itemprop']] = itemprop.get_text()
            microdata.append(schema_dict)

        return {"json_ld": schema_data, "microdata": microdata}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

# Example usage:
url = "https://example.com"
schema_info = fetch_schema(url)

if schema_info:
    print("JSON-LD Schema:")
    for schema in schema_info["json_ld"]:
        print(json.dumps(schema, indent=4))

    print("\nMicrodata Schema:")
    for data in schema_info["microdata"]:
        print(data)
