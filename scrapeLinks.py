from bs4 import BeautifulSoup
from rapidfuzz import fuzz, process

def extract_links(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    # soup = html_content
    divs = soup.find_all('div', class_='col')
    # a = soup.find_all('div', class_='col').find_parent('div').find_previous_sibling('a')
    a=[]
    for div in divs:
        parent = div.parent.parent
        links = parent.get('href')
        a.append(links)
    # print(a)
    div_text = [d.find_next('div').get_text(separator="\n") for d in divs]
    # div[0] = div[0].get_text(separator="\n")
    # print(div)
    # links = [div.get('href') for div in soup.find_all('div', class="col")]
    return div_text,a

def find_correct_link(div_text,links,query):
    best_match = process.extractOne(query, div_text)
    # print(best_match[0])
    # print("\n\n")
    # print(links.index(best_match[0]))
    index = div_text.index(best_match[0])
    return links[index]


# a = find_correct_link(div_text, links, "Vivo X70 Pro 256GB")
# print(a)