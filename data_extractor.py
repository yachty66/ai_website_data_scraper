import os 
import base64
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the OpenAI API Key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

prompt = """
You are provided with a screenshot of a website that shows data from virtual machines. You need to extract the price and configuration of each machine.

You need to return your extracted data in JSON format.

Example:

{
    "machines": [
        {
            "name": "machine1",
            "price": "100",
            "configuration": "1 CPU, 2 GB RAM, 10 GB SSD"
        },
        {
            "name": "machine2",
            "price": "200",
            "configuration": "2 CPU, 4 GB RAM, 20 GB SSD"
        }
    ]
}

It is possible that the configurations on the website look different.

If you cannot find any data, return an empty array, like this:

[]

Return the JSON array:
"""

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_data_from_screenshots(screenshots_dir):
    all_results = []  # List to accumulate results

    # Iterate over all screenshots in the directory
    for filename in os.listdir(screenshots_dir):
        if filename.endswith(".png"):  # Ensure it's a PNG file
            image_path = os.path.join(screenshots_dir, filename)
            
            # Getting the base64 string
            base64_image = encode_image(image_path)

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            payload = {
                "model": "gpt-4o",
                "response_format": {"type": "json_object"},
                "messages": [
                    {
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": prompt
                        },
                        {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                        }
                    ]
                    }
                ]
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            result = response.json()
            
            # Extract the content and append to results
            message_content = result['choices'][0]['message']['content']
            all_results.append(json.loads(message_content))  # Assuming the response is valid JSON

    # Save all results to a single JSON file
    with open("combined_results.json", "w") as outfile:
        json.dump(all_results, outfile, indent=4)

    print("All results saved to combined_results.json")

if __name__ == "__main__":
    extract_data_from_screenshots("screenshots")