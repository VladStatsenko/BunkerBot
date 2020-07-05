import logging
import random
import telebot
from telebot import types
import func

bot = telebot.TeleBot('1350177076:AAERlL8gsYLBi_Cz0t0N64BARQpXZ0fbybo')
telebot.logger.setLevel(logging.DEBUG)

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
    'start': 'Get used to the bot',
    'help': 'Gives you information about the available commands',

}

imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
imageSelect.add('Сгенерировать персонажа', 'Сгенерировать катаклизм', 'Сгенерировать убежище', 'Здоровье', 'Фобия',
                'Профессия', 'Характер', 'Правила игры', 'Помочь боту')

hideBoard = types.ReplyKeyboardRemove()  # if sent as reply_markup, will hide the keyboard


# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot('1350177076:AAERlL8gsYLBi_Cz0t0N64BARQpXZ0fbybo')
bot.set_update_listener(listener)  # register listener


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


def test_send_message_with_markdown(m):
    bot = telebot.TeleBot("1350177076:AAERlL8gsYLBi_Cz0t0N64BARQpXZ0fbybo")

    markdown = """
    *bold text*
    _italic text_
    [text](URL)
    """
    ret_msg = bot.send_message(m.chat.id, markdown, parse_mode="Markdown")
    assert ret_msg.message_id


# user can chose (multi-stage command example)
@bot.message_handler(commands=['start'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "Please choose your action now", reply_markup=imageSelect)  # show the keyboard
    userStep[cid] = 1


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_image_select(m):
    cid = m.chat.id
    text = m.text

    bot.send_chat_action(cid, 'typing')

    if text == 'Сгенерировать катаклизм':
        cid = m.chat.id
        bot.send_message(cid, random.choice(func.cataklism))
        userStep[cid] = 1
    elif text == 'Сгенерировать персонажа':
        cid = m.chat.id
        bot.send_message(cid, "*Общая информация:* " + "*\nПол:* " + random.choice(
            func.sex) + " " + "*Возраст:* " + random.choice(func.age) + " лет"
                         + "*\nПрофессия:* " + random.choice(func.profession) + "*\nЗдоровье:* " + random.choice(
            func.life)
                         + "*\nФобия:* " + random.choice(func.phobie) + "*\nХобби:* " + random.choice(func.hobbie)
                         + "*\nХарактер:* " + random.choice(func.character) + "*\nДоп.Информация:* " + random.choice(
            func.info)
                         + "*\nИнвентарь:* " + random.choice(func.inv) + "*\nСпец.Карточка 1:* " + random.choice(
            func.action)
                         + "*\nСпец.Карточка 2:* " + random.choice(func.action), parse_mode="Markdown")
        userStep[cid] = 1
    elif text == 'Сгенерировать убежище':
        cid = m.chat.id
        bot.send_message(cid, "*Площадь убежища:* " + str(
            random.randrange(50, 200, 10)) + " кв.м " + "*Время нахождения в бункере:* " +
                         str(random.randrange(1, 10,
                                              1)) + " месяцев" + "Убежище находится в прекрасном состоянии, надежно "
                                                                 "спрятано и хорошо защищено внутри от "
                                                                 "недоброжелателей защитно-герметическими дверями. "
                                                                 "Все системы жизнеобеспечения в норме и работают в "
                                                                 "автономном режиме. В таком убежище можно жить и не "
                                                                 "бояться за себя. "
                         + "В убежище оборудовано: столовая , средства оказания первой помощи, кулинарные книги, "
                           "настольная игра Монополия",
                         parse_mode="Markdown")
        userStep[cid] = 1
    elif text == 'Здоровье':
        cid = m.chat.id
        bot.send_message(cid, "*Новое здоровье:* " + random.choice(func.life), parse_mode="Markdown")
        userStep[cid] = 1
    elif text == 'Фобия':
        cid = m.chat.id
        bot.send_message(cid, "*Новая фобия:* " + random.choice(func.phobie), parse_mode="Markdown")
        userStep[cid] = 1
    elif text == 'Правила игры':
        cid = m.chat.id
        bot.send_message(cid, "Минимальное количество игроков для более-менее полноценной игры: 8-12 человек."
                              "В начале игры ведущий генерирует катаклизм, убежище и персонажа для каждого играющего."
                              "Катастрофу и убежище ведущий оглашает в общий чат, проговаривая информацию, "
                              "либо скидывая текстом. "
                              "Роли ведущий скидывает в личные сообщения каждого игрока.Перед началом игры "
                              "обговаривается приблизительное количество кругов, "
                              " обычно это половина от общего числа играющих и количество характеристик,"
                              "которые будут вскрываться в каждом ходу(Желательно вскрывать по 2 характеристики за "
                              "ход, если количество игроков от 6 до 10, если игроков больше, то по 1 характеристике). "
                              "Ведущий случайным образом выбирает, в какой последовательности игроки будут оглашать "
                              "свои характеристики. "
                              "Как только игра началась, каждый игрок должен вскрыть обязательно свою профессию и "
                              "одну или две характеристики, в зависимости от того, как игроки решили до этого("
                              "Обговаривается заранее). "
                              "После каждого круга начинается голосование, в ходе которого игроки имеют время "
                              "высказаться и выбрать, кто по их мнению не заслуживает места в убежище. "
                              "Кто набирает большее количество голосов – оправдывается и пытается переубедить других "
                              "игроков в своей важности. "
                              "Если он это делает успешно - игроки могут перенести свой голос на другого игрока, "
                              "если у него не получается переубедить игроков за столом – он вылетает из игры. "
                              "Выбивший игрок может остаться в чате игры, но должен замутиться, чтобы не мешать "
                              "другим здраво закончить игру. "
                              "В конце игры происходит итоговая дискуссия, где обговариваются выданные персонажи со "
                              "всеми известными характеристиками у игроков.Карты действий можно использовать в любой "
                              "момент.")
        userStep[cid] = 1
    elif text == 'Профессия':
        cid = m.chat.id
        bot.send_message(cid, "*Новая профессия:* " + random.choice(func.profession), parse_mode="Markdown")
        userStep[cid] = 1
    elif text == 'Помочь боту':
        cid = m.chat.id
        bot.send_message(cid,
                         "Привет. Если тебе нравится бот и ты хочешь поддержать разработчиков, то вот реквизиты: "
                         "\nhttps://money.yandex.ru/to/410015758594868 ",
                         parse_mode="Markdown")
        userStep[cid] = 1
    elif text == 'Характер':
        cid = m.chat.id
        bot.send_message(cid, "*Новая черта характера:* " + random.choice(func.character), parse_mode="Markdown")
        userStep[cid] = 1
    else:
        bot.send_message(cid, "Please, use the predefined keyboard!")
        bot.send_message(cid, "Please try again")


bot.polling()
