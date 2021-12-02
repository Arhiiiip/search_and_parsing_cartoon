import csv, time, requests
from bs4 import BeautifulSoup
#Функция для фильтрации параметров имеющих числовое значение:
def num_val(obj, min_val):
    if obj == 'Unknown':
        obj = 0
    if float(obj) >= min_val:
        return True
    else:
        return False
#Функция для фильтрации параметров, которые не обязательно должны встрчаться все разом:
def lists(obj, spiski):
    for i in spiski:
        if i in obj:
            return True
        else:
            return False
#Отдельная функция для фильтрации по жанру, так как для поиска можно использовать несколько жанров и они все должны учитываться:
def genre(obj, tags_user):
    for i in tags_user:
        if i not in obj:
            return False
        else:
            return True
#Функция, для проверки на соответсвие с запросом:
def filter_(param, condF, comp, obj):
    if condF(obj[param], comp):
        return True
    else:
        return False

print('Какой минимальный рейтинг вас интересует? Введите число, если оно не целое то используйте точку для разделения целой и десятичной части. Если это для вас не важно нажмите Enter.')
min_rating = input()
try:
    min_rating = float(min_rating)
except:
    if min_rating == '':
        print('')
    else:
        print('К сожелению вы ввели не число или вообще ничего не ввели, значит это не будет учтено(')
        time.sleep(0.5)
    min_rating = 0
print('Какое минимальное количество голосов вас интересует? Если это для вас не важно нажмите Enter.')
min_number_votes = input()
try:
    min_number_votes = float(min_number_votes)
except:
    if min_number_votes == '':
        print('')
    else:
        print('К сожелению вы ввели не число или вообще ничего не ввели, значит это не будет учтено(')
        time.sleep(0.5)
    min_number_votes = 0

print('Какие жанры вас интересуют? Если это для вас не важно нажмите Enter.')
tags_user = input().split(", ")
print('Какие предупреждения вас интересуют? Если это для вас не важно нажмите Enter.')
con_war = input().split(", ")
print('Какие типы вас интерсует? Если это для вас не важно нажмите Enter.')
type_user = input().split(", ")
print('Какое минимальное количество эпизодов вас интересует? Если это для вас не важно нажмите Enter.')
min_episodes = input()
try:
    min_episodes = float(min_episodes)
except:
    if min_episodes == '':
        print('')
    else:
        print('К сожелению вы ввели не число или вообще ничего не ввели, значит это не будет учтено(')
        time.sleep(0.5)
    min_episodes = 0
print('Важно для вас чтобы аниме ещё продолжало выпускатьcя или уже закончило? Введите "True" или "False". Если это для вас не важно нажмите Enter.')
finish_user = input()
print('Какие годы начала съёмки аниме вас интересует? Если это для вас не важно нажмите Enter.')
start_year = input().split(", ")
print('Какие год окончания съёмки аниме вас интерсует? Если это для вас не важно нажмите Enter.')
end_year = input().split(", ")
print('Какие сезоны съёмки вас интересует? Если это для вас не важно нажмите Enter.')
season_user = input().split(", ")
print('Какая студия вас интересует? Если это для вас не важно нажмите Enter.')
studios_user = input().split(", ")

with open('anime.csv', 'r', encoding='utf-8') as file:
    c = csv.DictReader(file, delimiter=',', quotechar='\"')
    arr = []
    for row in c:
        if filter_('Rating Score', num_val, min_rating, row) and filter_('Number Votes', num_val, min_number_votes, row):
            if filter_('Tags', genre, tags_user, row) and filter_('Content Warning', lists, con_war, row) and filter_('Type', lists, type_user, row):
                if filter_('Episodes', num_val, min_episodes, row) and filter_('StartYear', lists, start_year, row) and filter_('EndYear', lists, end_year, row):
                    if filter_('Season', lists, season_user, row) and filter_('Studios', lists, studios_user, row):
                        if row['Rating Score'] == 'Unknown':
                            arr.append([float(0), row['Name'], row['Url']])
                        else:
                            arr.append([float(row['Rating Score']), row['Name'], row['Url']])
arr.sort()
arr.reverse()

pics = 0
for i in range(0, len(arr)):
    response = requests.get(arr[i][2])
    soup = BeautifulSoup(response.text, 'html.parser')
    img = requests.get("https://www.anime-planet.com/" + soup.find('img', class_ = 'screenshots')['src'])
    img_file = open(str(i+1) + '.jpg', 'wb')
    img_file.write(img.content)
    img_file.close()
    pics += 1
    if pics == 5:
        break

with open('top.txt', 'w', encoding='utf-8') as file:
    for i in range(len(arr)):
        file.write(str(i+1)+ ' ' + arr[i][1] + arr[i][2] + '\n')
