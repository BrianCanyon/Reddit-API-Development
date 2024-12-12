## Libraries
import requests

## Authentication Parameters

# Credentials, saved locally. Needs to be revised
login_file_path = "C:\\Users\\j\\Documents\\reddit_login_secret.txt"
credentials_dict = {}
with open(login_file_path) as login_info:
    for line in login_info:
        key, value = line.split('=')
        credentials_dict[key] = value.replace("\n", "")

# POST request for access token
url = 'https://www.reddit.com/api/v1/access_token'
headers = {
    'User-Agent': 'MyBot' 
    }
data = {
    'grant_type': 'password',
    'username': credentials_dict['username'],
    'password': credentials_dict['password']
    }
response = requests.post(url, headers=headers, data=data, auth=(credentials_dict['client_id'], credentials_dict['client_secret']))
if response.status_code == 200:
    token = response.json().get('access_token')
else:
    print("Failed to Authenticate")
    print(response.json())