import os
from datetime import datetime

# the function checks if the file already exists. If so, the file is updated, if not a new file is created
def create_file(file_name):
    if os.path.exists(file_name):
        return open(file_name, 'a+')
    else:
        f = open(file_name, 'w+')
        f.write('News feed:')
        return f

file_name = create_file('news_feed.txt')


class AddNews():
    def __init__(self,city,news_text,name_file):
        self.city = city
        self.news_text = news_text
        self.name_file = name_file

    def write_news(self):
        current_date = datetime.now() # sets current date
        formatted = current_date.strftime("%d/%m/%Y %H:%M") #formats the date
        self.name_file.write(f'\nNews_______________\n{self.news_text}\n{self.city}, {formatted}\n') # creates news record in the file


class AddAd():
    def __init__(self,exp_date,ad_text,name_file):
        self.exp_date = exp_date
        self.ad_text = ad_text
        self.name_file = name_file

    def write_ads(self):
        current_date = datetime.now() # sets current date
        deadline = datetime.strptime(self.exp_date, "%Y-%m-%d") # entered exp_date is transformed into datetime object
        remaining_days = deadline - current_date # calculates how many days are left
        self.name_file.write(f'\nPrivate ad_______________\n{self.ad_text}\nValid until: {self.exp_date}, {remaining_days.days} days\n') # creates ad record in the file


sign_month = {'Aries':'March 21 – April 19','Taurus':'April 20 – May 20','Gemini':'May 21 – June 20','Cancer':'June 21 – July 22','Leo':'July 23 – August 22','Virgo':'August 23 – September 22','Libra':'September 23 – October 22','Scorpio':'October 23 – November 21','Sagittarius':'November 22 – December 21','Capricorn':'December 22 – January 19','Aquarius':'January 20 – February 18','Pisces':'February 19 – March 20'}

class AddHoroscope():
    def __init__(self,zodiac_sign,hor_text,name_file):
        self.zodiac_sign = zodiac_sign
        self.hor_text = hor_text
        self.name_file = name_file

    def write_horoscope(self):
        birth_days = 'Unknown date'
        for key, value in sign_month.items(): # goes through the dictionary and check if the entered sign exists there. If so, assigns value to the variable
            if self.zodiac_sign.lower() == key.lower():
                birth_days = value
                break
        self.name_file.write(f'\nHoroscope_______________\n---  {self.zodiac_sign}  ---\n{self.hor_text}\nBorn on: {birth_days}\n') # creates horoscope record in the file


class SelectType(AddNews,AddAd,AddHoroscope):
    def __init__(self):
        pass

    def select_feed_type(self):

        feed_type = ''
        while feed_type not in ['news', 'ad', 'horoscope']: # input will appear until one of the requested values is enetered
            feed_type = input("Please select what you'd like to add: news, ad or horoscope: " )
# checks what value is entered. depending on the value asks for other inputs and add a record to the file
        if feed_type.lower() == 'news':
            user_entered_city = input('Please enter the city the news is from: ')
            user_entered_text = input("Please enter the text of the news: ")
            news = AddNews(user_entered_city, user_entered_text, file_name)
            news.write_news()

        elif feed_type.lower() == 'ad':
            user_entered_exp_date = input('Please enter the expiration date: ')
            user_entered_text = input("Please enter the text of the ad: ")
            ad = AddAd(user_entered_exp_date, user_entered_text, file_name)
            ad.write_ads()

        else:
            user_entered_sign = input('Please enter zodiac sign: ')
            user_entered_text = input("Please enter the text of the horoscope: ")
            horoscope = AddHoroscope(user_entered_sign, user_entered_text, file_name)
            horoscope.write_horoscope()


a = SelectType()
a.select_feed_type()






