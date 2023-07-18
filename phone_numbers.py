import telebot
from telebot import types

import pycountry
import phonenumbers
from phonenumbers import carrier
from faker import Faker
from babel import Locale

import datetime

with open('keys.txt', 'r') as f:
    key=f.readline()
bot = telebot.TeleBot(key)

checking=False
generating=False
ID=1

bot_info="GENERATE AND VALIDATE PHONE NUMBERS"

start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
check_button = types.KeyboardButton("🔎 CHECK VALIDATION")
generate_button = types.KeyboardButton("💡 GENERATE NEW NUMBER")
start_markup.add(check_button, generate_button)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    with open('file.txt', 'a') as f:
        mynow=datetime.datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S')
        f.write(message.from_user.first_name+'---'+message.from_user.username+'\nNow-'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n'+mynow+'\n\n')
    global ID
    ID=1
    bot.send_message(message.chat.id, bot_info)
    bot.send_message(message.chat.id, "🚩NEW SESSION🚩")
    bot.send_message(message.chat.id, "CHOOSE YOUR OPTION✔️", reply_markup=start_markup)

@bot.message_handler(commands=['stop'], func=lambda message: checking or generating)
def exit_checking(message):
    global checking, generating
    generating=False
    checking=False
    bot.send_message(message.chat.id, 'Stopped.', reply_markup=start_markup)

@bot.message_handler(func=lambda message: checking)
def check_validation(message):
    number=message.text
    msg='⛔️Invalid number'
    global ID
    try:
        num_obj = phonenumbers.parse(number)
    except:
        ID+=1
        pass
    else:
        ID+=1
        if phonenumbers.is_valid_number(num_obj):
            msg='✅️Valid number'
    bot.reply_to(message, '#'+str(ID)+'\n'+msg+'\n\nSend new number or use /stop command to finish validation check')

@bot.message_handler(func=lambda message:message.text==check_button.text)
def check_(message):
    global checking
    checking = True
    check_markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, 'Send phone number to check it', reply_markup=check_markup)
    
@bot.message_handler(func=lambda message: generating)
def generate_numbers(message):
    msg=message.text.split()
    try:
        reg=msg[1].upper()
        count=int(msg[0])
        lcl=str(Locale.parse('und_'+reg))
    except:
        bot.reply_to(message, 'Invalid input. Try again')
    else:
        fake = Faker(locale=lcl)
        country=pycountry.countries.get(alpha_2=reg)
        global generating
        for _ in range(count):
            c=0
            while True:
                if not generating: break
                number = fake.phone_number()
                try:
                    num_obj = phonenumbers.parse(number, reg)
                except:
                    print(number, reg)
                else:
                    carrier_=carrier.name_for_number(num_obj, "en")
                    if phonenumbers.is_valid_number(num_obj):
                        if carrier_:
                            break
                        else:
                            if c>=100:
                                carrier_="___"
                                break
                            c+=1

            if not generating: break
            global ID  
            international_number = phonenumbers.format_number(num_obj, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            n=international_number.replace('-', ' ').split()
            generated_num=f"🌐Area code: {n[0][1:] if len(n)<=3 else n[1]}\n📱Number: {international_number}\n▶️Carrier: {carrier_}"
            bot.send_message(message.chat.id, '#'+str(ID)+'\n'+generated_num)
            ID+=1
        try:
            bot.send_message(message.chat.id, f'Country: {country.flag}\nNumeric-3 code: {country.numeric}\nPhone code: {num_obj.country_code}\nName: {country.name}', reply_markup=start_markup)
        except:
            bot.send_message(message.chat.id, "Country error", reply_markup=start_markup)

        generating=False


@bot.message_handler(func=lambda message:message.text==generate_button.text)
def generate_number(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, 'Input country and count with space(EX: 12 RU)', reply_markup=markup)
    global generating
    generating=True

bot.infinity_polling()


