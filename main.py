import os
import telebot
from telebot import *
from datetime import date
import gspread
import logging
from config import *
from flask import Flask, request

bot = telebot.Telebot(BOT_TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)
googlesheet_id = 'https://docs.google.com/spreadsheets/d/1E-F6Nfm2iLEaVTN-4eh2b2uYfE10eZ_9sNDrUZsZpzY/edit#gid=0'
gc = gspread.service_account(filename='my-project-19798-python-bot-53bb87dd46fb.json')

###знакомимся
@bot.message_handler(commands=['start'])
def start(message):
    if message.text =='Отмена':
        # нужна ли помощь еще?
        markup = types.InlineKeyboardMarkup(row_width=1)
        help_please = types.InlineKeyboardButton('Да', callback_data='help_please')
        no_help = types.InlineKeyboardButton('Нет', callback_data='no_help')
        markup.add(help_please, no_help)

        bot.send_message(message.chat.id,
                         'Могу помочь чем-то ещё?',
                         reply_markup=markup,
                         parse_mode='html')
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        yes = types.InlineKeyboardButton('Да', callback_data='answer_yes')
        no = types.InlineKeyboardButton('Нет', callback_data='answer_no')
        markup.add(yes, no)
        global user_name;
        user_name = f"{message.from_user.last_name} {message.from_user.first_name}"
        menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        cancel = types.KeyboardButton("Отмена")
        menu.add(cancel)
        bot.send_message(message.chat.id,
                     f'Добрый день, в меню ты можешь отменять действия',
                     reply_markup=menu,
                     parse_mode='html')

        bot.send_message(message.chat.id,
                     f'<b>{user_name}</b>,я верно к тебе обращаюсь?',
                     reply_markup=markup,
                     parse_mode='html')

@bot.callback_query_handler(func = lambda call:True)
def callback(call):
    if call.message:
        if call.data == "answer_yes":
            global check_name;
            check_name = 0
            bot.send_message(call.message.chat.id,
                             "Рад с тобой познакомиться! Давай расскажу, что я умею",
                             parse_mode='html')
            markup_choice = types.InlineKeyboardMarkup(row_width=1)
            friend = types.InlineKeyboardButton('Поблагодарить друга', callback_data='thanks')
            money = types.InlineKeyboardButton('Проверить баланс', callback_data='check_money')
            idea = types.InlineKeyboardButton('Предложить идею подарка', callback_data='get_idea')
            finish = types.InlineKeyboardButton('Завершить сеанс', callback_data='no_help')
            markup_choice.add(friend, money, idea, finish)
            bot.send_message(call.message.chat.id, "В меню ты можешь выбрать, чем я могу тебе помочь!",
                             reply_markup=markup_choice)
        elif call.data == "answer_no":
            bot.send_message(call.message.chat.id, f"Давай исправим это) Назови свою Фамилию Имя (Именно в этом порядке), а Имя напиши полностью. Например, <b>Иванов Иван</b>", parse_mode='html')
            bot.register_next_step_handler(call.message, get_full_name)
        elif call.data == "thanks":
            bot.send_message(call.message.chat.id,
                            "Напиши, кого ты хочешь поблагодарить в формате 'Фамилия Имя - причина'",
                            parse_mode='html')
            bot.register_next_step_handler(call.message, get_thank)

        elif call.data == "check_money":
            bot.send_message(call.message.chat.id,
                             "Проверяю твой банковский счет",
                             parse_mode='html')

            today = date.today().strftime("%d.%m.%Y")
            if check_name == 0:
                sh = gc.open_by_url(googlesheet_id)
                sheet = sh.worksheet("Банк")
                cell = sheet.find(user_name)
                money = sheet.cell(cell.row, cell.col + 1).value
                bot.send_message(call.message.chat.id,
                                 f'На твой балансе сейчас {money} Ibrahim',
                                 parse_mode='html')
                markup = types.InlineKeyboardMarkup(row_width=1)
                help_please = types.InlineKeyboardButton('Да', callback_data='help_please')
                no_help = types.InlineKeyboardButton('Нет', callback_data='no_help')
                markup.add(help_please, no_help)

                ### помочь чем-то еще
                bot.send_message(call.message.chat.id,
                                 'Могу помочь чем-то ещё?',
                                 reply_markup=markup,
                                 parse_mode='html')
            elif check_name == 1:
                sh = gc.open_by_url(googlesheet_id)
                sheet = sh.worksheet("Банк")
                cell = sheet.find(user_name)
                money = sheet.cell(cell.row, (cell.col + 1)).value
                bot.send_message(call.message.chat.id,
                                 f'На твоем балансе сейчас {money} Ibrahim',
                                 parse_mode='html')
                markup = types.InlineKeyboardMarkup(row_width=1)
                help_please = types.InlineKeyboardButton('Да', callback_data='help_please')
                no_help = types.InlineKeyboardButton('Нет', callback_data='no_help')
                markup.add(help_please, no_help)

                ### помочь чем-то еще
                bot.send_message(call.message.chat.id,
                                 'Могу помочь чем-то ещё?',
                                 reply_markup=markup,
                                 parse_mode='html')
            else:
                bot.send_message(call.message.chat.id,
                                 f'Кажется, случилась ошибка, не могу тебя найти. Попробуй нажать "/start" и снова представиться',
                                 parse_mode='html')


        elif call.data == "get_idea":
            bot.send_message(call.message.chat.id,
                             "Какой подарок ты бы хотел получить за участие в жизни компании?")
            bot.register_next_step_handler(call.message, get_idea)

        elif call.data == "help_please":
            markup_choice = types.InlineKeyboardMarkup(row_width=1)
            friend = types.InlineKeyboardButton('Поблагодарить друга', callback_data='thanks')
            money = types.InlineKeyboardButton('Проверить баланс', callback_data='check_money')
            idea = types.InlineKeyboardButton('Предложить идею подарка', callback_data='get_idea')
            finish = types.InlineKeyboardButton('Завершить сеанс', callback_data='no_help')
            markup_choice.add(friend, money, idea, finish)
            bot.send_message(call.message.chat.id, "В меню ты можешь выбрать, чем я могу тебе помочь!",
                             reply_markup=markup_choice)
        elif call.data == "no_help":
            bot.send_message(call.message.chat.id,
                             "Хорошего дня! Если я понадоблюсь просто пиши'/help'")
            bot.register_next_step_handler(call.message, help)
        else:
            bot.register_next_step_handler(call.message, help)



def get_full_name(message):
    if message.text == 'Отмена':
        # нужна ли помощь еще?
        markup = types.InlineKeyboardMarkup(row_width=1)
        help_please = types.InlineKeyboardButton('Да', callback_data='help_please')
        no_help = types.InlineKeyboardButton('Нет', callback_data='no_help')
        markup.add(help_please, no_help)

        bot.send_message(message.chat.id,
                         'Могу помочь чем-то ещё?',
                         reply_markup=markup,
                         parse_mode='html')
    else: # получаем имя
        global user_name;
        user_name = message.text
        global check_name;
        check_name = 1
        bot.send_message(message.from_user.id,
                    f"Приятно познакомиться, <b>{user_name}</b>!",
                    parse_mode='html')
        markup_choice = types.InlineKeyboardMarkup(row_width=1)
        friend = types.InlineKeyboardButton('Поблагодарить друга', callback_data='thanks')
        money = types.InlineKeyboardButton('Проверить баланс', callback_data='check_money')
        idea = types.InlineKeyboardButton('Предложить идею подарка', callback_data='get_idea')
        finish = types.InlineKeyboardButton('Завершить сеанс', callback_data='no_help')
        markup_choice.add(friend, money, idea, finish)
        bot.send_message(message.chat.id, "В меню ты можешь выбрать, чем я могу тебе помочь!", reply_markup=markup_choice)


###выбираем что будем делать
@bot.message_handler(commands=['help'])
def help(message):
    markup_choice = types.InlineKeyboardMarkup(row_width=1)
    friend = types.InlineKeyboardButton('Поблагодарить друга', callback_data='thanks')
    money = types.InlineKeyboardButton('Проверить баланс', callback_data='check_money')
    idea = types. InlineKeyboardButton('Предложить идею подарка', callback_data='get_idea')
    finish = types.InlineKeyboardButton('Завершить сеанс', callback_data='no_help')
    markup_choice.add(friend, money, idea, finish)
    bot.send_message(message.chat.id, "В меню ты можешь увидеть, чем я могу тебе помочь!", reply_markup=markup_choice)


def get_thank(message):
    today = date.today().strftime("%d.%m.%Y")
    global sep;
    sep = "-"
    #  разделяем сообщение на 2 части, Фамилия и Имя
    if sep in message.text:
        name, reason = message.text.split("-", 1)
        text_message = f'{today} {name} получил(а) в благодарность 2 Ibrahims'
        bot.send_message(message.chat.id, text_message)

        # открываем Google таблицу и добавляем запись
        sh = gc.open_by_url(googlesheet_id)
        sheet = sh.worksheet("Благодарность")
        sheet.append_row([today, user_name, name, reason])

        markup = types.InlineKeyboardMarkup(row_width=1)
        help_please = types.InlineKeyboardButton('Да', callback_data='help_please')
        no_help = types.InlineKeyboardButton('Нет', callback_data='no_help')
        markup.add(help_please, no_help)

        ### помочь чем-то еще
        bot.send_message(message.chat.id,
                    'Могу помочь чем-то ещё?',
                    reply_markup=markup,
                    parse_mode='html')
    elif message.text =='Отмена':
        # нужна ли помощь еще?
        markup = types.InlineKeyboardMarkup(row_width=1)
        help_please = types.InlineKeyboardButton('Да', callback_data='help_please')
        no_help = types.InlineKeyboardButton('Нет', callback_data='no_help')
        markup.add(help_please, no_help)

        bot.send_message(message.chat.id,
                         'Могу помочь чем-то ещё?',
                         reply_markup=markup,
                         parse_mode='html')

    else:
        bot.send_message(message.chat.id,
                         "Кажется произошла ошибка, давай попробуем еще раз. "
                         "Напиши, кого ты хочешь поблагодарить в формате 'Фамилия Имя - причина'."
                         "И не забудь добавить <b> тире </b>",
                         parse_mode='html')
        bot.register_next_step_handler(message, get_thank)


def get_idea(message):
        today = date.today().strftime("%d.%m.%Y")
        #  разделяем сообщение на 2 части, Фамилия и Имя
        idea = message.text
        text_message = f'Твоя идея просто невероятная! Обязательно поделюсь с HR)'
        bot.send_message(message.chat.id, text_message)

        # открываем Google таблицу и добавляем запись
        sh = gc.open_by_url(googlesheet_id)
        sheet = sh.worksheet("Бизнес идея")
        sheet.append_row([today, user_name, idea])

        #нужна ли помощь еще?
        markup = types.InlineKeyboardMarkup(row_width=1)
        help_please = types.InlineKeyboardButton('Да', callback_data='help_please')
        no_help = types.InlineKeyboardButton('Нет', callback_data='no_help')
        markup.add(help_please, no_help)

        bot.send_message(message.chat.id,
                        'Могу помочь чем-то ещё?',
                        reply_markup=markup,
                        parse_mode='html')


def check_money(message):
    if message.text =='Отмена':
        # нужна ли помощь еще?
        markup = types.InlineKeyboardMarkup(row_width=1)
        help_please = types.InlineKeyboardButton('Да', callback_data='help_please')
        no_help = types.InlineKeyboardButton('Нет', callback_data='no_help')
        markup.add(help_please, no_help)

        bot.send_message(message.chat.id,
                         'Могу помочь чем-то ещё?',
                         reply_markup=markup,
                         parse_mode='html')

    elif check_name == 0:
        today = date.today().strftime("%d.%m.%Y")
        sh = gc.open_by_url(googlesheet_id)
        sheet = sh.worksheet("Банк")
        cell = sheet.find(f"{message.from_user.last_name} {message.from_user.first_name}")
        money = sheet.cell(cell.row, cell.col+1).value
        bot.send_message(message.chat.id,
                    f'На твоем балансе сейчас {money} Ibrahim',
                    parse_mode='html')
    elif check_name == 1:
        today = date.today().strftime("%d.%m.%Y")
        sh = gc.open_by_url(googlesheet_id)
        sheet = sh.worksheet("Банк")
        cell = sheet.find(user_name)
        money = sheet.cell(cell.row, (cell.col + 1)).value
        bot.send_message(message.chat.id,
                    f'На твоем балансе сейчас {money} Ibrahim',
                    parse_mode='html')
    else:
        bot.send_message(message.chat.id,
                    f'Кажется, случилась ошибка, не могу тебя найти. Попробуй нажать "/start" и снова представиться',
                    parse_mode='html')


    #нужна ли помощь еще?
    markup = types.InlineKeyboardMarkup(row_width=1)
    help_please = types.InlineKeyboardButton('Да', callback_data='help_please')
    no_help = types.InlineKeyboardButton('Нет', callback_data='no_help')
    markup.add(help_please, no_help)

    bot.send_message(message.chat.id,
                    'Могу помочь чем-то ещё?',
                    reply_markup=markup,
                    parse_mode='html')

if __name__=="__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host = "0.0.0.0", port=int(os.environ.get("PORT", 5000)))

@server.router(f"/{BOT_TOKEN}", methods = ["POST"])
def redirect_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200
