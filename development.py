## Libraries
import requests
import datetime
import time

## Authentication
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
    
## Lets try to query some post data

# ChatGPT says these are the most popular stock related subreddits, I chose to toss bitcoin in becuase why not

stock_sub_list = ['r/wallstreetbets', 'r/stocks', 'r/investing', 'r/pennystocks', 'r/StockMarket', 'r/Daytrading', 'r/Options', 'r/Finance', 'r/Dividends', 'r/Bitcoin']
token = get_reddit_token()
headers = {
    'Authorization': f'Bearer {token}',
    'User-Agent': 'MyBot'
    }
# This URL returns the single most recent post on /WSB, URL stuff confuses me greatly, so I am defining what does what
subreddit = 'investing'
base_url = f'https://oauth.reddit.com/r/{subreddit}/new?limit=100'
response = requests.get(base_url, headers=headers)
if response.status_code == 200:
    post_data = response.json()
else:
    print('cooked') #xD
    print(response.status_code)

## Going to try and make a few simple functions for working with the response dump. It returns a nasty JSON file with all types of information imbedded, creating a few
## easy to read/use functions will support further development efforts.
def get_post_ids(post_dict):
    id_list = []
    for post in post_dict['data']['children']:
        id_list.append(post['data']['id'])
    return id_list


def fetch_posts(url, after=None):
    if after:
        url = f"{url}&after={after}"
    response = requests.get(url, headers=headers)
    ## This is strictly for debugging, fix later
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code}")
    return response.json()
post_ids = []

timestamp_dt = datetime.datetime.now()
historical_data_limit = timestamp_dt - datetime.timedelta(weeks=15)
last_post = None
while timestamp_dt > historical_data_limit:
    response_data = fetch_posts(base_url, after=last_post)
    posts = response_data['data']['children']

    if not posts: #check is the posts list is empty, unsure why this would be
        print(last_post)
        print(response_data)
        print(posts)
        print(timestamp_dt)
        print('no more posts found')
        break

    last_post = posts[-1]['data']['name']
    post_ids.extend([post['data']['id'] for post in posts])
    timestamp_utc = posts[-1]['data']['created_utc'] #this line creates a timestamp but in utc format
    timestamp_dt = datetime.datetime.fromtimestamp(timestamp_utc)
    time.sleep(1) # Accomidating reddit API call frequency limits, yes this script will be slow
    
print(post_ids)
print(len(post_ids))



