import random
import vk_api
import bs4
import requests
import datetime
import json

from vk_api.longpoll import VkLongPoll, VkEventType

#чтение всего файла
def reading():
    s = ''
    file = open("data/nap.txt", 'r')
    for i in range(25):
        s = s + file.readline()
    return s

#выделение нужного фрагмента напоминания
def file_msg(string,chislo):
    s = ''
    text = ''
    skip = True
    for word in string:
        s = s + word
        #print(s[-10:])
        if s[-10:] == chislo:
            skip = False
        elif skip == False and word == "#":
            break
        elif skip == False:
            text = text + word
    return text

def filter_msg(string):
    s = ''
    text = ''
    skip = True
    for word in string:
        s = s + word
        #print(s[-10:])
        if s[-9:] == "\'text\': \'":
            skip = False
        elif skip == False and word == "'":
            break
        elif skip == False:
            text = text + word
    return text
#функция откправки сообщений
def write_msg(user_id, message):
    vk.method('messages.send',{'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})

#выделение из строки id пользователей   
def clean(string):
    result = ''
    skip = True
    for i in list(string):
        if i == '[':
            skip = False
        elif i == ']':
            skip = True
            break
        elif skip == False and i != ' ':
            result = result + i
    return result

def write_msg(user_id, message):
    vk.method('messages.send',{'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})
    
#дата
def _get_time():
    request = requests.get("https://my-calend.ru/date-and-time-today")
    b = bs4.BeautifulSoup(request.text, "html.parser")
    return b.select(".page")[0].findAll("h2")[0]

#дата
def _get_ned():
    request = requests.get("https://students.bmstu.ru/schedule/d2e70d3c-4aee-11e9-a55b-005056960017")
    b = bs4.BeautifulSoup(request.text, "html.parser")
    return b.select(".page-header")[0].findAll("i")[0]

#полуение имени по id
def _get_name(user_id):
    request = requests.get("https://vk.com/id"+str(user_id))
    b = bs4.BeautifulSoup(request.text, "html.parser")
    return b.findAll("h2")[0]

#числитель\знаменатель
def chzn():
    w = datetime.date.today().isocalendar()[1]
    return w%2

#очищение вывода от лишнего
def clean(string_line):

        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """
        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True

        return result

