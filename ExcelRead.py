import pandas as pd

# Function to read the XLSX file
def read_xlsx_file(file_name, column_name):
    try:
        # Attempt to read the XLSX file
        data = pd.read_excel(file_name, usecols=[column_name])
        return data
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return None
    except KeyError:
        print(f"The '{column_name}' column does not exist in the Excel file.")
        return None
    except Exception as e:
        print(f"Error reading file {file_name}: {str(e)}")
        return None

# Usage example
file_name = 'data.xlsx'  # Replace 'data.xlsx' with your XLSX file name
column_name = 'document_number'  # Replace 'document_number' with your column name
data = read_xlsx_file(file_name, column_name)

if data is not None:
    print(data)  # Print the 'document_number' column
