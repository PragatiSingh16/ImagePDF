import requests

url = 'http://localhost:8000/process_file/'
files = {'file': open('test.jpg', 'rb')}  # Replace 'your_file.pdf' with the path to your file
response = requests.post(url, files=files)
print(response.text)
print(response.json())  # Process the response returned by your FastAPI application
