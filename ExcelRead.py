import pandas as pd
from WebCrawlingTest import extract_data

# Read the CSV file
df = pd.read_csv('Data.csv', encoding='gbk', encoding_errors='ignore')

# Store the data in the "document_number" column in a variable
data = df['document_number'].tolist()

# Create an empty list to store the results
results_list = []

# Read one value at a time from the data list
for document_id in data:
    print(document_id)
    results = extract_data(document_id)
    
    # If results is None, create a dictionary with None values
    if results is None:
        results = {'document_id': document_id}
        # Add None values for all other columns
        # You can replace this with the actual column names
        for key in ['Product Name', 'Patent No.', 'Company', 'Reg Rev Period', 'Testing Phase', 'Approval Phase', 'IND/IDE Filing Date', 'NDA/PMA Filing Date', 'Approval Date', 'Application No.', 'Pat term ext']:
            results[key] = None
    else:
        # Add the document_id to the results dictionary
        results['document_id'] = document_id
    
    # Append the results to the results list
    results_list.append(results)

# Convert the results list to a DataFrame
results_df = pd.DataFrame(results_list)

# Write the results DataFrame to a CSV file
results_df.to_csv('Results.csv', index=False)