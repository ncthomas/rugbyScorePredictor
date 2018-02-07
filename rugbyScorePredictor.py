__author__ = 'niclas'

from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np

class myPredictor:
    
    def __init__(self, url_address):
        
        self.url_address = url_address
    

    def get_url_content(self):
        
        driver = webdriver.Chrome()
        driver.get(self.url_address)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close()

        return soup

    def get_url_teams(self, soup):
        
        teams = soup.findAll("span", {"class":"fixtures-bet-name"})

        return teams

    def get_url_odds(self, soup):
        
        odds = soup.findAll(lambda tag: tag.name == 'span' and  tag.get('class') == ['odds'])

        return odds

    def get_teams_and_odds(self, teams, odds):
        
        teamnames = []
        fracs = []

        for odd, team in zip(odds, teams):

            if team.contents[0] != 'Draw':

                frac = odd.contents[0].split("(")[1].split(")")[0]
                numerator, denominator = int(frac.split("/")[0]), int(frac.split("/")[1])

                teamnames.append(team.contents[0])
                fracs.append(numerator/denominator)

        return teamnames, fracs

    def get_predictions(self, teamnames, fracs):
        
        for i in np.arange(0,len(teamnames),2):

            team1 = teamnames[i]
            team2 = teamnames[i+1]

            fracsteam1 = fracs[i]
            fracsteam2 = fracs[i+1]

            print(team1, "vs", team2, ":")

            if fracsteam1 <= fracsteam2:
                print(team1, "to win by", int(2*fracsteam2))
            else:
                print(team2, "to win by", int(2*fracsteam1))

            print("")

if __name__ == '__main__':
    
    predict = myPredictor("https://www.oddschecker.com/rugby-union/internationals")
    soup = predict.get_url_content()
    teamnames = predict.get_url_teams(soup)
    odds = predict.get_url_odds(soup)
    teamnames, fracs = predict.get_teams_and_odds(teamnames, odds)
    predict.get_predictions(teamnames, fracs)
