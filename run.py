# -*- coding: utf-8 -*-
# This example show how to use inline keyboards and process button presses
import json
from time import sleep
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
import threading



#https://api.telegram.org/bot588938933:AAFetPuKIs2D2ngbOElevpt5ojec-6Y2qrM/getUpdates
TELEGRAM_TOKEN = '680565733:AAGV-qO0t66_LJ9bYTx_lBFcaEcLwdV_qL8'
group_id=[-1001115498598,-1001159230627]
in_group=None
tmp_msg=''
user_info = {}
tmp_num=0
bot = telebot.TeleBot(TELEGRAM_TOKEN)

line_1='Join our Telegram group'
line_2='Follow us on Twitter'
line_3='Retweet one tweet'
line_4='Follow and like us on Facebook'
line_5='Create an account on GJ.COM'


class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None


def process_name_step(message):
    try:
        global tmp_chat_id
        tmp_chat_id = message.chat.id
        user_info['id'] = tmp_chat_id
        info=bot.get_chat(message.chat.id)
        tmp_name = info.first_name+info.last_name
        user_info['name']=tmp_name
        str1="""\
Please provide the e-mail address you used to register on our website
Note: By entering your e-mail address you accept that we will send you further updates about the GJ Airdrops and our exchange.
"""
        msg = bot.reply_to(message, str1)
        bot.register_next_step_handler(msg, process_email_step)
    except Exception as e:
        bot.reply_to(message, 'bot is busy')

def process_email_step(message):
    try:
        # chat_id = message.chat.id
        tmp_email = message.text
        user_info['email'] = tmp_email
        str1 = """\
Thank you. Please now provide me a link to your Facebook profile. For example https://www.facebook.com/yourtradingcommunity
"""
        msg = bot.reply_to(message, str1)
        bot.register_next_step_handler(msg, process_facebook_step)
    except Exception as e:
        bot.reply_to(message, 'bot is busy')

def process_facebook_step(message):
    try:
        # chat_id = message.chat.id
        tmp_facebook = message.text
        user_info['facebook'] = tmp_facebook
        str1 = """\
Thanks again, please now provide me your Twitter ID. For Example @GJ_Exchange
"""
        msg = bot.reply_to(message, str1)
        bot.register_next_step_handler(msg, process_twiter_step)
    except Exception as e:
        bot.reply_to(message, 'bot is busy')

def process_twiter_step(message):
    try:
        # chat_id = message.chat.id
        tmp_twiter = message.text
        user_info['twiter'] = tmp_twiter

        with open("./user_info.txt", encoding="utf-8", mode="a") as data:
            data.write('\n' + str(user_info['id'])+'#####'+user_info['name']+'#####'+user_info['email']+'#####'+user_info['facebook']+'#####'+user_info['twiter'])

        str1="""
Congratulations！You will receive 50 GT tokens. You can visit GJ.COM website, and check the "Activity" page, where the section showing “GT reward earned” will be updated within 3 week days after the end of promotion to include your reward.
All GT rewards received by the user during the promotion will be issued within 15 working days after GT has officially launched.

Your referral link: https://t.me/GJHelperBot
You can share your referral link to your friends:)
"""
        msg = bot.reply_to(message, str1)

        try:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('/info')
            msg = bot.reply_to(message, 'Click on the button to view our official website and community link', reply_markup=markup)
            bot.register_next_step_handler(msg, process_links_step)
        except Exception as e:
            bot.reply_to(message, 'bot is busy')

    except Exception as e:
        bot.reply_to(message, 'bot is busy')


def process_links_step(message):
    try:

        choose_links = message.text
        if choose_links == '/info':
            str1 = """
Official site:
https://www.gj.com

Telegram(Chinese):
 https://t.me/GJCOMEX

Telegram(English):
 https://t.me/yourtradingcommunity

Twitter:
https://twitter.com/GJ_Exchange

LinkedIn:
 https://www.linkedin.com/company/gj-exchange/

Medium:
 https://medium.com/@GJ.COM

Facebook:
 https://www.facebook.com/yourtradingcommunity
"""
            bot.send_message(message.chat.id, str1)
            # file1 = open('./web.html', 'rb')
            # bot.send_document(message.chat.id, file1)

    except Exception as e:
        bot.reply_to(message, 'bot is busy')


def process_language_step(message):
    try:

        language = message.text
        if language == 'English' or language == 'ok':
            global str_a
            str_a = 'en'

        else:
            str_a = 'ch'

#########################################################  main
        tmp_uid = message.chat.id
        global in_group
        global tmp_msg
        tmp_msg = message
        in_group = 'no'
        if tmp_uid in group_id:
            in_group = 'yes'

        # else:
        #     try:
        #         if (bot.get_chat_member(group_id[0], tmp_uid).status) in ['creator','member','administrator']:
        #             in_group = 'yes'
        #         if (bot.get_chat_member(group_id[1], tmp_uid).status) in ['creator','member','administrator']:
        #             in_group = 'yes'
        #     except:
        #         in_group = 'no'

        elif tmp_uid not in group_id:
            try:
                if (bot.get_chat_member(group_id[0], tmp_uid).status) in ['creator','member','administrator']:
                    in_group = 'yes'
            except:
                    in_group = 'no'

            try:
                if (bot.get_chat_member(group_id[1], tmp_uid).status) in ['creator','member','administrator']:
                    in_group = 'yes'
            except:
                in_group = 'no'


        if message.text == 'hi':
            bot.reply_to(message, 'hello! who are you?')
        elif 'fuck' in message.text or 'Fuck' in message.text:
            bot.reply_to(message, "I know you are scolding me, please use civilized language.")
        else:
            str1="""\
In order to be eligible for the draw, you will need to complete the following:
1. Join our Telegram group  (REQUIRED)
2. Follow us on Twitter  (REQUIRED)
3. Retweet one tweet  (REQUIRED)
4. Follow and like us on Facebook   (REQUIRED)
5. Create an account on GJ.COM (REQUIRED)
"""

            str2="""\
Have you completed all the steps above?          
"""
            if in_group == 'yes':
                bot.send_message(message.chat.id, str1, reply_markup=gen_markup())
                bot.send_message(message.chat.id, str2, reply_markup=gen_markup_new())
            elif in_group == 'no':
                bot.send_message(message.chat.id, str1, reply_markup=gen_markup())
                bot.send_message(message.chat.id, str2, reply_markup=gen_markup_new())
            else:
                bot.send_message(message.chat.id, str1, reply_markup=gen_markup())
                bot.send_message(message.chat.id, str2, reply_markup=gen_markup_new())

    except Exception as e:
        bot.reply_to(message, 'bot is busy')



def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton(line_1, url="https://t.me/yourtradingcommunity"),
               InlineKeyboardButton(line_2, url="https://twitter.com/GJ_Exchange"),
               InlineKeyboardButton(line_3, url="https://twitter.com/GJ_Exchange/status/1046327155108470785"),
               InlineKeyboardButton(line_4, url="https://www.facebook.com/yourtradingcommunity"),
               InlineKeyboardButton(line_5, url="https://www.gj.com/#/signup/new"),)
    return markup

def gen_markup_new():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add( InlineKeyboardButton('yes', callback_data="a"),InlineKeyboardButton('no', callback_data="b"),)
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "a":
        if in_group =='no':
            bot.answer_callback_query(call.id, "please perform  all the required tasks first")
        elif in_group =='yes':
            # bot.answer_callback_query(call.id, "please submit your data")
            process_name_step(message=tmp_msg)
    elif call.data == "b":
        bot.answer_callback_query(call.id, "Before you submit your data, please perform the required task first.")

@bot.message_handler(commands=['help', 'start','info'])
def message_handler(message):
     print(message.chat.type)
    # man_num=bot.get_chat_members_count(group_id[0])
    # global tmp_num
    # if  man_num > tmp_num:
    #     bot.send_message(message.chat.id, "welcome new members, enter /start to call bot",)
    # tmp_num=man_num

     if message.chat.type == "private":

         try:
            # markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            # markup.add('English', '中文 （未完成）')
            # msg = bot.reply_to(message, 'Please choose language', reply_markup=markup)
            # bot.register_next_step_handler(msg, process_language_step)

            tmp_uid = message.chat.id
            global in_group
            global tmp_msg
            tmp_msg = message
            in_group = 'no'
            if tmp_uid in group_id:
                in_group = 'yes'
            elif tmp_uid not in group_id:
                try:
                    if (bot.get_chat_member(group_id[0], tmp_uid).status) in ['creator', 'member', 'administrator']:
                        in_group = 'yes'
                except:
                    in_group = 'no'

                try:
                    if (bot.get_chat_member(group_id[1], tmp_uid).status) in ['creator', 'member', 'administrator']:
                        in_group = 'yes'
                except:
                    in_group = 'no'
            if message.text == 'hi':
                bot.reply_to(message, 'hello! who are you?')
            elif 'fuck' in message.text or 'Fuck' in message.text:
                bot.reply_to(message, "I know you are scolding me, please use civilized language.")
            # elif message.text == 'start':

            str1 = """\
    In order to be eligible for the draw, you will need to complete the following:
    1. Join our Telegram group  (REQUIRED)
    2. Follow us on Twitter  (REQUIRED)
    3. Retweet one tweet  (REQUIRED)
    4. Follow and like us on Facebook   (REQUIRED)
    5. Create an account on GJ.COM (REQUIRED)
    """

            str2 = """\
    Have you completed all the steps above?          
    """
            if in_group == 'yes':
                bot.send_message(message.chat.id, str1, reply_markup=gen_markup())
                bot.send_message(message.chat.id, str2, reply_markup=gen_markup_new())
            elif in_group == 'no':
                bot.send_message(message.chat.id, str1, reply_markup=gen_markup())
                bot.send_message(message.chat.id, str2, reply_markup=gen_markup_new())
            else:
                bot.send_message(message.chat.id, str1, reply_markup=gen_markup())
                bot.send_message(message.chat.id, str2, reply_markup=gen_markup_new())


         except Exception as e:
            bot.reply_to(message, 'bot is busy')


     if message.chat.type == "group" or  message.chat.type == "supergroup":

        try:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('/info')
            msg = bot.reply_to(message, "you can click '/info' to get more message,and chatting with robots privately to know more.", reply_markup=markup)
        except Exception as e:
            bot.reply_to(message, 'bot is busy')

        if message.text=='/info':
            str1 = """
GJ.COM Community Channels:

Official Site:
https://www.gj.com

Help Center：
https://support.gj.com/hc/en-us

Telegram(Official Announcement):
https://t.me/GJCOMFANS

Telegram(Chinese):
 https://t.me/GJCOMEX

Telegram(English):
 https://t.me/yourtradingcommunity

Twitter:
https://twitter.com/GJ_Exchange

LinkedIn:
 https://www.linkedin.com/company/gj-exchange/

Medium:
 https://medium.com/@GJ.COM

Facebook:
 https://www.facebook.com/yourtradingcommunity
"""
            bot.reply_to(message,str1)


while True:

    try:

        bot.polling(none_stop=True)

    except Exception as e:
        sleep(15)