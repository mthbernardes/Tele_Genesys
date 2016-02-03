import time, subprocess, telepot, sys
from daemon import Daemon

admins = ['mthbernardes']

class daemon_server(Daemon):
    def run(self):
        main()

def get_api():
    api_keys = {}
    api = open('api_key.txt','r')
    for i in api:
        i = i.strip()
        if not i.startswith('#'):
            k,v = i.split(':',1)
            api_keys[k] = v
    return api_keys

def handle_message(msg):
    user_id = msg['from']['id']
    nome = msg['from']['first_name']
    sobrenome = msg['from']['last_name']
    username = msg['from']['username']
    hostname = subprocess.check_output(['hostname']).lower()
    content_type, chat_type, chat_id = telepot.glance2(msg)
    if username in admins:
        if content_type is 'document':
            bot.downloadFile(msg['document']['file_id'], msg['document']['file_name'])

        elif content_type is 'text':
            command = msg['text'].lower()
            actions(user_id,command,hostname)
    else:
        bot.sendMessage(user_id, 'Desculpe '+nome+' '+sobrenome+' nao tenho permissao para falar com voce!')

def actions(user_id,command,hostname):
    if '/hostnames' in command:
        bot.sendMessage(user_id, hostname)

    elif len(command.split(' ',2)) >= 3:
        command = command.split(' ',2)
        if command[0] == '/shell' and command[1] in hostname or command[1] in 'all':
            execute = command[2].split()
            system = subprocess.check_output(execute)
            bot.sendMessage(user_id, hostname+'\n'+system)

def main():
    bot.notifyOnMessage(handle_message)
    while 1:
        time.sleep(10)

daemon_service = daemon_server('/var/run/TeleGenesys.pid')
if len(sys.argv) >= 2:
    if sys.argv[1] == 'start':
        api_key = get_api()
        api = api_key['telegram_api']
        bot = telepot.Bot(api)
        daemon_service.start()

    elif sys.argv[1] == 'stop':
        daemon_service.stop()

    elif sys.argv[1] == 'restart':
        daemon_service.restart()

    elif sys.argv[1] == 'status':
        daemon_service.is_running()
else:
    print 'Usage:',sys.argv[0],'star | stop | restart | status'
