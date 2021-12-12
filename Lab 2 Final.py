import csv
import requests
from bs4 import BeautifulSoup


def sort_num_val(obj, min_val):
    if obj == 'Unknown':
        obj = 0
    if float(obj) >= min_val:
        return True
    else:
        return False


def sort_list(obj, list_user):
    if list_user == '':
        return True
    for j in list_user:
        if j in obj:
            return True
        else:
            return False


def sort_(param, conditional, comp, obj):
    if conditional(obj[param], comp):
        return True
    else:
        return False


e = 'Если это для вас не важно нажмите Enter.'
survey = [
    'Какие жанры вас интересуют?',
    'Какие предупреждения вас интересуют?',
    'Какие типы вас интерсует?',
    'Какие годы начала съёмки аниме вас интересует?',
    'Какие годы окончания съёмки аниме вас интерсует?',
    'Какие сезоны съёмки вас интересует?',
    'Какая студия вас интересует?',
    'Какой минимальный рейтинг вас интересует? '
    'Введите число, если оно не целое то используйте точку для '
    'разделения '
    'целой и десятичной части.',
    'Какое минимальное количество голосов вас интересует?',
    'Какое минимальное количество эпизодов вас интересует?',
    'Важно для вас чтобы аниме ещё продолжало выпускатьcя или '
    'уже закончило? '
    'Введите "True" или "False".'
]

answer = {
    'tags_user': None,
    'con_war': None,
    'type_user': None,
    'start_year': None,
    'end_year': None,
    'season_user': None,
    'studios_user': None,
    'min_rating': None,
    'min_number_votes': None,
    'min_episodes': None,
    'finish_user': None
}

check = 0
for i in answer:
    print(survey[check] + e)
    check += 1
    if check <= 7:
        answer[i] = input().split(", ")
    if check > 7:
        answer[i] = input()
    if 7 < check < 11:
        try:
            answer[i] = float(answer[i])
        except ValueError:
            answer[i] = 0

list_sort = [
    ['Tags', sort_list, answer['tags_user']],
    ['Content Warning', sort_list, answer['con_war']],
    ['Type', sort_list, answer['type_user']],
    ['StartYear', sort_list, answer['start_year']],
    ['EndYear', sort_list, answer['end_year']],
    ['Season', sort_list, answer['season_user']],
    ['Studios', sort_list, answer['studios_user']],
    ['Rating Score', sort_num_val, answer['min_rating']],
    ['Number Votes', sort_num_val, answer['min_number_votes']],
    ['Episodes', sort_num_val, answer['min_episodes']],
    ['Finished', sort_list, answer['finish_user']]
]

with open('anime.csv', 'r', encoding='utf-8') as file:
    c = csv.DictReader(file, delimiter=',', quotechar='\"')
    arr = []
    for row in c:
        result = 0
        for i in range(len(list_sort)):
            if sort_(list_sort[i][0], list_sort[i][1], list_sort[i][2],
                     row):
                result += 1
            if result == 11:
                if row['Rating Score'] == 'Unknown':
                    arr.append([float(0), row['Name'], row['Url']])
                else:
                    arr.append([float(row['Rating Score']), row['Name'],
                                row['Url']])
arr.sort()
arr.reverse()

pics = 0
for i in range(0, len(arr)):
    response = requests.get(arr[i][2])
    soup = BeautifulSoup(response.text, 'html.parser')
    img = requests.get("https://www.anime-planet.com/"
                       + soup.find('img', class_='screenshots')['src'])
    img_file = open(str(i + 1) + '.jpg', 'wb')
    img_file.write(img.content)
    img_file.close()
    pics += 1
    if pics == 5:
        break

with open('Top.txt', 'w', encoding='utf-8') as file:
    for i in range(len(arr)):
        file.write(str(i + 1) + ' ' + arr[i][1] + arr[i][2] + '\n')

print(
    'Результат вашего поиска лежит в папке Top.txt, и отсортированно '
    'по рейтингу. Плакаты к первым пяти аниме названы в порядке '
    'убывания. Приятного просмотра)')
