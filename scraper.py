from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import csv
import sys
import pickle
import random
import pyfiglet
import os
import datetime
from colorama import init, Fore, Style
from telethon.tl.types import UserStatusRecently
from telethon.tl.types import UserStatusRecently, ChannelParticipantsAdmins, UserStatusLastMonth, UserStatusLastWeek, UserStatusOffline, UserStatusOnline
from time import sleep
from telethon.tl.functions.channels import GetFullChannelRequest
import datetime

init()

lg = Fore.LIGHTGREEN_EX
rs = Fore.RESET
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN
r = Fore.RED
g = Fore.GREEN
b = Fore.BLUE

today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)

info = lg + '(' + w + 'i' + lg + ')' + rs
error = lg + '(' + r + '!' + lg + ')' + rs
success = w + '(' + lg + '+' + w + ')' + rs
INPUT = lg + '(' + cy + '~' + lg + ')' + rs
colors = [lg, w, r, cy]
def banner():
    f = pyfiglet.Figlet(font='slant')
    logo = f.renderText('REIS')
    print(random.choice(colors) + logo + rs)

def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

clr()
banner()
print(f'  {r}Reis Üye Çekme Yazılımı\n')
f = open('vars.txt', 'rb')
accs = []
while True:
    try:
        accs.append(pickle.load(f))
    except EOFError:
        f.close()
        break
print(f'{INPUT}{cy} Kullanıcı Scrape Etmek İçin Hesap Seçin\n')
i = 0
for acc in accs:
    print(f'{lg}({w}{i}{lg}) {acc[2]}')
    i += 1
ind = int(input(f'{INPUT}{cy} Seçiminizi Girin: '))
api_id = accs[ind][0]
api_hash = accs[ind][1]
phone = accs[ind][2]
group_name = input(f"Başında @ Olmadan Grubun Adını Girin: {r}")
c = TelegramClient(f'sessions\\{phone}', api_id, api_hash)
c.connect()
if not c.is_user_authorized():
    try:
        c.send_code_request(phone)
        code = input(f'{INPUT}{lg} Giriş Kodunu Giriniz {w}{phone}{r}: ')
        c.sign_in(phone, code)
    except PhoneNumberBannedError:
        print(f'{error}{w}{phone}{r} Banlı!{rs}')
        print(f'{error}{lg} Bunu elemek için manage.py çalıştır{rs}')
        sys.exit()
group = c.get_entity(group_name)
target_grp = "t.me/" + group_name

choice = int(input(f"\n{lg}Nasıl Bir Scrape İşlemi Planlıyorsun ? \n\n{r}[{cy}0{r}]{lg} Tüm Kullanıcılar\n{r}[{cy}1{r}]{lg} Sadece Aktif Kullanıcılar ( Dün ve Bugün )\n{r}[{cy}2{r}]{lg} Bu hafta aktif kullanıcılar\n{r}[{cy}3{r}]{lg} Bu ay aktif kullanıcılar\n{r}[{cy}4{r}]{lg} Aktif Olmayan Kullanıcılar \n\nYour choice: "))
members = []
members = c.iter_participants(group, aggressive=True)

channel_full_info = c(GetFullChannelRequest(group))
cont = channel_full_info.full_chat.participants_count

def write(group,member):
    if member.username:
        username = member.username
    else:
        username = ''
    if isinstance(member.status,UserStatusOffline):
        writer.writerow([username, member.id, member.access_hash, group.title, group.id,member.status.was_online])
    else:
        writer.writerow([username, member.id, member.access_hash, group.title, group.id,type(member.status).__name__])

admin_choice = input(f"{lg}Adminleri ayrı bir csv dosyasına ayırmak istiyor musun ?  {rs}[y/n] {lg}")
if admin_choice == "y" or admin_choice == "Y":
    with open("members\\admins.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash', 'group', 'group id','status'])
        for member in c.iter_participants(group, filter=ChannelParticipantsAdmins):    
            if not member.bot:
                write(group,member)
f.close()
print(f"{lg}")
with open("members\\members.csv", "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash', 'group', 'group id','status'])
    if choice == 0:
        try:
            for index,member in enumerate(members):
                print(f"{index+1}/{cont}", end="\r")
                if index%100 == 0:
                    sleep(3)
                if not member.bot:
                    write(group,member)                   
        except:
            print("\n Kullanıcıların 95%%  Fazlası Eklendi ")
    elif choice == 1:
        try:
            for index,member in enumerate(members):
                print(f"{index+1}/{cont}", end="\r")
                if index%100 == 0:
                    sleep(3)
                if not member.bot:
                    if isinstance(member.status, (UserStatusRecently,UserStatusOnline)):
                        write(group,member)
                    elif isinstance(member.status,UserStatusOffline):
                        d = member.status.was_online                    
                        today_user = d.day == today.day and d.month == today.month and d.year == today.year
                        yesterday_user = d.day == yesterday.day and d.month == yesterday.month and d.year == yesterday.year
                        if today_user or yesterday_user:
                            write(group,member)
        except:
            print("\nKullanıcıların 95%%  Fazlası Eklendi")
    elif choice == 2:
        try:
            for index,member in enumerate(members):
                print(f"{index+1}/{cont}", end="\r")
                if index%100 == 0:
                    sleep(3)
                if not member.bot:
                    if isinstance(member.status, (UserStatusRecently,UserStatusOnline,UserStatusLastWeek)):
                        write(group,member)
                    elif isinstance(member.status,UserStatusOffline):
                        d = member.status.was_online
                        for i in range(0,7):
                            current_day = today - datetime.timedelta(days=i)
                            correct_user = d.day == current_day.day and d.month == current_day.month and d.year == current_day.year
                            if correct_user:
                                write(group,member)
        except:
            print("\nKullanıcıların 95%%  Fazlası Eklendi")
    elif choice == 3:
        try:
            for index,member in enumerate(members):
                print(f"{index+1}/{cont}", end="\r")
                if index%100 == 0:
                    sleep(3)
                if not member.bot:
                    if isinstance(member.status, (UserStatusRecently,UserStatusOnline,UserStatusLastWeek,UserStatusLastMonth)):
                        write(group,member)
                    elif isinstance(member.status,UserStatusOffline):
                        d = member.status.was_online
                        for i in range(0,30):
                            current_day = today - datetime.timedelta(days=i)
                            correct_user = d.day == current_day.day and d.month == current_day.month and d.year == current_day.year
                            if correct_user:
                                write(group,member)
        except:
            print("\nKullanıcıların 95%%  Fazlası Eklendi")
    elif choice == 4:
        try:
            all_users = []
            active_users = []
            for index,member in enumerate(members):
                print(f"{index+1}/{cont}", end="\r")
                all_users.append(member)
                if index%100 == 0:
                    sleep(3)
                if not member.bot:
                    if isinstance(member.status, (UserStatusRecently,UserStatusOnline,UserStatusLastWeek,UserStatusLastMonth)):
                        active_users.append(member)
                    elif isinstance(member.status,UserStatusOffline):
                        d = member.status.was_online
                        for i in range(0,30):
                            current_day = today - datetime.timedelta(days=i)
                            correct_user = d.day == current_day.day and d.month == current_day.month and d.year == current_day.year
                            if correct_user:                            
                                active_users.append(member)
            for member in all_users:
                if member not in active_users:
                    write(group,member)
        except:
            print(f"\n{r}Kullanıcıların 95%%  Fazlası Eklendi")
                
f.close()

print(f"\n{lg}Kullancılar CSV dosyasına kaydedildi.{rs}\n")
clr()
banner()
with open('target_grp.txt', 'w') as f:
    f.write(target_grp)
f.close()
sys.exit()

