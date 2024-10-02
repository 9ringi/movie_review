import requests

# Base URL for your API
BASE_URL = 'http://127.0.0.1:8000/api/reviews/movie/'

# Set the authentication header
headers = {'Authorization': 'Token 38c469cd4eaaaba31c92a870b5628857e4933023'}

# Parameters for the GET request
params = {'movie_title': 'Inception'}

# Make the GET request
response = requests.get(BASE_URL, headers=headers, params=params)

# Print the response
print("Response:", response.json())
