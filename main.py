import telebot

#@TestfulOfSteel_bot 
TOKEN = "7062605820:AAH5MHvfue7vypO65-G95kuOJB_aS0Tr-Ks"

def message(text, var) :
    return ('message', text, var)

def cond(cases) :
    return ('cond', cases)

def condEquals(var, val, results) :
    return ( lambda data : data[var] == val, results )
def condElse(results) :
    return ( lambda data : True, results )

dialogue = [
    message('Что?', 'a'),
    message('А поподробнее?', 'b'),
    message('Точно?', 'c'),

    cond([

        condEquals('a', 'Ничего', [
            message('Че крутой такой?', 'd'),
            message('Ну ты и чел?', 'e')
        ]),
        condElse([
            message('Ну не лол так не лол', 'd'),
            message('Просто кек', 'e')
        ])

    ])
]

save = {}


def processDialogue(id : int, data : dict, var : str) :
    stack : list = [] #pos, arr

    curArr : list = dialogue
    curPos = 1 #Сдвиг для пропуска первого сообщения

    variable = dialogue[0][2]

    while True : 
        print("Current pos:", curPos)

        if curPos == len(curArr) :

            if len(stack) > 0 :
                prev = stack.pop()

                curPos = prev[0]
                curArr = prev[1]

                continue;
            else :
                return None

        # Проверка условий
        type = curArr[curPos][0]

        if type == 'message' :
            text = curArr[curPos][1]

            if variable in data :
                variable = curArr[curPos][2]
                curPos += 1
                continue

            data[variable] = var
            variable = curArr[curPos][2]

            return text
        elif type == 'cond' :
            for cond in curArr[curPos][1] : # [ {check, arr} ]
                if not cond[0](data) : continue

                print("stack add", cond[1])

                stack.append( (curPos+1, curArr) ) #После pop перейти дальше

                curPos = 0;
                curArr = cond[1]

                break;
        elif type == 'end' :
            return None;


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message) :
    id = message.chat.id

    if id in save :
        del save[id]

    keyboard = telebot.types.InlineKeyboardMarkup();

    keyboard.add( telebot.types.InlineKeyboardButton("Лол", callback_data='foo') )
    keyboard.add( telebot.types.InlineKeyboardButton("Не лол", callback_data='start') )

    bot.send_message(id, dialogue[0][1], reply_markup=keyboard )
    save[id] = {}

    bot.set_chat_menu_button()

@bot.message_handler(chat_types=['private'])
def simple_message(message : telebot.types.Message) :
    id = message.chat.id
    data = save[id]

    msg = processDialogue(id, data, message.text)

    if msg == None : 
        bot.send_message(message.chat.id, "Сообщения закончились")
    else :
        bot.send_message(message.chat.id, msg)




bot.polling()

#bot.polling(none_stop=True)