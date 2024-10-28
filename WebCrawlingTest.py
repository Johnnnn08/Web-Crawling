import requests
from bs4 import BeautifulSoup

def extract_data(document_id):
    api_url = f"https://www.federalregister.gov/api/v1/documents/{document_id}"

    response = requests.get(api_url)

    if response.status_code == 200:
        document_data = response.json()
        html_url = document_data["body_html_url"]
        html_response = requests.get(html_url)
        if html_response.status_code == 200:
            soup = BeautifulSoup(html_response.text, "html.parser")
            text = soup.get_text()
            # Define the keywords to search for
            keywords = {
                "Product Name": {"keyword": "FDA recently approved for marketing the human drug product",
                                 "offset": len("FDA recently approved for marketing the human drug product"),
                                 "end_char": ")"},
                "Patent No.": {"keyword": "(U.S. Patent No.", "offset": 0, "end_char": ")"},
                "Company": {"keyword": ") from", "offset": len(") from"), "end_char": "."},
                "Reg Rev Period": {"start_keyword": "FDA has determined that the applicable regulatory review period for",
                                   "end_keyword": " days"},
                "Testing Phase": {"start_keyword": "Of this time,", "end_keyword": "days"},
                "Approval Phase": {"start_keyword": "regulatory review period, while", "end_keyword": "days"},
                "IND/IDE Filing Date": {"keyword": "investigational new drug application became effective was on",
                                        "offset": len("investigational new drug application became effective was on"),
                                        "end_char": "."},
                "NDA/PMA Filing Date": {"keyword": "human drug product under section 505(b) of the act: ",
                                        "offset": len("human drug product under section 505(b) of the act: "),
                                        "end_char": "."},
                "Approval Date": {"keyword": "was approved on ", "offset": len("was approved on "), "end_char": "."},
                "Application No.": {"start_keyword": "FDA has verified the applicant's claim that", "end_keyword": "was"},
                "Pat term ext": {"start_keyword": "In its application for patent extension, this applicant seeks ",
                                 "end_keyword": "days"}
            }

            # Create an empty dictionary to hold the results
            results = {}

            # Loop over the text to find the keywords
            for key, keyword_data in keywords.items():
                if "start_keyword" in keyword_data:
                    start_index = text.find(keyword_data["start_keyword"])
                    if start_index != -1:
                        end_index = text.find(keyword_data["end_keyword"], start_index + len(keyword_data["start_keyword"]))
                        if end_index != -1:
                            value = text[start_index + len(keyword_data["start_keyword"]):end_index].strip()
                            if key in ["Reg Rev Period", "Testing Phase", "Approval Phase", "Pat term ext"]:
                                value = ''.join(filter(str.isdigit, value))
                            results[key] = value
                else:
                    start_index = text.find(keyword_data["keyword"])
                    if start_index != -1:
                        end_index = text.find(keyword_data["end_char"], start_index + keyword_data["offset"])
                        if end_index != -1:
                            results[key] = text[start_index + len(keyword_data["keyword"]):end_index].strip()

            return results
        else:
            print(f"Error retrieving HTML: {html_response.status_code}")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage:
document_id = "94-4802"
results = extract_data(document_id)
if results is not None:
    print(results)
