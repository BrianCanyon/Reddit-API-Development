'''
OVERVIEW
The purpose of this script is to process a large amount of text data from reddit. 
Since the underlying data comes from the largest stock related subreddits, the
script will determine if the post is relevant (ie. actually about the market,a stock,
ect.) then execute sentiment analysis against to determine accurcy against real world 
stock data.

ASSUMPTIONS
This script assumes a database table is available named 'posts'. Possible
future itterations of this script could use a .csv dump of this table in
order to remove the need for a DB connection
'''
## Libraries
from sqlalchemy import create_engine, text
import pandas as pd
import yfinance as yf
# from sklearn.feature_extraction.text import TfidfVectorizer # For TF-IDF

## Pulling data from sql to pandas df
engine = create_engine('mysql+mysqlconnector://root:59shredder@localhost/mysql')
query = text('SELECT * FROM posts')
posts_df = pd.read_sql(query, engine)

# The df from the posts table is very raw, below creates a column that determines
# if each post is about a specific stock/crypto/ect., then drops what cant be 
# indentified

# Get list of ticker symbols and names from F500
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
tables = pd.read_html(url)
sp500_table = tables[0]
stock_tickers = sp500_table['Symbol'].to_list()
stock_names = sp500_table['Security'].to_list()
stock_list = stock_tickers + stock_names
stock_list.extend(['BTC', 'Bitcoin'])

# Drop rows that do not relate to a specific F500 stock or have empty text body
indexes_to_keep = set()
for index, row in posts_df.iterrows():
    for stock in stock_list:
        if stock in row['title'] and row['text_body'] != None:
            indexes_to_keep.add(index)

posts_df = posts_df.loc[posts_df.index.isin(indexes_to_keep)]
for title in posts_df['title'][:40]:
    print(title)




            

    



