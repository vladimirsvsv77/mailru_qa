import os
import re
import requests
import argparse
import time
from pymongo import MongoClient


parser = argparse.ArgumentParser(description='start_parsing.py')
parser.add_argument('-number')
parser.add_argument('-start')
parser.add_argument('-end')
opt = parser.parse_args()
number = opt.number
start = opt.start
end = opt.end


def write_file(filename, text):
    f = open(os.getcwd() + '/' + filename, 'a')
    f.write(text + '\n')
    f.close()


client = MongoClient('localhost', 27017)
db = client.mairudata
questions = db.mairudata


def start_parsing(count_start, count_end):
    count_attempt = 0

    while True:
        try:
            while count_start > count_end:
                url = 'https://otvet.mail.ru/api/v2/question'
                data = {
                    'qid': str(count_start)
                }
                req = requests.post(url, data=data)

                try:
                    if req.json()['status'] == '200':
                        if req.json()['bestanswer'] != '0':
                            question =  req.json()['qtext']
                            question = re.sub('<[^<]+?>', '', question.replace('\n', ' ').replace('\r', ' '))
                            answ = req.json()['best']['atext']
                            answ = re.sub('<[^<]+?>', '', answ.replace('\n', ' ').replace('\r', ' '))
                            if question != '' and answ != '' and answ is not None and question is not None:
                                qa = {
                                    "qid": str(count_start),
                                    "question": question,
                                    "answer": answ
                                }
                                questions.insert_one(qa)

                except Exception as e:
                    write_file('errors.txt', str(number) + ' - ' + str(e))
                    write_file('errors.txt', str(number) + ' - ' + req.text)
                    write_file('errors.txt', str(number) + ' - ' + '____________________________________')

                if count_start % 1000 == 0:
                    write_file('count_start.txt', str(number) + ' - ' + str(count_start))

                count_start -= 1
        except Exception as e:
            write_file('errors.txt', str(number) + ' - ' + str(e))
            write_file('errors.txt', str(number) + ' - ' + '____________________________________')
            if count_attempt > 2:
                time.sleep(180)
                count_start -= 1
                count_attempt = 0
            else:
                time.sleep(60)
                count_attempt += 1




start_parsing(int(start), int(end))
