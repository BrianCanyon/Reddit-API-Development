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

## Pulling data from sql to pandas
engine = create_engine('mysql+mysqlconnector://root:@localhost/mysql')
query = 'SELECT * FROM posts'

posts_df = pd.read_sql(query, engine)
print(posts_df)

