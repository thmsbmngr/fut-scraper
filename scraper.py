import signal
import sys
import requests
import time
from bs4 import BeautifulSoup

#Handling ctrl+c press
def signal_handler(sig, frame):
    print("Ctrl+C pressed")
    print("Exiting application...")
    soup.clear()
    page.close()
    file.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

URL = 'https://www.futbin.com/players?page='
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

#Getting last page number
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
nav = soup.find_all(name="li", attrs={"class": "page-item"})
#nav[5] is the list item with the last page number in
pages = int(nav[5].get_text())

csv_header = "id;name;rating;pace;shooting;passing;dribbling;defending;physicality\n"
open("players.csv", "w", encoding="utf-8").close()
file = open("players.csv", "a", encoding="utf-8")
file.write(csv_header)

for page_num in range(1, pages + 1):
    page_url = URL + str(page_num)
    page = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    table_1 = soup.find_all(name="tr", attrs={"class": "player_tr_1"})
    table_2 = soup.find_all(name="tr", attrs={"class": "player_tr_2"})

    table = table_1 + table_2

    print("Scraping " + str(page_num) + " page")
    for row in range(0, len(table)):
        if row % 20 == 0:
            time.sleep(1)
        player_data = []
        
        data = table[row].findChildren(name="td")

        # Getting name and id of the player-card the a element from futbin
        player_a_element = data[0].findChild(name="a", attrs={"class": "player_name_players_table"})
        player_url = player_a_element['href']
        player_id = player_url.split("/")[3]
        player_name = player_a_element.get_text()
        player_data.append(player_id)
        player_data.append(player_name)

        # Getting overall rating of player
        rating = data[1].findChild(name="span").get_text()
        player_data.append(rating)

        # Getting the stats of the player
        # pace: 8, shooting: 9, passing: 10, dribbling: 11, defending: 12, physicality: 13
        pace = 8
        physicality = 13
        for stat_num in range(pace, physicality):
            stat = data[stat_num].findChild(name="span").get_text()
            player_data.append(stat)

    
        player_string = ";".join(player_data)
        file.write(player_string + "\n")

    soup.clear()
    page.close()

file.close()