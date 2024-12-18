import requests
import datetime
import time
def get_reddit_token():

    # Credentials, saved locally. Needs to be revised
    login_file_path = "/Users/brian.canyon/documents/reddit_login_secret.txt"
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
        return token
    else:
        return response.json()
# Your access token from Reddit OAuth2
access_token = get_reddit_token()

# Headers for authentication
headers = {'Authorization': f'bearer {access_token}', 'User-Agent': 'your_app_name'}

# Base URL for the API call
base_url = 'https://oauth.reddit.com/r/wallstreetbets/new?limit=1000'

def fetch_posts(url, after=None):
    if after:
        url = f"{url}&after={after}"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return None
    return response.json()

# List to store post IDs
post_ids = []

# Define the start and end dates
start_date = datetime.datetime(2023, 12, 1)
end_date = datetime.datetime(2023, 12, 31)

# Loop through each day in the date range
current_date = start_date
while current_date <= end_date:
    # Convert current_date to Unix timestamp
    print(current_date)
    before_timestamp = int(current_date.timestamp())
    after_timestamp = int((current_date - datetime.timedelta(days=1)).timestamp())
    
    # Build the URL with date parameters
    url = f"{base_url}&before={before_timestamp}&after={after_timestamp}"
    
    # Fetch posts
    response_data = fetch_posts(url)
    if response_data is None or 'data' not in response_data or 'children' not in response_data['data']:
        print("No more posts found or error in fetching data.")
        break
    
    posts = response_data['data']['children']
    if not posts:  # Check if posts list is empty
        print(f"No posts found for {current_date.strftime('%Y-%m-%d')}.")
    else:
        post_ids.extend([post['data']['id'] for post in posts])
    
    # Move to the next day
    current_date += datetime.timedelta(days=1)
    time.sleep(1)  # Accommodating Reddit API call frequency limits

print(post_ids)
print(len(post_ids))
