import os
import re
from hometask4 import normalize_paragraph
from datetime import datetime

# the function checks if the file already exists. If so, the file is updated, if not a new file is created
def create_file(name):
    if not os.path.exists(name):
        with open(name, 'w', encoding='utf-8') as f:
            f.write('News feed:\n')
    return name


file_name = create_file('news_feed_task6.txt')


class AddNews():
    def __init__(self,city,news_text,name_file):
        self.city = city
        self.news_text = news_text
        self.name_file = name_file

    def write_news(self):
        current_date = datetime.now() # sets current date
        formatted = current_date.strftime("%d/%m/%Y %H:%M") #formats the date
        with open(self.name_file, "a", encoding="utf-8") as f:
            f.write(f'\nNews_______________\n{self.news_text}\n{self.city}, {formatted}\n') # creates news record in the file


class AddAd():
    def __init__(self,exp_date,ad_text,name_file):
        self.exp_date = exp_date
        self.ad_text = ad_text
        self.name_file = name_file

    def write_ads(self):
        current_date = datetime.now() # sets current date
        deadline = datetime.strptime(self.exp_date, "%Y-%m-%d") # entered exp_date is transformed into datetime object
        remaining_days = deadline - current_date # calculates how many days are left
        with open(self.name_file, "a", encoding="utf-8") as f:
            f.write(f'\nPrivate ad_______________\n{self.ad_text}\nValid until: {self.exp_date}, {remaining_days.days} days\n') # creates ad record in the file


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
        with open(self.name_file, "a", encoding="utf-8") as f:
            f.write(f'\nHoroscope_______________\n---  {self.zodiac_sign}  ---\n{self.hor_text}\nBorn on: {birth_days}\n') # creates horoscope record in the file


class FileRecords:
    def __init__(self, file_record_name='input.txt',
                 default_file_path='/Users/Olga_Romanenko/Desktop/python/epam_training/python_training',
                 output_file=file_name):
        self.default_file_path = default_file_path
        self.file_record_name = file_record_name
        self.output_file = output_file

    def read_records_from_file(self, file_path=None):
        if file_path is None:
            file_path = os.path.join(self.default_file_path, self.file_record_name)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"No {self.file_record_name} found in {self.default_file_path}")

        records = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = [str(normalize_paragraph(p)).strip("[]'") for p in line.split("|")]
                    records.append(parts)

        os.remove(file_path)
        return records

    def process_file_records(self, file_path=None):
        records = self.read_records_from_file(file_path)

        for rec in records:
            feed_type = rec[0].lower()

            if feed_type == "news":
                AddNews(rec[1], rec[2], self.output_file).write_news()

            elif feed_type == "ad":
                AddAd(rec[1], rec[2], self.output_file).write_ads()

            elif feed_type == "horoscope":
                AddHoroscope(rec[1], rec[2], self.output_file).write_horoscope()


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

class SelectInputMode(SelectType,FileRecords):
    def __init__(self):
        input_mode = ''
        while input_mode not in ['manual', 'file']:
            input_mode = input(f"Please select how you'd like to enter the data manual or file: ")

            if input_mode == 'manual':
                processor = SelectType()
                processor.select_feed_type()
            elif input_mode == 'file':
                folder_path = input(f'Please provide the path to the folder with the file (or press Enter to use default): ')

                file_name_input = input(f"Please provide the file name (or press Enter to use default 'input.txt'): ")
                if not folder_path:
                    folder_path = '/Users/Olga_Romanenko/Desktop/python/epam_training/python_training'

                if not file_name_input:
                    file_name_input = 'input.txt'

                processor = FileRecords(file_record_name=file_name_input, default_file_path=folder_path, output_file=file_name)
                processor.process_file_records()


SelectInputMode()
