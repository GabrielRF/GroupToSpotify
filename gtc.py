from bs4 import BeautifulSoup
import configparser
import re
import requests
import spotipy
import spotipy.util as util
import sys
import telebot

config = configparser.ConfigParser()
config.sections()
config.read('/usr/local/bin/GroupToChannel/bot.conf')

arg1 = sys.argv[1]

token = config[arg1]['TOKEN']
crawl = config[arg1]['CRAWL']
write = config[arg1]['WRITE']
history = config[arg1]['SIZE']
user_id = config[arg1]['USER_ID']
playlist_id = config[arg1]['PLAYLIST_ID']

list_file = '/usr/local/bin/GroupToChannel/lists/' + arg1 + '_whitelist.txt'
last_updates = '/usr/local/bin/GroupToChannel/logs/' + arg1 + '_log.txt'

bot = telebot.TeleBot(token)

def create_file(file):
    open(file, 'w', encoding='utf-8')

def get_html(url):
    response = requests.get(url)
    html = BeautifulSoup(response.content, 'html.parser')
    return html

def get_urls(text):
    urls = re.findall(r'(https?://\S+)', text)
    return urls

def get_title(html):
    try:
        title = html.find('meta', {'property': 'og:title'})
        title = title['content']
    except:
        title = html.title.text.strip()
    return title

def get_domain(url):
    domain = url.split('://')[1].split('/')[0].replace('www.','')
    return domain

def get_img(html):
    img = html.find('img', {'class', 'cover'}).get('src')
    if not img:
        img = html.find('meta', {'name': 'og:image'})
    try:
        preview = False
        if 'http:' not in img and 'https:' not in img:
            img = 'http:' + img
    except TypeError:
        img = ''
        preview = True
    return preview, img

def check_spotify_song(url):
    if 'open.spotify.com/track/' in url:
        return True
    else:
        return False

def check_whitelist(text):
    try:
        listwords = open(list_file, 'r', encoding="utf-8")
    except FileNotFoundError:
        create_file(list_file)
        listwords = open(list_file, 'r', encoding="utf-8")
    for word in listwords.readlines():
        if word.title().replace('\n','') in text.title():
            return True
    return False

def add_recent_updates(link):
    try:
        with open(last_updates, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        create_file(last_updates)
        with open(last_updates, 'r') as file:
            lines = file.readlines()
    if lines.__len__() >= int(history):
        lines.pop(0)
    lines.append(''.join(link) + '\n')
    with open(last_updates, 'w') as file:
        for l in lines:
            file.write(l)

def check_recent_updates(param,new):
    try:
        updates = open(last_updates,'r')
    except FileNotFoundError:
        create_file(last_updates)
        updates = open(last_updates,'r')
    for upd in updates:
        if param in upd.split('\n'):
            new = False
            return new
    if new:
        add_recent_updates(param)
        return new

def send_message(url):
    html = get_html(url)
    try:
        title = get_title(html)
        preview, img = get_img(html)
    except:
        return 0
    domain = get_domain(url)
    message = ('<b>' + title + '</b>' 
        '<a href="' + img + '">.</a>\n'
        '<a href="' + url + '">' + domain + '</a>')
    if len(write) > 5:
        bot.send_message(write, message, parse_mode='HTML',
            disable_web_page_preview=preview)

def add_to_playlist(url):
    track_id = url.split('/track/')[1]
    track_id = 'spotify:track:' + track_id
    print(track_id)
    scope = 'playlist-modify-private'
    sp_token = util.prompt_for_user_token(user_id, scope,
        client_id = config[arg1]['CLIENT_ID'],
        client_secret = config[arg1]['CLIENT_SECRET'],
        redirect_uri = 'http://gabrf.com'
    )
    if sp_token:
        sp = spotipy.Spotify(auth=sp_token)
        sp.trace = False
        results = sp.user_playlist_add_tracks(user_id, playlist_id, [track_id])
        print(results)
    else:
        print("Can't get token for", user_id)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if str(message.chat.id) == str(crawl):
        urls = get_urls(message.text)
        for url in urls:
            if check_whitelist(url):
                if(check_recent_updates(url, True)):
                    send_message(url)
                    if check_spotify_song(url):
                        try:
                        # if True:
                            add_to_playlist(url)
                            bot.reply_to(message, 'Música adicionada!')
                        except:
                            bot.reply_to(message, 'Ops! Ocorreu algum erro.')
                else:
                    bot.reply_to(message, 'Repetido')
                    print('repetido')
            else:
                print('not ok')
    else:
        print('Ignorado')

bot.polling()

