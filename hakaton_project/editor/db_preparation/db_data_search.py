import requests
from bs4 import BeautifulSoup
import time

# Define custom headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
}

def fetch_latex_from_page(url, retries=3):
    """
    Fetches LaTeX content from a specified URL by sending an HTTP GET request.

    Attempts to retrieve the content from a webpage by parsing the HTML for a
    <textarea> element with the name 'tex'. If found, returns the stripped text
    content. Retries the request up to a specified number of times in case of
    failure, with a delay between attempts.

    Args:
        url (str): The URL of the webpage to fetch the LaTeX content from.
        retries (int, optional): The number of retry attempts in case of failure.
            Defaults to 3.

    Returns:
        str or None: The LaTeX content if found, otherwise None.
    """
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS)
            
            if response.status_code == 200:
                page_content = response.text
                
                soup = BeautifulSoup(page_content, 'html.parser')

                textarea = soup.find('textarea', {'name': 'tex'})
                if textarea:
                    return textarea.get_text(strip=True)

                return None

            else:
                print(f"Failed to retrieve content from {url} with status code {response.status_code}")
                break

        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed to retrieve {url}: {e}")
            time.sleep(2)

    return None

def scrape_latex_from_site(base_url, page_links):
    """
    Scrapes LaTeX formulas from a list of webpage links.

    Iterates over a list of page links, constructs the full URL for each link,
    and retrieves LaTeX content using the fetch_latex_from_page function. 
    Collected LaTeX formulas are stored in a list, which is returned at the end.

    Args:
        base_url (str): The base URL to prepend to each page link.
        page_links (list of str): A list of relative page links to scrape.

    Returns:
        list of str: A list containing all the LaTeX formulas found on the pages.
    """
    all_latex_formulas = []
    
    for link in page_links:
        full_url = base_url + link
        latex_formula = fetch_latex_from_page(full_url)
        if latex_formula:
            all_latex_formulas.append(latex_formula)
            print(len(all_latex_formulas))
        time.sleep(1)
    
    return all_latex_formulas