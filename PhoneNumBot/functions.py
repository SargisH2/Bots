import phonenumbers
from phonenumbers import carrier
from faker import Faker
import pandas as pd
from datetime import datetime
import time

col = ['ID', 'Name', 'Date', 'Count', 'Last request']
# df = pd.DataFrame(columns = col)
# df.to_csv("data.csv")
df = pd.read_csv("data.csv")
IDs = list(df['ID'])
id, name = None, None
def user_info(message):
    global id, name
    id, name = message.from_user.id, message.from_user.first_name
    if id not in IDs:
        IDs.append(id)
        global df
        df = pd.concat([df, pd.DataFrame([[id, name, None, None, None]], columns=col)], axis=0).iloc[:,-5:]
        global log 
    return id, name

def is_valid(number):
    try:
        num_obj = phonenumbers.parse(number)
        return phonenumbers.is_valid_number(num_obj)
    except:
        return False

def generate(message, log):
    time0 = time.time()
    numbers = []
    try:
        count=int(message)
        if count < 1 or count > 100: return []
    except:
        return []
    fake = Faker(locale='en_US')
    for _ in range(count):
            while True:
                number = fake.phone_number()
                if 'x' not in number:
                    try:
                        num_obj = phonenumbers.parse(number, 'US')
                    except:
                        continue
                    
                    carrier_ = carrier.name_for_number(num_obj, "en")
                    if carrier_:
                        break
            numbers.append(phonenumbers.format_number(num_obj, phonenumbers.PhoneNumberFormat.INTERNATIONAL)+f", Carrier: {carrier_}")
    if log:
        global df
        df.loc[df['ID']==id, 'Date':] = [datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Count: '+str(count), "Numbers:\n"+'\n'.join(numbers)]
        df.iloc[:, -5:].to_csv("data.csv")
    return [*numbers, f"\nGenerated in {round(time.time()-time0, 2)}s"]

def history(id):
    params = [str(df.loc[df['ID']==id, i][0]).replace('nan', '') for i in col[-3:]]
    info = '\n'.join(params)
    return info