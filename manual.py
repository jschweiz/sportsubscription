import requests
import sys
from bs4 import BeautifulSoup
import time
import config
import json

def find_url(groups, _date, _hour):
    for group in groups:
        date = group.find('span', attrs={'class' : 'day'}).contents[0]
        hour = group.find('span', attrs={'class' : 'hour'}).contents[0]
        if date == _date and hour == _hour:
            full_button = group.find('div', attrs={'class': 'full'})
            if full_button != None:
                return config.FULL_TRAINING
            closed_button = group.find('div', attrs={'class': 'close'})
            if closed_button != None:
                return config.CLOSED_TRAINING
            inscription_button = group.find('a', attrs={'class': 'btn_insc'})
            if inscription_button != None:
                return inscription_button['href']
            already_sub_button = group.find('a', attrs={'class': 'in'})
            if already_sub_button != None:
                return config.ALREADY_SUB
    return config.NO_TRAINING

def find_sport(name, sports):
    for s in sports['sports']:
        if s['sport'] == name:
            return s
    return None

def find_hour(nickname, sport):
    for d in sport['dates']:
        if d['name'] == nickname:
            return d
    return None


def main(data, context):

    pple_str = "{\"students\" : [{ \"username\" : \"%s\",\"password\": \"%s\",\"wanted_trainings\": [{\"sport\": \"%s\",\"dates\": [\"%s\"]}]}]}" % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    print(pple_str)
    people = json.loads(pple_str)

    with open('sports.json') as f:
        sports = json.load(f)
    
    for person in people['students']:

        
        subscribed = False
        while subscribed == False:

            time.sleep(10)

            # Connect with account
            s = requests.Session()
            s.post(config.connection_url, data={'txtLogin' : person['username'], 'txtPassword': person['password']})
            print("--> Connected to the account %s" % person['username'])


            for training in person['wanted_trainings']:

                sport_name = training['sport']
                sport = find_sport(sport_name, sports)
                if sport == None:
                    print('--> Sport %s not found' % sport_name)
                    continue
                url = sport['url']

                for date_nickname in training['dates']:

                    date = find_hour(date_nickname, sport)
                    if date == None:
                        print('--> Training on %s for %s not found' % (date_nickname, sport_name))
                        continue

                    # Looking for all available trainings
                    html = s.get(url).content
                    groups = BeautifulSoup(html, features="html.parser").find_all('div', attrs={'class' : 'group'})

                    # Find the appropriate one
                    d = date['date']
                    h =  date['hour']
                    partial_url = find_url(groups, d, h)

                    if partial_url == config.NO_TRAINING:
                        print('--> No %s training found for %s:%s. Aborting subscription' % (sport_name, d, h))
                        continue
                    elif partial_url == config.ALREADY_SUB:
                        print('--> Already subscribed to %s:%s:%s' %(sport_name,d, h))
                        continue
                    elif partial_url == config.FULL_TRAINING:
                        print('--> Training %s:%s:%s is already full. Try earlier next time' % (sport_name,d, h))
                        continue
                    elif partial_url == config.CLOSED_TRAINING:
                        print('--> Training %s:%s:%s is still closed. Try later' % (sport_name,d, h))
                        continue

                    training_url = config.base_url + partial_url
                    # print('--> Trying to subscribe on %s:%s' % (d, h))

                    # Subscribing on the page
                    soup = BeautifulSoup(s.get(training_url).content, features="html.parser")
                    soup.find('button', attrs={'class':'shop_cours_info add'})
                    data = {
                        'groupe_nom': '',
                        'quantity': '-',
                        'confirm_valid': 1,
                        'type': 1
                    }
                    s.post(url=training_url + '#form', data=data)
                    print('--> Subscribed to the sport training %s:%s' % (d, h))
                    subscribed = True

        s.close()


if __name__ == "__main__":
    main('data', 'context')