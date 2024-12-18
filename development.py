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
base_url = f'https://oauth.reddit.com/r/{subreddit}/new?limit=1000'
response = requests.get(base_url, headers=headers)
if response.status_code == 200:
    post_data = response.json()
else:
    print('cooked') #xD
    print(response.status_code)

## Going to try and make a few simple functions for working with the response dump. It returns a nasty JSON file with all types of information imbedded, creating a few
## easy to read/use functions will support further development efforts.


def fetch_posts(url):
    response = requests.get(url, headers=headers)
    ## This is strictly for debugging, fix later
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code}")
    return response.json()
## Target data to extract from json dump
post_id = []
post_title = []
post_sub = []
post_ups = []
post_ups_ratio = []
post_text = []

## This loop intends to pull the top 100 postIDs per day from each target subreddit, and save them in a list
stock_sub_list = ['r/stocks', 'r/bitcoin']
for sub in stock_sub_list:
    base_url = f'https://oauth.reddit.com/{sub}/top?limit=100&t=day'
    start_date_dt = datetime.datetime.now()
    end_date_dt = start_date_dt - datetime.timedelta(weeks=1)
    while start_date_dt > end_date_dt:
        # Converting datetime to unix format
        before_timestamp = int(start_date_dt.timestamp())
        after_timestamp = int((start_date_dt - datetime.timedelta(days=1)).timestamp())
        url = f'{base_url}&before={before_timestamp}&after={after_timestamp}'
        print(url)
        response_data = fetch_posts(url)
        posts = response_data['data']['children']

        if response_data is None or 'data' not in response_data or 'children' not in response_data['data']:
            print("No more posts found or error in fetching data.")
            break
        
        # For debugging, having issues where API call returns 200 (sucsess) but has empty list
        if not posts:
            print(f"No posts found for {start_date_dt.strftime('%Y-%m-%d')}.")
        # If response is not empty, appends values to primary list
        else:
            for post in posts:
                post_id.append(post['data']['id'])
                post_title.append(post['data']['title'])
                post_sub.append(post['data']['subreddit'])
                post_ups.append(post['data']['ups'])
                post_ups_ratio.append(post['data']['upvote_ratio'])
                post_text.append(post['data'].get('selftext', ''))
            
        # Moving date range one day backward    
        start_date_dt -= datetime.timedelta(days=1)
        # Respecting reddit API call limits
        time.sleep(1)

        ## Inlcuding this print statement for sanity as this takes forever to run
        print(start_date_dt)

print(post_id)
print(len(post_id))
print(len(post_sub))
print(len(post_ups))
print(len(post_text))
print(post_title[-1])



