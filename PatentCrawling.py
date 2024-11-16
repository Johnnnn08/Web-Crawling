import requests
import xml.etree.ElementTree as ET
import csv
def get_patent_info(patent_number):
    # Generate the website URL
    url = f"https://assignment-api.uspto.gov/patent/lookup?query={patent_number}&filter=PatentNumber"

    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve patent info for {patent_number}. Status code: {response.status_code}")
        return {'Patent No.': patent_number, 'issueDate': '', 'patAssigneeName': ''}

    # Parse the XML response
    root = ET.fromstring(response.content)

    # Initialize a dictionary to store the patent info
    patent_info = {'Patent No.': patent_number}

    # Extract the issue date
    issue_date_elements = root.findall(".//arr[@name='issueDate']")
    for issue_date_element in issue_date_elements:
        date_elements = issue_date_element.findall('date')
        if len(date_elements) == 1:
            patent_info['issueDate'] = date_elements[0].text
            break
    else:
        patent_info['issueDate'] = ''

    # Extract the patent assignee name
    assignee_name_element = root.find(".//arr[@name='patAssigneeName']/str")
    if assignee_name_element is not None:
        patent_info['patAssigneeName'] = assignee_name_element.text
    else:
        patent_info['patAssigneeName'] = ''

    return patent_info

def read_csv_file(csv_file):
    patent_numbers = []
    with open(csv_file, 'r', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            patent_numbers.append(row['Patent No.'])
    return patent_numbers
def main():
    csv_file = 'results1105.csv'
    patent_numbers = read_csv_file(csv_file)
    patent_info_list = []

    for patent_number in patent_numbers:
        patent_info = get_patent_info(patent_number)
        patent_info_list.append(patent_info)

    # Now you can write the patent_info_list to a CSV file
    with open('output.csv', 'w', newline='', encoding='utf-8', errors='ignore') as csvfile:
        fieldnames = ['Patent No.', 'issueDate', 'patAssigneeName']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for patent_info in patent_info_list:
            writer.writerow(patent_info)

if __name__ == '__main__':
    main()
