from bs4 import BeautifulSoup
import lxml
import requests
import pandas as pd 
import os

dirname = os.path.dirname(__file__)
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
YEARS = [2022]
POSITIONS = ["QB", "RB", "WR", "TE", "K", "DST"]


def football_db_scraper_weekly():
  columns =  ['Name', 'Position', 'Year', 'Week', 'Rank', 'Team', 'Standard Pts', 'Pass_Att', 'Pass_Cmp', 'Pass_Yds', 'Pass_TD', 'Int', 'Pass_2Pt', 'Rush_Att', 'Rush_Yds', 'Rush_TD', 'Rush_2Pt', 'Rec', 'Rec_Yds', 'Rec_TD', 'Rec_2Pt', 'FL', 'FL_TD', 'Half PPR Pts', 'PPR Pts', 'XPA', 'XPM', 'FGA', 'FGM', '50_Plus', 'DST_Sack', 'DST_Int', 'DST_Saf', 'DST_FR', 'DST_Blk', 'DST_TD', 'DST_PA', 'DST_Pass_Yds', 'DST_Rush_Yds', 'DST_Tot_Yds']
  df = pd.DataFrame(columns = columns)
  for year in YEARS:
    if year >= 2022:
      end = 19
    else:
      end = 18
    for week in range(1, end):
      for pos in POSITIONS: 
        url = "https://www.footballdb.com/fantasy-football/index.html?pos=" + pos + "&yr=" + str(year) + "&wk=" + str(week) + "&key=b6406b7aea3872d5bb677f064673c57f"
        source = requests.get(url, headers = HEADERS) 
        soup = BeautifulSoup(source.text, 'lxml')
        table = soup.find( "table", {"class":"statistics scrollable"} ).findAll("tr")
        if pos != "K" and pos != "DST":
          for index in range(2,len(table)):
            row = table[index]
            name = row.find("a").get_text()
            rank = index-1
            line = [name, pos, year, week, rank]
            row_data = row.find_all("td")
            for ind in range(len(row_data)):
              if ind == 1:
                line.append(row_data[ind].find("b").get_text())
              if ind == 2:
                line.append(float(row_data[ind].get_text()))
              if ind > 2:
                line.append(int(row_data[ind].get_text()))
            points = weekly_rec_pts(line)
            line.append(points[0])
            line.append(points[1])
            while len(line) < len(columns):
              line.append(0)
            df.loc[len(df)] = line

        if pos == "K":
          for index in range(1,len(table)):
            row = table[index]
            name = row.find("a").get_text()
            rank = index-1
            line = [name, pos, year, week, rank]
            row_data = row.find_all("td")
            for ind in range(len(row_data)):
              if ind == 1:
                line.append(row_data[ind].find("b").get_text())
              if ind == 2:
                line.append(float(row_data[ind].get_text()))
                for i in range(16):
                  line.append(0)
                line.append(line[6])
                line.append(line[6])
              if ind > 2:
                line.append(int(row_data[ind].get_text()))
            while len(line) < len(columns):
              line.append(0)
            df.loc[len(df)] = line

        if pos == "DST":
          for index in range(1,len(table)):
            row = table[index]
            name = row.find("a").get_text()
            rank = index-1
            line = [name, pos, year, week, rank]
            row_data = row.find_all("td")
            for ind in range(len(row_data)):
              if ind == 1:
                line.append(row_data[ind].find("b").get_text())
              if ind == 2:
                line.append(float(row_data[ind].get_text()))
                for i in range(16):
                  line.append(0)
                line.append(line[6])
                line.append(line[6])
                for i in range(5):
                  line.append(0)
              if ind == 3:
                line.append(float(row_data[ind].get_text()))
              if ind > 3:
                line.append(int(row_data[ind].get_text()))
            df.loc[len(df)] = line     

  df.to_csv(dirname + '\\'+'weekly_data.csv')

def football_db_scraper_yearly():
  df_weekly = pd.read_csv(dirname + '\\' + 'weekly_data.csv') 
  columns =  ['Name', 'Position', 'Year', 'Rank', 'Standard Pts', 'Pass_Att', 'Pass_Cmp', 'Pass_Yds', 'Pass_TD', 'Int', 'Pass_2Pt', 'Rush_Att', 'Rush_Yds', 'Rush_TD', 'Rush_2Pt', 'Rec', 'Rec_Yds', 'Rec_TD', 'Rec_2Pt', 'FL', 'FL_TD', 'Half PPR Pts', 'PPR Pts', 'XPA', 'XPM', 'FGA', 'FGM', '50_Plus', 'DST_Sack', 'DST_Int', 'DST_Saf', 'DST_FR', 'DST_Blk', 'DST_TD', 'DST_PA', 'DST_Pass_Yds', 'DST_Rush_Yds', 'DST_Tot_Yds', 'Team']
  df = pd.DataFrame(columns = columns)
  for year in YEARS:
    for pos in POSITIONS:
      url = "https://www.footballdb.com/fantasy-football/index.html?pos=" + pos + "&yr=" + str(year) + "&wk=all&key=b6406b7aea3872d5bb677f064673c57f"
      source = requests.get(url, headers = HEADERS) 
      soup = BeautifulSoup(source.text, 'lxml')
      table = soup.find( "table", {"class":"statistics scrollable"} ).findAll("tr")     
      if pos != "K" and pos != "DST":
        for index in range(2,len(table)):
          row = table[index]
          name = row.find("a").get_text()
          rank = index-1
          line = [name, pos, year, rank]
          row_data = row.find_all("td")
          for ind in range(len(row_data)):
            if ind == 2:
              text = row_data[ind].get_text().replace(',','')
              line.append(float(text))
            if ind > 2:
              text = row_data[ind].get_text().replace(',','')
              line.append(int(text))
          points = yearly_rec_pts(line)
          line.append(points[0])
          line.append(points[1])
          while len(line) < len(columns)-1:
            line.append(0)

          team = find_team(line, df_weekly)
          line.append(team)
          df.loc[len(df)] = line

      if pos == "K":
        for index in range(1,len(table)):
          row = table[index]
          name = row.find("a").get_text()
          rank = index-1
          line = [name, pos, year, rank]
          row_data = row.find_all("td")
          for ind in range(len(row_data)):
            if ind == 2:
              text = row_data[ind].get_text().replace(',','')
              line.append(float(text))
              for i in range(16):
                line.append(0)
              line.append(line[6])
              line.append(line[6])
            if ind > 2:
              text = row_data[ind].get_text().replace(',','')
              line.append(int(text))
          while len(line) < len(columns)-1:
            line.append(0)
          team = find_team(line, df_weekly)
          line.append(team)
          df.loc[len(df)] = line

      if pos == "DST":
        for index in range(1,len(table)):
          row = table[index]
          name = row.find("a").get_text()
          rank = index-1
          line = [name, pos, year, rank]
          row_data = row.find_all("td")
          for ind in range(len(row_data)):
            if ind == 2:
              text = row_data[ind].get_text().replace(',','')
              line.append(float(text))
              for i in range(16):
                line.append(0)
              line.append(line[6])
              line.append(line[6])
              for i in range(5):
                line.append(0)
            if ind == 3:
              text = row_data[ind].get_text().replace(',','')
              line.append(float(text))
            if ind > 3 and ind < 10:
              text = row_data[ind].get_text().replace(',','')
              line.append(int(text))
            if ind >= 10:
              text = row_data[ind].get_text().replace(',','')
              line.append(float(text))  
          team = find_team(line, df_weekly)
          line.append(team)            
          df.loc[len(df)] = line     
  df.to_csv(dirname + '\\'+'yearly_data.csv')

def find_team(line, df_weekly):
  name = line[0]
  position = line[1]
  team = df_weekly[(df_weekly['Position']==position) & (df_weekly['Name']==name)]['Team'].unique()[0]
  return team

def weekly_rec_pts(line):
  std_pts = line[6]
  rec = line[17]
  return (std_pts + .5*rec, std_pts + rec)

def yearly_rec_pts(line):
  std_pts = line[4]
  rec = line[15]
  return (std_pts + .5*rec, std_pts + rec)

#football_db_scraper_weekly()
#football_db_scraper_yearly()
