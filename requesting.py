#make requests to tarkov wiki

import requests
from bs4 import BeautifulSoup

search_string = "SA-5"

def search_wiki(search_string):
    tarkov_wiki_base_url = "https://escapefromtarkov.gamepedia.com/Special:Search?search="
    tarkov_wiki = requests.get(f"{tarkov_wiki_base_url}{search_string}", auth=('user','pass'))

    soup = BeautifulSoup(tarkov_wiki.text, 'html.parser')

    is_correct_page = soup.find("meta", property = "og:description")
    # If we searched the exact name of a page, then we are brought directly to it
    if is_correct_page:
        print(f"Here is the wiki page for {search_string} comrade \n{tarkov_wiki_base_url}{search_string}")
    #Otherwize show top x search results
    else:
        #top_results = soup.find_all("div", class_ = "unified-search__result__content")
        top_urls = list()
        for top_result in soup.find_all("a", class_ = "unified-search__result__link"):
            #print(top_result)
            top_urls.append((top_result.get('data-title'),top_result.get('href')))
        num_results = 5
        
        for i in range(num_results):
            print(f"[{top_urls[i][0]}]({top_urls[i][1]})")
        if num_results <= len(top_urls):
            print("")
           # print(f"Here are the top {num_results} results for {search_string} comrade: ",top_urls[:num_results])
        else:
            print("Woah we dont have that many results!")

search_wiki(search_string)