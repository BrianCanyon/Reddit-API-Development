## Libraries
import requests

## Authentication
def get_reddit_token():

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
subreddit_url = 'https://oauth.reddit.com/r/wallstreetbets/new?limit=5'
response = requests.get(subreddit_url, headers=headers)
print(type(response))
if response.status_code == 200:
    post_data = response.json()
    print(type(post_data))
else:
    print('cooked')

## Going to try and make a few simple functions for working with the response dump. It returns a nasty JSON file with all types of information imbedded, creating a few
## easy to read/use functions will support further development efforts.
def get_post_ids(post_dict):
    id_list = []
    for post in post_dict['data']['children']:
        id_list.append(post['data']['id'])
    return id_list



print(get_post_ids(post_data))

