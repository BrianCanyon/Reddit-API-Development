import pandas as pd
from sqlalchemy import create_engine

# Sample data
data = {
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
}

df = pd.DataFrame(data)

# Connection string
engine = create_engine('mysql+mysqlconnector://root:@localhost/mysql')

# Push DataFrame to MySQL
df.to_sql('your_table_name', con=engine, if_exists='replace', index=False)



