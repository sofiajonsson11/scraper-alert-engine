from bs4 import BeautifulSoup

def parse_example_page(html):
    soup = BeautifulSoup(html, "lxml")

    #Example extraction ( change based on actual page structure)
    title = soup.find("h1").get_text(strip=True)
    price = None #Add as needed

    return {
        "title": title,
        "price": price
    }   