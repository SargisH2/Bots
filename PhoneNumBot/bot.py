from telebot import types, TeleBot
from functions import user_info, is_valid, generate, history

with open('keys.txt', 'r') as f:
    key = f.readline()
bot = TeleBot(key)

log=False
user_id, user_name = None, None
start_msg="Hello! Use telegram account or continue as a guest."
logged_msg = ", you can check validation of a number, or generate new!"
guest_msg = "Check valdation, generate numbers or log in with /Use command"
send_check_msg = "Send number to check it"
invalid_num_text = "⛔️Invalid number"
valid_num_text = "✅️Valid number"
generate_msg = "Input Count (Limit: 100)"
invalid_count = "⛔️Invalid Count"
not_history_text = "Nothing to show :("
waiting_text = "Wait a sec...⏳"


empty_markup = types.ForceReply(selective=False)
#
start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
guest_btn = types.KeyboardButton("/Guest")
use_btn = types.KeyboardButton("/Use my info")
start_markup.add(guest_btn, use_btn)
#
com_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
check_button = types.KeyboardButton("🔎 CHECK VALIDATION")
generate_button = types.KeyboardButton("💡 GENERATE NUMBERS")
his_btn = types.KeyboardButton("Show last request")
com_markup.add(check_button, generate_button)
#
com_markup_guest = types.ReplyKeyboardMarkup(resize_keyboard=True)
com_markup_guest.add(check_button, generate_button)
com_markup_guest.add(use_btn)

def log_guest():
    global user_id, user_name, com_markup
    com_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    com_markup.add(check_button, generate_button)
    com_markup.add(use_btn)
    user_id, user_name = None, None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    log_guest()
    bot.send_message(message.chat.id, start_msg, reply_markup=start_markup)

@bot.message_handler(commands=['Guest', 'Use'])
def st_2(message):
    msg = message.text
    if 'Use' in msg:
        global user_id, user_name, com_markup
        if not user_id:
            user_id, user_name = user_info(message)
            com_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(check_button, generate_button)
            com_markup.add(his_btn)
            bot.send_message(message.chat.id, user_name+logged_msg, reply_markup=com_markup)
        else:
            bot.send_message(message.chat.id, 'Logged in as '+user_name, reply_markup=com_markup)
    else:
        log_guest()
        bot.send_message(message.chat.id, guest_msg, reply_markup=com_markup)
        

def check_val(message):
    if is_valid(message.text):
        bot.send_message(message.chat.id, valid_num_text, reply_markup=com_markup if user_id else com_markup_guest)
    else:
        bot.send_message(message.chat.id, invalid_num_text, reply_markup=com_markup if user_id else com_markup_guest)
@bot.message_handler(func=lambda message: message.text==check_button.text)
def checking(message):
    bot.send_message(message.chat.id, send_check_msg, reply_markup=empty_markup)
    bot.register_next_step_handler(message, check_val)
################################################### check/generate
def gen_num(message):
    del_id = bot.send_message(message.chat.id, waiting_text).message_id
    numbers = generate(message.text, bool(user_id))
    bot.delete_message(message.chat.id, del_id)
    if numbers:
        msg="\n".join(numbers) + '\nCount: ' + message.text
        bot.send_message(message.chat.id, msg, reply_markup=com_markup if user_id else com_markup_guest)
    else:
        bot.send_message(message.chat.id, invalid_count, reply_markup=com_markup if user_id else com_markup_guest)
@bot.message_handler(func=lambda message: message.text == generate_button.text)
def generating(message):
    bot.send_message(message.chat.id, generate_msg, reply_markup=empty_markup)
    bot.register_next_step_handler(message, gen_num)


@bot.message_handler(func=lambda message: message.text == his_btn.text)
def find_history(message):
    msg =  history(user_id)
    if not msg.replace('\n', ''):
        msg = not_history_text
    bot.send_message(message.chat.id, msg, reply_markup=com_markup)

bot.infinity_polling()
