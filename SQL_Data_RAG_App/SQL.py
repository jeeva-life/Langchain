import os
# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
# from langchain.sql_database import SQLDatabase
from langchain_community.utilities import SQLDatabase  # Updated import
import urllib.parse
# from langchain_community.chains import create_sql_query_chain
# from langchain.chains import SQLDatabaseChain
from langchain_experimental.sql import SQLDatabaseChain







# Load the API key from environment variables
open_api_key = os.getenv("OPEN_API_KEY")

if open_api_key:
    print(f"Loaded API Key: {open_api_key}")
else:
    print("Error: OPEN_API_KEY not found in environment variables.")


llm = ChatOpenAI(temperature=0, openai_api_key = open_api_key)

host = "localhost"
port = "3306"
username = "root"
database_name = "college"

password = os.getenv("SQL_PASS_KEY")
# URL encode the password to handle special characters
encoded_password = urllib.parse.quote(password.encode('utf-8'))


# Step 2: Connect to the database
connection_uri = f"mysql+mysqlconnector://{username}:{encoded_password}@{host}:{port}/{database_name}"
# Debugging: Print the connection URI (optional, for debugging only)
print(f"Connection URI: {connection_uri}")

# Connect to the database
db = SQLDatabase.from_uri(connection_uri, sample_rows_in_table_info=2)


# Step 4: Rebuild SQLDatabaseChain
SQLDatabaseChain.model_rebuild()

# Step 5: Create the SQLDatabaseChain
chain = SQLDatabaseChain.from_llm(llm, db)

# chain = create_sql_query_chain(llm,db)
# chain = SQLDatabaseChain.from_llm(llm, db)


print(db.dialect)
print(db.get_usable_table_names())
db.run("SELECT count(*) FROM course LIMIT 10;")


response = chain.invoke({"question": "How many courses are there"})
print("response")

db.run(response)

