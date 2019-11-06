import random
import vk_api
import bs4
import requests
import datetime
import json
import bible

print("bot activated")

from vk_api.longpoll import VkLongPoll, VkEventType
#кнопки
def button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }

#главное меню
keyboard_main = {
    "one_time": False,
    "buttons": [
    [
    button(label="дата",color = "positive"),
    button(label="ссылки",color = "primary")
    ],
    [
    button(label="расписание на сегодня",color = "positive"),
    button(label="расписание на завтра",color = "positive")
    ],
    [
    button(label="расписание на эту неделю",color = "positive")
    ],
    [
    button(label="расписание на следующую неделю",color = "positive")
    ],
    [
    button(label="обновить клавиатуру",color = "secondary")
    ]
    ]
}

keyboard_main = json.dumps(keyboard_main, ensure_ascii=False).encode('utf-8')
keyboard_main = str(keyboard_main.decode('utf-8'))

#меню ссылок
keyboard_s = {
    "one_time": False,
    "buttons": [
    [
    button(label="диск",color = "positive")
    ],
    [
    button(label="вернуться назад",color = "primary")
    ]
    ]
}

keyboard_s = json.dumps(keyboard_s, ensure_ascii=False).encode('utf-8')
keyboard_s = str(keyboard_s.decode('utf-8'))

#функция откправки сообщений
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

    
vk = vk_api.VkApi(token='6029a9bfd073b90a86569e12dc44cb0c4b8802110787038805463904e0ab1da4b7b0bb987212dcad0cc63')

longpoll = VkLongPoll(vk)

slov1 = {"33583588" : False}
slov2 = {"33583588" : False}

write_msg("33583588", "bot activated")
#главный цикл
for event in longpoll.listen():
    
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            print("id = ", event.user_id, "\nname: ", clean(_get_name(event.user_id)), "\nmessage: ", event.text, "\n\n")#информация для Одмена

            #главное меню:
            if event.text.lower() == "дата":
                nl = '\n'
                write_msg(event.user_id, f"{clean(_get_time())} {nl} {clean(_get_ned())} ")

            elif event.text.lower() == "нет ты" or event.text.lower() == "ты пидор":
                write_msg(event.user_id, "нет ты")
                
            elif event.text.lower() == "дат":
                 write_msg(event.user_id, f"{clean(_get_name(event.user_id))}, вы долбоеб? Вы ошиблись даже здесь!!!")

            elif event.text.lower() == "расписание на завтра":
                d = datetime.date.today() + datetime.timedelta(days=1)
                wd = d.weekday()
                if chzn() == 1 and wd != 0:
                    write_msg(event.user_id, open('data/znamweek.txt', 'r', encoding='utf-8').read().split('#\n')[wd])
                elif chzn() == 0 and wd != 0:
                    write_msg(event.user_id, open('data/chislweek.txt', 'r', encoding='utf-8').read().split('#\n')[wd])
                elif chzn() == 1 and wd == 0:
                    write_msg(event.user_id, open('data/chislweek.txt', 'r', encoding='utf-8').read().split('#\n')[wd])
                elif chzn() == 0 and wd == 0:
                    write_msg(event.user_id, open('data/znamweek.txt', 'r', encoding='utf-8').read().split('#\n')[wd])
                    
            elif event.text.lower() == "расписание на сегодня":
                d = datetime.date.today()
                wd = d.weekday()
                if chzn() == 1:
                    write_msg(event.user_id, open('data/znamweek.txt', 'r', encoding='utf-8').read().split('#\n')[wd])
                else:
                    write_msg(event.user_id, open('data/chislweek.txt', 'r', encoding='utf-8').read().split('#\n')[wd])

            elif event.text.lower() == "расписание на эту неделю":
                if chzn() == 1:
                    write_msg(event.user_id, open('data/znamweek.txt', 'r', encoding='utf-8').read())
                else:
                    write_msg(event.user_id, open('data/chislweek.txt', 'r', encoding='utf-8').read())
                    
            elif event.text.lower() == "расписание на следующую неделю":
                if chzn() == 1:
                    write_msg(event.user_id, open('data/chislweek.txt', 'r', encoding='utf-8').read())
                else:
                    write_msg(event.user_id, open('data/chislweek.txtznamweek.txt', 'r', encoding='utf-8').read())

            #меню ссылок
            elif event.text.lower() == "диск":
                write_msg(event.user_id, "https://drive.google.com/drive/folders/101EW_MCEvfXDnCvD6tILdkNoaW9lGWEh")
            
            #действия с клавиатурой
            elif event.text.lower() == "обновить клавиатуру" or event.text.lower() == "начать":
                vk.method("messages.send", {"peer_id": event.user_id, 'random_id': random.randint(0, 2048),"message": "Клавиатура обновлена", "keyboard": keyboard_main})

            elif event.text.lower() == "ссылки":
                vk.method("messages.send", {"peer_id": event.user_id, 'random_id': random.randint(0, 2048),"message": "Меню ссылок", "keyboard": keyboard_s})

            elif event.text.lower() == "вернуться назад":
                vk.method("messages.send", {"peer_id": event.user_id, 'random_id': random.randint(0, 2048),"message": "Главное меню", "keyboard": keyboard_main})

            #работа с напоминаниями
            elif event.text.lower() == "напоминания":
                write_msg(event.user_id,bible.reading())

            elif event.text.lower() == "добавить напоминание":
                slov1 = {event.user_id : True}
                print(slov1, "\n" , slov2)
                write_msg(event.user_id,"Введите дату(Пример:2019-10-23). Следующим сообщением введите само напоминание.")
                
            elif slov1[event.user_id]:
                print(slov1, "\n" , slov2)
                a = vk.method("messages.getHistory", {'user_id' : event.user_id, 'offset' : 0, 'count' : 1, 'peer_id': event.user_id })
                print(bible.filter_msg(str(a)))
                file = open("data/nap.txt",'a')
                file.write("\n" + bible.filter_msg(str(a)))
                slov1 = {event.user_id : False}
                slov2 = {event.user_id : True}
                file.close()
                
                
            elif slov2[event.user_id]:
                print(slov1, "\n" , slov2)
                a = vk.method("messages.getHistory", {'user_id' : event.user_id, 'offset' : 0, 'count' : 1, 'peer_id': event.user_id })
                print(bible.filter_msg(str(a)))
                file = open("data/nap.txt",'a')
                file.write("\n" + bible.filter_msg(str(a)))
                file.write("\n#")
                file.close()
                

            #если пользователь что-то ввел не так:                        
            else:
                write_msg(event.user_id, "Попробуй что-нибудь другое. Если залагала клавиатура, напиши \"начать\"")
                
