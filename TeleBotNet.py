import telepot,time,subprocess
admins = ['ADMIN_USER_HERE']
group = "GROUP_HERE"
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
            actions(command,hostname)
    else:
        bot.sendMessage(group, 'Desculpe '+nome+' '+sobrenome+' nao tenho permissao para falar com voce!')
def actions(command,hostname):
    print command
    if '/hostnames' in command:
        bot.sendMessage(group, hostname)
    elif len(command.split(' ',2)) >= 3:
        command = command.split(' ',2)
        if command[0] == '/shell' and command[1] in hostname or command[1] in 'all':
            execute = command[2].split()
            system = subprocess.check_output(execute)
            bot.sendMessage(group, hostname+'\n'+system)
api = "API_TOKEN_HERE"
bot = telepot.Bot(api)
bot.notifyOnMessage(handle_message)
while 1:
    time.sleep(10)
