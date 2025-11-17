import requests

def fetch_html(url):
    """
    Fetches the HTML content of the given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the page.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise an error for bad responses
    return response.text