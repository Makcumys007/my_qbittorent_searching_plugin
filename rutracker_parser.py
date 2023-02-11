import requests
from requests_html import HTMLSession, HTML

login = 'https://rutracker.net/forum/login.php'

headers = {
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

data = {
    "redirect": "https://rutracker.net/forum/index.php",
    "login_username": "HelloWorld007",
    "login_password": "19931102",
    "cap_sid": "rjTHmDK8ibLBRVQuAVGZ",
    "cap_code_0e71bff0760616a57bb4c57753e7a2e6": "d6u",
    "login": "%C2%F5%EE%E4"
}


def use_HTMLParser(text):
    html = HTML(html=text)
    html.encoding = 'utf-8'
    return html

def get_the_list_of_search_result(text='Avatar'):
    html = use_HTMLParser(text)
    match = html.find('a')
    link_list = []

    for link in match:
        if link.attrs.get('data-topic_id'):
            link_list.append(f"https://rutracker.net/forum/{link.attrs.get(('href'))}")
    return link_list


def get_the_torrent(link_list, session):
    torrents = []

    for link in link_list:
        result = session.get(link)

        if result.status_code == 200:
            html = use_HTMLParser(result.text)
            match = html.find('title', first=True)
            title = match.text

            match = html.find('.borderless', first=True)
            info = match.text

            match = html.find('.seed', first=True)
            seed = "0"
            if match != None:
                seed = match.text


            match = html.find('.leech', first=True)
            leech = "Личи: 0"
            if match != None:
                leech = match.text

            match = html.find('.magnet-link', first=True)
            magnet = match.attrs.get('href')

            torrent = {
                'description': link,
                'title': title,
                'info': info.replace('\xa0', '|'),
                'seed': seed.replace('\xa0', ''),
                'leech': leech.replace('\xa0', ''),
                'magnet': magnet
            }

            torrents.append(torrent)
    return torrents
class Rutracker:
    def __init__(self) -> None:
        with requests.Session() as self.session:
            req = self.session.post(login, data, headers)




    def search(self, what):
        url = f"https://rutracker.net/forum/tracker.php?nm={what}"
        result = self.session.get(url)
        if result.status_code == 200:
            link_list = get_the_list_of_search_result(result.text)
            return get_the_torrent(link_list, self.session)




def main():
    request_for_seaerch = input("Что искать: ")
    my_eng = Rutracker()
    content = my_eng.search(request_for_seaerch)
    print(f"Количество: {len(content)}")

    for e in content:
        print(f"{e['title']}")
        print(f"{e['info']} | {e['seed']} | {e['leech']}")
        print(f"Страница раздачи: {e['description']}")
        print(f"Magnet-ссылка: {e['magnet']}")
        print("*****************************************************************************")


if __name__ == '__main__':
    main()
