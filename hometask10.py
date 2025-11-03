import os
import re
import csv
import json
from collections import  Counter
import string
from re import findall
import xml.etree.ElementTree as ET
import sqlite3
import pyodbc

from hometask4 import normalize_paragraph
from datetime import datetime

# the function checks if the file already exists. If so, the file is updated, if not a new file is created
def create_file(name):
    if not os.path.exists(name):
        with open(name, 'w', encoding='utf-8') as f:
            f.write('News feed:\n')
    return name


file_name = create_file('news_feed_task9.txt')

class WritingIntoDB:
    def __init__(self, db_name="task10.db"):
        with pyodbc.connect("Driver={SQLite3};Database=" + db_name + "") as self.connection:
            self.cursor = self.connection.cursor()
        self.add_tables()

    def add_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS news
                   (id INTEGER PRIMARY KEY, 
                   city TEXT,
                   date TEXT,
                   news_text TEXT)""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS ad
                   (id INTEGER PRIMARY KEY,
                    date DATE,
                    expires_in_days INTEGER,
                    ad_text TEXT)""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS horoscope
                  (id INTEGER PRIMARY KEY,
                   sign TEXT,
                   birth_dates TEXT,
                   horo_text TEXT)""")

        self.connection.commit()

    def insert_news(self, city, date, news_text):
        self.cursor.execute("""SELECT COUNT (*) FROM news
            WHERE city = ? AND date = ? AND news_text = ?""",
                            (city, date, news_text))

        result = self.cursor.fetchone()[0]

        if result == 0:
            self.cursor.execute("""INSERT INTO news (city, date, news_text) VALUES (?, ?, ?)""",
                                (city, date, news_text))
            self.connection.commit()
            print(f"News added")
        else:
            print("Duplicate news skipped")


    def add_horoscope(self, zodiac_sign, birth_dates, horo_text):
        self.cursor.execute("""SELECT COUNT(*) FROM horoscope 
        WHERE sign=? AND birth_dates=? AND horo_text=?""",
                            (zodiac_sign, birth_dates, horo_text))

        result = self.cursor.fetchone()[0]

        if result == 0:
            self.cursor.execute("""INSERT INTO horoscope (sign, birth_dates, horo_text) VALUES (?, ?, ?)""",
                                    (zodiac_sign, birth_dates, horo_text))

            self.connection.commit()
            print(f"Horo added")
        else:
            print("Duplicate horo skipped")


    def add_ad(self, exp_date, days_left, ad_text):
        self.cursor.execute("""SELECT COUNT(*) FROM ad WHERE date=? AND expires_in_days=? AND ad_text=?""",
                            (exp_date, days_left, ad_text))

        result = self.cursor.fetchone()[0]

        if result == 0:
            self.cursor.execute("""INSERT INTO ad (date, expires_in_days, ad_text) VALUES (?, ?, ?)""",
                                (exp_date, days_left, ad_text))

            self.connection.commit()
            print(f"Ad added")
        else:
            print("Duplicate news skipped")

    def close(self):
        self.cursor.close()


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

        db = WritingIntoDB()
        db.insert_news(self.city, formatted, self.news_text)
        db.close()


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

        db = WritingIntoDB()
        db.add_ad(self.exp_date, remaining_days.days, self.ad_text)
        db.close()


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

        db = WritingIntoDB()
        db.add_horoscope(self.zodiac_sign, birth_days, self.hor_text)
        db.close()


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

class JsonRecords:
    def __init__(self, file_record_name='input.json',
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
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format in {self.file_record_name}: {e}")

        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            raise ValueError("JSON file must contain a list or a single record object")

        os.remove(file_path)
        return data

    def process_file_records(self, file_path=None):
        records = self.read_records_from_file(file_path)

        for rec in records:
            feed_type = rec.get("type", "").lower()

            if feed_type == "news":
                city = rec.get("city", "Unknown")
                text = rec.get("text", "")
                AddNews(city, text, self.output_file).write_news()

            elif feed_type == "ad":
                exp_date = rec.get("exp_date", "")
                text = rec.get("text", "")
                AddAd(exp_date, text, self.output_file).write_ads()

            elif feed_type == "horoscope":
                sign = rec.get("zodiac_sign", "")
                text = rec.get("text", "")
                AddHoroscope(sign, text, self.output_file).write_horoscope()

            else:
                print(f"⚠️ Unknown feed type in JSON record: {feed_type}")

class XmlRecords:
    def __init__(self, file_record_name='input.xml',
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

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML format in {self.file_record_name}: {e}")

        records = []

        for record in root.findall("record"):
            feed_type = record.attrib.get("type", "").lower()
            data = {child.tag: child.text for child in record}
            data["type"] = feed_type
            records.append(data)

        os.remove(file_path)
        return records

    def process_file_records(self, file_path=None):
        records = self.read_records_from_file(file_path)

        for rec in records:
            feed_type = rec.get("type", "")

            if feed_type == "news":
                city = rec.get("city", "Unknown")
                text = rec.get("text", "")
                AddNews(city, text, self.output_file).write_news()

            elif feed_type == "ad":
                exp_date = rec.get("exp_date", "")
                text = rec.get("text", "")
                AddAd(exp_date, text, self.output_file).write_ads()

            elif feed_type == "horoscope":
                sign = rec.get("zodiac_sign", "")
                text = rec.get("text", "")
                AddHoroscope(sign, text, self.output_file).write_horoscope()

            else:
                print(f"⚠️ Unknown feed type in XML record: {feed_type}")


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

class SelectInputMode(SelectType,FileRecords,JsonRecords):
    def __init__(self):
        input_mode = ''
        while input_mode not in ['manual', 'txt', 'json', 'xml']:
            input_mode = input(f"Please select how you'd like to enter the data manual, txt, json or xml: ")

            if input_mode == 'manual':
                processor = SelectType()
                processor.select_feed_type()
            elif input_mode == 'txt':
                folder_path = input(f'Please provide the path to the folder with the file (or press Enter to use default): ')

                file_name_input = input(f"Please provide the file name (or press Enter to use default 'input.txt'): ")
                if not folder_path:
                    folder_path = '/Users/Olga_Romanenko/Desktop/python/epam_training/python_training'

                if not file_name_input:
                    file_name_input = 'input.txt'

                processor = FileRecords(file_record_name=file_name_input, default_file_path=folder_path, output_file=file_name)
                processor.process_file_records()
            elif input_mode == 'json':
                folder_path = input(f'Please provide the path to the folder with the file (or press Enter to use default): ')

                file_name_input = input(f"Please provide the file name (or press Enter to use default 'input.json'): ")
                if not folder_path:
                    folder_path = '/Users/Olga_Romanenko/Desktop/python/epam_training/python_training'

                if not file_name_input:
                    file_name_input = 'input.json'

                processor = JsonRecords(file_record_name=file_name_input, default_file_path=folder_path,
                                        output_file=file_name)
                processor.process_file_records()

            elif input_mode == 'xml':
                folder_path = input(f'Please provide the path to the folder with the file (or press Enter to use default): ')
                file_name_input = input(f"Please provide the file name (or press Enter to use default 'input.xml'): ")

                if not folder_path:
                    folder_path = '/Users/Olga_Romanenko/Desktop/python/epam_training/python_training'

                if not file_name_input:
                    file_name_input = 'input.xml'

                processor = XmlRecords(file_record_name=file_name_input, default_file_path=folder_path,
                                        output_file=file_name)
                processor.process_file_records()


SelectInputMode()


# counting words
def count_words(file_to_open):
    counter = Counter()
    chars_included = r'[a-zA-Z]+'
    with open(file_to_open, 'r') as initial_file:
        for line in initial_file:
            line = line.lower()
            words = re.findall(chars_included, line)
            counter.update(words)
    return counter

word_counts = count_words(file_name)

# writing the words down into csv
def word_count_csv(word_counts, filename="word_count.csv"):
    with open(filename, 'w',  newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter = '-')
        for word, count in word_counts.most_common():
            writer.writerow([word, count])

word_count_csv(word_counts)

# counting letters and writing them down into csv
def count_letters(file_to_open, output_csv="letter_count.csv"):
    counter = Counter()
    counter_upper = Counter()
    with open(file_to_open, 'r') as initial_file:
        for line in initial_file:
            for chars in line:
                if chars.isalpha():
                    counter.update(chars.lower())
                    if chars.isupper():
                        counter_upper.update(chars.upper())

    total_letters = sum(counter.values())

    headers = ['letter','count_all','count_uppercase','percentage']
    with open(output_csv, 'w',  newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for letter, count_all in sorted(counter.items()):
            count_upper = counter_upper.get(letter.upper(), 0)
            percentage = round((count_all / total_letters) * 100, 2)
            writer.writerow({
                'letter': letter,
                'count_all': count_all,
                'count_uppercase': count_upper,
                'percentage': percentage
            })

count_letters(file_name)



