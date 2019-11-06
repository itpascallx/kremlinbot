import random
import vk_api
import bs4
import requests
import datetime
import json
import bible
import time

print("napominaka activated")
from vk_api.longpoll import VkLongPoll, VkEventType

#чтение всего файла
def reading():
    s = ''
    file = open("data/nap.txt", 'r')
    d = datetime.date.today()
    for i in range(25):
        s = s + file.readline()
    return s

#глобальные переменные для file_msg
i = 0
st = ""
text = "" 
skip = True

#выделение нужного фрагмента напоминания
def file_msg(string,chislo):
    print("sysle")
    global i
    global st
    global text
    global skip
    for word in string[i:]:
        st = st + word
        i = i + 1
        if st[-10:] == chislo:
            skip = False
        elif skip == False and word == "#":
            skip = True
            file_msg(string,chislo)
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
    
vk = vk_api.VkApi(token='6029a9bfd073b90a86569e12dc44cb0c4b8802110787038805463904e0ab1da4b7b0bb987212dcad0cc63')

longpoll = VkLongPoll(vk)

s = vk.method('groups.getMembers',{'group_id' : '188277159'})


write_msg("33583588", "hello")
#print(str(s)[24:164])
#print (clean(str(s)).split(','))


users = clean(str(s)).split(',')# id всех пользователей группы
users = ["33583588"]
n1 = 0

#функция напоминания
def napomin():
    #переменные##
    global n1
    today = datetime.date.today()
    #############
    for user in users:
        try:
            write_msg(user, str(today) + ":")
            write_msg(user, file_msg(reading(),str(today)))
        except:
            print(user, " - не могу отправить сообщение")
            


#цикл напоминания
while True:
    napomin()
    time.sleep(86400)
