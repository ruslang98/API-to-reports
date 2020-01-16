import os
import re
import json
import requests

from datetime import datetime

now = datetime.strftime(datetime.now(), '%Y.%m.%d %H:%M')

try:
    todos_url = 'https://jsonplaceholder.typicode.com/todos'
    todos_response = requests.get(todos_url)
    todos = json.loads(todos_response.text)

    users_url = 'https://jsonplaceholder.typicode.com/users'
    user_response = requests.get(users_url)
    users = json.loads(user_response.text)

    for i in range(len(todos)):
        if todos[i]['title'] == '':
            todos.pop(i)

except requests.exceptions.RequestException as e:
    print('Response is: {content}'.format(content=e.response.content))


# Find path to script and check presence folder
def change_dir():
    current_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_path)
    if not os.path.exists('tasks'):
        os.mkdir('tasks')
    os.chdir('tasks')


def create_file(username, name, email, company, user_id):
    with open(f'{username}.txt', 'w') as opened_file:
        opened_file.write(f'{name} <{email}> {now}')
        opened_file.write(f'\n{company}')
        opened_file.write('\n')
        for todo in todos:
            if todo['userId'] == user_id and todo['completed']:
                if len(todo['title']) > 50:
                    opened_file.write('\n' + todo['title'][:50] + '...')
                else:
                    opened_file.write('\n' + todo['title'])
        opened_file.write('\n')
        for todo in todos:
            if todo['userId'] == user_id and not todo['completed']:
                if len(todo['title']) > 50:
                    opened_file.write('\n' + todo['title'][:50] + '...')
                else:
                    opened_file.write('\n' + todo['title'])


# Add time of creation to existing files
def rename_file(username):
    with open(username + '.txt') as opened_file:
        text = opened_file.read()
    time = re.search(r'[0-9]{4}\.(0[1-9]|1[012])\.(0[1-9]|1[0-9]|2[0-9]|3[01]) '
                     r'(([0,1][0-9])|(2[0-3])):[0-5][0-9]', text)
    report_time = time.group(0).replace('.', '-').replace(' ', 'T')
    return os.rename(f'{username}.txt', f'{username}_{report_time}.txt')


def check_file(username):
    return True if os.path.exists(f'{username}.txt') else False


def main():
    try:
        change_dir()
        for user in users:
            if check_file(user['username']):
                rename_file(user['username'])
                create_file(user['username'], user['name'], user['email'], user['company']['name'], user['id'])
            else:
                create_file(user['username'], user['name'], user['email'], user['company']['name'], user['id'])
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
