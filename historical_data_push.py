## This script populates a local SQL DB with relevant subreddit data

## Libraries
import requests
import datetime
import time
import pandas as pd
from sqlalchemy import create_engine, text

## Authentication
# SQL
engine = create_engine('mysql+mysqlconnector://root:@localhost/mysql')

# Since this script will populate the 'posts' table from scratch, we need to make sure
# it is empty prior to appending (ie. INSERT INTO)
drop_table = text("DROP TABLE IF EXISTS posts")
with engine.connect() as con:
    con.execute(drop_table)
    con.commit()

# Reddit
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
    response = requests.post(url, headers=headers, data=data, auth=(credentials_dict['client_id'],\
                                                                     credentials_dict['client_secret']))
    # If authentication is successful, the token is returned
    if response.status_code == 200:
        token = response.json().get('access_token')
        return token
    else:
        return response.json()
    
## Now that we have a token for authentication, we can query reddit data directly (get)

# ChatGPT says these are the most popular stock related subreddits. I chose to toss bitcoin in becuase
# why not, this list can be modified to target whichever subreddits the user would like info on.
stock_sub_list = ['r/wallstreetbets', 'r/stocks', 'r/investing', 'r/pennystocks', 'r/StockMarket', \
                  'r/Daytrading', 'r/Options', 'r/Finance', 'r/Dividends', 'r/Bitcoin']

# Token is created and saved in the 'headers' variable, which will be part of future get requests.
token = get_reddit_token()
headers = {
    'Authorization': f'Bearer {token}',
    'User-Agent': 'MyBot'
    }

# Given a url, this function will return the reponse. If failed, will return the error status code.
def get_posts(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code}")
    return response.json()

## This function will loop through the targeted subreddits and push data to SQL
def main():
    for sub in stock_sub_list:
        # The url changes throughout each itteration of the loop, it is a unique identifier as to what 
        # data we are looking to query from reddit. This step only changes the subreddit.  
        base_url = f'https://oauth.reddit.com/{sub}/top?limit=100&t=day'

        # These two lines determine what timeframe to build out a historical backlog. The 'weeks' parameter
        # in the 'timedelta' function can be modified to scrape as much historical data as required. 
        start_date_dt = datetime.datetime.now()
        end_date_dt = start_date_dt - datetime.timedelta(weeks=1)

        # Inner loop targets the top 100 (ie. all) posts within a specific subreddit per day. The loop
        # breaks once it has traversed back to 'end_date_dt'.
        while start_date_dt > end_date_dt:
            # Converting datetime to unix format.
            before_timestamp = int(start_date_dt.timestamp())
            after_timestamp = int((start_date_dt - datetime.timedelta(days=1)).timestamp())
            
            # Embedding datetime values into the url in proper format.
            url = f'{base_url}&before={before_timestamp}&after={after_timestamp}'

            # Getting the json response data and parsing
            response_data = get_posts(url)
            posts = response_data['data']['children']

            # Below are the target lists we are looking to generate, notice [id, title, sub, ups, ups_ratio, text]
            # will be captured for each post within the set time duration, for each targeted sub.
            post_id = []
            post_title = []
            post_sub = []
            post_ups = []
            post_ups_ratio = []
            post_text = []

            if response_data is None or 'data' not in response_data or 'children' not in response_data['data']:
                print("No more posts found or error in fetching data.")
                break
            
            # For debugging, having issues where API call returns 200 (sucsess) but has an empty values
            if not posts:
                print(f"No posts found for {start_date_dt.strftime('%Y-%m-%d')}.")
                break
            # If response is not empty, appends values to primary lists
            # Likely should be noted that this messy append stuff only exists becuase we need to translate
            # json format to column/row
            else:
                # populating each list with proper data
                for post in posts:
                    post_id.append(post['data']['id'])
                    post_title.append(post['data']['title'])
                    post_sub.append(post['data']['subreddit'])
                    post_ups.append(post['data']['ups'])
                    post_ups_ratio.append(post['data']['upvote_ratio'])
                    post_text.append(post['data'].get('selftext', ''))

            # Creating dataframe from above lists
            data = {
                'id': post_id,
                'title': post_title,
                'subreddit': post_sub,
                'upvotes': post_ups,
                'upvote_ratio': post_ups_ratio,
                'text_body': post_text
            }
            df = pd.DataFrame(data)

            # Pushing to sql, the 'to_sql()' pandas function is quite amazing
            df.to_sql('posts', con=engine, if_exists='append', index=False)
                
            # Moving date range one day backward    
            start_date_dt -= datetime.timedelta(days=1)

            # Respecting reddit API call limits
            time.sleep(1)

            # Inlcuding this print statement for sanity as this takes forever to run
            print(start_date_dt)
if __name__ == '__main__':
    main()