import re
import requests


url = 'https://rutracker.net/forum/login.php'
url_2 = 'https://rutracker.net/forum/index.php'


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


class Item():

    def __init__(self, title, href, seedmed, leechmed, capacity):
        self.title = title
        self.href = href
        self.seedmed = seedmed
        self.leechmed = leechmed
        self.capacity = capacity

    def get_magnet_href(self, session):
        url = self.href
        result = session.get(url).text

        my_patern = re.compile(r"magnet:.*magnet\"")
        start = my_patern.search(result).start()
        end = my_patern.search(result).end()

        magnet_href = result[start:end-1]

        return magnet_href


# Поиск
def search(value, session):
    url = f"https://rutracker.net/forum/tracker.php?nm={value}"
    result = session.get(url)

    return result


def get_list_search(text):
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    my_patern = re.compile(r"<tbody>.*</tbody>")
    res = my_patern.search(text)
    text = text[res.start():res.end()]
    text = text.replace('><tr', '>\n<tr')

    my_patern = re.compile(r"<tr.*</tr>")
    return my_patern.findall(text)


def make_item_wrapper(list):
    items = []

    for res in list_of_res:
        res = res.replace("\">", "\">\n")

        my_patern = re.compile(r"bold\" href=\".*\">")
        start = my_patern.search(res).start()
        end = my_patern.search(res).end()
        href = f"https://rutracker.net/forum/{res[start+12:end-2]}"

        res = res.replace('\n', '')
        res = res.replace('</a></div>', '</a>\n</div>')
        my_patern = re.compile(r"viewtopic.*</a>")
        start = my_patern.search(res).start()
        end = my_patern.search(res).end()
        title = res[start:end]
        title = title[title.find('>')+1:len(title)-4]

        my_patern = re.compile(r"<a class=\"small tr-dl dl-stub\".*</a>")
        start = my_patern.search(res).start()
        end = my_patern.search(res).end()
        capacity = res[start:end]
        capacity = capacity[capacity.find('>')+1:len(capacity)-12]
        capacity = capacity.replace('&nbsp;', ' ')

        # res = res.replace("</td><td ", "</td>\n<td ")
        # my_patern = re.compile(r"seedmed\">.*</b>")
        # print(my_patern.search(res))
        # start = my_patern.search(res).start()
        # end = my_patern.search(res).end()
        # # seedmed = res[start+9:end-4]

        res = res.replace("</td><td ", "</td>\n<td ")
        my_patern = re.compile(r"Личи\">.*</td>")
        start = my_patern.search(res).start()
        end = my_patern.search(res).end()
        leechmed = res[start+6:end-5]

        # items.append(Item(title, href, seedmed, leechmed, capacity))
    return items


with requests.Session() as session:
    req = session.post(url, data, headers)

    text = search('Avatar', session).text

    list_of_res = get_list_search(text)

    print(len(list_of_res))
    items = make_item_wrapper(list_of_res)

    for item in items:
        print(f"{item.title} {item.capacity} {item.seedmed} {item.leechmed} ")
        print("######")

