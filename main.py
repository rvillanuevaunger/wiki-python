import re
from bs4 import BeautifulSoup
import wikipedia
from stop_words import get_stop_words
from collections import Counter
import pandas as pd

# Get Wikipedia page HTML via API
ws = wikipedia.WikipediaPage('Web scraping')
ws_html = ws.html()

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(ws_html, 'lxml')

# Identify Stopwords
stop_words = list(get_stop_words('en'))

#For each section identify titles, total word counts, and links
for header in soup.find_all(['h1', 'h2', 'h3']): 
    title = header.get_text()  
    title = title[:-6]  
    print(title)  
    for elem in header.next_siblings:  
        if elem.name and elem.name.startswith('h'):
            break
        if elem.name in ('p', 'ul'): 
            text = elem.get_text()  
            words = re.findall(r'\b\w+', text)  
            lower_case = Counter([word.lower() for word in words if not word.lower() in stop_words])  
            df = pd.DataFrame(lower_case.most_common(5)) 
            df.columns = ['words', 'frequency']  
            print(df)  
            for links in elem.find_all('a'): 
                print(links['href'])  
