import pandas as pd
import json
# Read JSON data from file
with open('users.json', 'r') as file:
    json_data = json.load(file)

# Convert JSON to DataFrame
df = pd.DataFrame.from_dict(json_data, orient='index')

# Write DataFrame to Excel
df.to_excel('rv.xlsx', index_label='User ID')
