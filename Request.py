import requests

url = "http://127.0.0.1:8000/"
file_path = r"C:\\Users\\Pragati\\PycharmProjects\\ImagePDF\\page_1-3775102289.jpg"

try:
    with open(file_path, "rb") as file:
        files = {"file": file}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        print("Request successful")
        print(response.json())
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)  # Print the response content for debugging purposes

except FileNotFoundError:
    print("File not found. Please check the file path.")
except Exception as e:
    print(f"An error occurred: {str(e)}")