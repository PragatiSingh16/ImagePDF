import requests

url = "http://127.0.0.1:8000/"
file_path = "C:\\Users\\Pragati\\Desktop\\ImagePDF\\imagerandom.jpg"

files = {"file": open(file_path, "rb")}
response = requests.post(url, files=files)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print("Request successful")
    print(response.json())
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)  # Print the response content for debugging purposes