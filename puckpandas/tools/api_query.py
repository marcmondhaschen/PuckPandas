import requests


# generic call to some nhl api query
# returns formatted json
def fetch_json_data(url):
    """
    Fetches JSON responses from the inputted URL. Anticipates

    Parameters: url - The web address to attempt to fetch a JSON response from

    Returns: json_data - The formatted JSON response
    """
    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
    else:
        json_data = {}

    return json_data
