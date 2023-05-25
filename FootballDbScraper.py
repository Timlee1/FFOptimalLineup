from bs4 import BeautifulSoup
import lxml
import requests
import pandas as pd 
import os

dirname = os.path.dirname(__file__)
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

def football_db_scraper_qb():
    year = 2022
    week = 1 
    pos = "QB"
    url = "https://www.footballdb.com/fantasy-football/index.html?pos=" + pos + "&yr=" + str(year) + "&wk=" + str(week) + "&key=b6406b7aea3872d5bb677f064673c57f"
    source = requests.get(url, headers = HEADERS) 
    soup = BeautifulSoup(source.text, 'lxml')
    table = soup.find( "table", {"class":"statistics scrollable"} )
    columns =  ['Name', 'Position', 'Year', 'Week', 'Rank', 'Pass_Att', 'Pass_Cmp', 'Pass_Yds', 'Pass_TD', 'Int', 'Pass_2Pt', 'Rush_Att', 'Rush_Yds', 'Rush_TD', 'Rush_2Pt', 'Rec', 'Rec_Yds', 'Rec_TD', 'Rec_2Pt', 'FL', 'FL_TD']
    df = pd.DataFrame(columns = columns)
    
    table = table.findAll("tr")
    for index in range(len(table)):
        
        if index >= 2:
          row = table[index]
          name = row.find("a").get_text()
          rank = index-2
          line = [name, 'QB', year, week, rank]
          row_data = row.find_all("td")
          for ind in range(len(row_data)):
            if ind > 2:
              line.append(int(row_data[ind].get_text()))
          df.loc[len(df)] = line
          print(df)
          break 


    

football_db_scraper_qb()