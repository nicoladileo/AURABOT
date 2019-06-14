import telepot
import time
import csv
import distance
import datetime

TOKEN = '838127239:AAGJ1f6vDt7XCDkdehmkX_ziy0DAZOcDaL4'
COMMANDS = ['/avellino','/benevento','/caserta','/napoli','/salerno']
DEFAULT_MESSAGE = '''Comando non riconosciuto.
Per interagire con il bot invia la tua posizione o digita uno dei seguenti comandi:
/avellino
/benevento
/caserta
/napoli
/salerno'''
capoluoghi = ['Avellino Scuola Alighieri','Benevento Campo Sportivo','Caserta CE51 Ist.Manzoni','Napoli NA09 Via Argine','Salerno Parco Mercatello']

def read_csv_centraline():
    with open('centraline.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        centraline = [row for row in csv_reader]
        return centraline

def read_centralina(name):
    today = datetime.datetime.now().strftime('%Y-%m-%d').replace('2019','2018')
    hour_temp = '%02d'
    hour = datetime.datetime.now().hour
    with open('giugno_2018.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        letture = [row for row in csv_reader if row['descrizione'] == name and row['data_ora'].split(' ')[0] == today]
        misurazioni = ''
        rilievo = ''
        for row in letture:
            if row['data_ora'].split(' ')[1].split(':')[0] == hour_temp % hour:
                rilievo = row['data_ora'].split(' ')[0].replace('2018','2019')
                misurazioni += row['inquinante'] + ': ' + row['valore'] + ' ' + row['um'] + '\n'
    return 'Ultimo rilievo: ' + rilievo + '\n' + misurazioni


def on_message_received(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    message = ''
    timestamp = datetime.datetime.fromtimestamp(msg['date'])
    print(timestamp.strftime('%d-%m-%Y %H:%M:%S') + ' Messaggio ricevuto da ' + msg['from']['first_name'] + ' ' + msg['from']['last_name'])
    if (content_type == 'text'):
        if msg['text'].lower() in COMMANDS:
            message = msg['text']
            idx = COMMANDS.index(message)
            centralina = capoluoghi[idx]
            message = 'Centralina vicina: ' + centralina + '\n'
            misurazioni = read_centralina(centralina)
            message += misurazioni
        else:
            message = DEFAULT_MESSAGE
    elif (content_type == 'location'):
        #Invio coordinate
        latitude = msg['location']['latitude']
        longitude = msg['location']['longitude']
        centraline = read_csv_centraline()
        min_distance = 10000000000
        nearest = ''
        for row in centraline:
            c_distance = distance.haversine(latitude,longitude,float(row['latitudine']),float(row['longitudine']))
            if c_distance < min_distance:
                min_distance = c_distance
                nearest = row['centrale']
        message = 'Centralina vicina: ' + nearest + '\n'
        misurazioni = read_centralina(nearest)
        message += misurazioni
    else:
        message = DEFAULT_MESSAGE
    bot.sendMessage(chat_id, message)

bot = telepot.Bot(TOKEN)
bot.message_loop(on_message_received)

print('Listening')

while 1:
    time.sleep(10)
