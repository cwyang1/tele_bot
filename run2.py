# -*- coding: utf-8 -*-
# This example show how to use inline keyboards and process button presses
import json
from time import sleep

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
import threading



#https://api.telegram.org/bot588938933:AAFetPuKIs2D2ngbOElevpt5ojec-6Y2qrM/getUpdates
TELEGRAM_TOKEN = '666802293:AAFMsP30aRF8ziWRldu6O33ssqwu0fCwDK8'
group_id=[-1001115498598,-1001159230627]
in_group=None
tmp_msg=''
user_info = {}
tmp_num=0
bot = telebot.TeleBot(TELEGRAM_TOKEN)

line_1='加入电报群'
line_2='关注Twitter'
line_3='转发Twitter帖子'
line_4='关注Facebook'
line_5='注册 GJ.COM 账号'

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
请确保您完成所有任务之后，请提供GJ.COM的注册邮箱地址，以便接收空投GT
备注：输入邮箱地址代表您默认接受我们给您发送有关GJ空投和GJ.COM交易所的更多信息：）
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
感谢，请提供您的Facebook主页的链接，比如：https://www.facebook.com/yourtradingcommunity
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
再次感谢！请提供您的Twitter ID，比如：@GJ_Exchange
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

        with open("./user_info2.txt", encoding="utf-8", mode="a") as data:
            data.write('\n' + str(user_info['id'])+'#####'+user_info['name']+'#####'+user_info['email']+'#####'+user_info['facebook']+'#####'+user_info['twiter'])

        str1="""
恭喜你！你将得到50GT的奖励，奖励将于活动结束后3个工作日内更新显示，你可到GJ.COM官网【内测活动】页面「已获得的GT奖励」处查看。活动期间用户所获得的所有GT奖励将于GT正式上线后15个工作日内发放。

你的邀请链接: https://t.me/GJHelperCNBot

分享链接邀请好友一起参与：)
"""
        msg = bot.reply_to(message, str1)

        try:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('/info')
            msg = bot.reply_to(message, '点击按钮，查看我们的官网和社区链接', reply_markup=markup)
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
官网:
https://www.gj.com

Telegram(中文):
 https://t.me/GJCOMEX

Telegram(英文):
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
请先完成以下几个小任务，即可参与空投活动：
1. 加入电报群（必做）
2. 关注Twitter（必做）
3. 转发Twitter帖子（必做）
4. 关注Facebook（必做）
5. 注册 GJ.COM 账号（必做）
"""

            str2="""\
你已经完成以上所有操作了吗？        
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
    markup.add(InlineKeyboardButton(line_1, url="https://t.me/GJCOMEX"),
               InlineKeyboardButton(line_2, url="https://twitter.com/GJ_Exchange"),
               InlineKeyboardButton(line_3, url="https://twitter.com/GJ_Exchange/status/1046327155108470785"),
               InlineKeyboardButton(line_4, url="https://www.facebook.com/yourtradingcommunity"),
               InlineKeyboardButton(line_5, url="https://www.gj.com/#/signup/new"),)
    return markup

def gen_markup_new():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add( InlineKeyboardButton('是', callback_data="a"),InlineKeyboardButton('否', callback_data="b"),)
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "a":
        if in_group =='no':
            bot.answer_callback_query(call.id, "请先完成所有“必做”任务")
        elif in_group =='yes':
            # bot.answer_callback_query(call.id, "请填写相关信息")
            process_name_step(message=tmp_msg)
    elif call.data == "b":
        bot.answer_callback_query(call.id, "请先完成所有“必做”任务，之后您就可以进入下一步骤.")

@bot.message_handler(commands=['help', 'start','info'])
def message_handler(message):

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
请先完成以下几个小任务，即可参与空投活动：
1. 加入电报群（必做）
2. 关注Twitter（必做）
3. 转发Twitter帖子（必做）
4. 关注Facebook（必做）
5. 注册 GJ.COM 账号（必做）
"""

            str2 = """\
你已经完成以上所有操作了吗？        
"""
            if in_group == '是':
                bot.send_message(message.chat.id, str1, reply_markup=gen_markup())
                bot.send_message(message.chat.id, str2, reply_markup=gen_markup_new())
            elif in_group == '否':
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
            msg = bot.reply_to(message, "你可以点击 '/info' 查看网址信息,还可以和机器人私下聊天，了解更多.", reply_markup=markup)
        except Exception as e:
            bot.reply_to(message, 'bot is busy')

        if message.text=='/info':
            str1 = """
官网:
GJ.COM 社群渠道:

官网:
https://www.gj.com

帮助中心：
https://support.gj.com/hc/en-us

电报群(官方公告):
https://t.me/GJCOMFANS

电报群(中文):
 https://t.me/GJCOMEX

电报群(英文):
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