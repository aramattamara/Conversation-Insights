#To Access OS environmental variables
import os

# Library for API calls
import requests
from model import Message, User, connect_to_db, db

bot_key = os.environ['API_BOT_KEY']

def get_updates():
    print(bot_key)
    
    response = requests.get('https://api.telegram.org/bot' + bot_key + '/getUpdates')

    return response.json()

def get_text():
    text = get_updates()
    mm = []
    for u in text['result']:
        m = Message(u['message']['text'])
        mm.append(m)
    db.session.add(mm)
    db.session.commit()

# import schedule
# if __name__ == '__main__':
    # # schedule.every(30).seconds.do(get_text)
    # while True:
    #     # schedule.run_pending()
    #     get_text()
    #     sleep(30)
    

foo = Message(text = "hello")
db.session.add(foo)
db.session.commit()