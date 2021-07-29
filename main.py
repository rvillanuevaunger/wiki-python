# Import packages
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

"""
Extract Text from Wikipedia Page
 I. Section Titles
   1. Identify section titles
   2. Extract title text
   3. Remove trailing characters
   4. Print section title
   5. Stop at next header
 II. Word Counts by Section
   6. Use section titles to identify section content (paragraphs and lists)
   7. Extract section content
   8. Separate individual words
   9. Convert to lower case, count instances, and remove stopwords
   10. Create dataframe
   11. Add dataframe column titles
   12. Print dataframe of 5 most common words for section content
 III. Links in Section
   13. Identify links within content
   14. Print links
"""

for header in soup.find_all(['h1', 'h2', 'h3']):  # 1.
    title = header.get_text()  # 2.
    title = title[:-6]  # 3.
    print(title)  # 4.
    for elem in header.next_siblings:  # 5.
        if elem.name and elem.name.startswith('h'):
            break
        if elem.name in ('p', 'ul'):  # 6.
            text = elem.get_text()  # 7.
            words = re.findall(r'\b\w+', text)  # 8.
            lower_case = Counter([word.lower() for word in words if not word.lower() in stop_words])  # 9.
            df = pd.DataFrame(lower_case.most_common(5)) # 10.
            df.columns = ['words', 'frequency']  # 11.
            print(df)  # 12.
            for links in elem.find_all('a'):  # 13.
                print(links['href'])  # 14.
