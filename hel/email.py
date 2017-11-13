def send_mail(topic, body, addresser, recievers):
    with open('send.log', 'a', encoding='utf-8') as file:
        # Text prettification
        text = 'From: ' + addresser + '\n'
        text += 'To: '
        for reciever in recievers:
            text += reciever + ' '
        text += '\n' + topic + '\n' + body + '\n'
        text += '------------------------------------\n'

        file.write(text)
