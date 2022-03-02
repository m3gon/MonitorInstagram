import requests , threading , random
from discord_webhook import DiscordEmbed , DiscordWebhook
from queue import Queue
from colorama import Fore , init
init(autoreset=True)
class HTTP:
    def http_request(self, request, url, headers, data, proxy):
        if request == 'POST':
            if data and not proxy:
                return requests.post(url, headers=headers, data=data)
            elif data and proxy:
                return requests.post(url, headers=headers, data=data, proxies=proxy)
        elif request == 'GET':
            if not proxy:
                return requests.get(url, headers=headers)
            if proxy:
                return requests.get(url, headers=headers, proxies=proxy)
class Color:
    def color(self, color, text):
        if color == 'MAGENTA':
            return Fore.LIGHTMAGENTA_EX + text + Fore.RESET
        elif color == 'GREEN':
            return Fore.LIGHTGREEN_EX + text + Fore.RESET
        elif color == 'RED':
            return Fore.LIGHTRED_EX + text + Fore.RESET
        elif color == 'RESET':
            return Fore.RESET
class Files:
    def __init__(self):
        self.c = Color()
    def check_file_proxies(self, name_file='proxies.txt'):
        try:
            self.file_proxies = open(name_file).read().splitlines()
            print("[" + self.c.color("GREEN","+") + f"] Successfully Loaded '{self.c.color('GREEN','proxies.txt')}'")
            if len(open(name_file).read().splitlines()) == 0:
                print("[" + self.c.color("GREEN","+") + f"] Please Open File '{self.c.color('GREEN','proxies.txt')}' And Enter Proxies\n[{self.c.color('GREEN','+')}] Press Enter To Exit")
                input()
                exit(0)
            else:
                pass
        except FileNotFoundError:
            self.create_file_proxies = open('proxies.txt', 'a')
            print("[" + self.c.color("GREEN","+") + f"] Successfully Create File '{self.c.color('GREEN','proxies.txt')}'\n[{self.c.color('GREEN','+')}] Please Open File '{self.c.color('GREEN','proxies.txt')}' And Enter Proxies\n[{self.c.color('GREEN','+')}] Press Enter To Exit")
            input()
            exit(0)
    def check_file_target(self, name_file='target.txt'):
        try:
            self.file_target = open(name_file).read().splitlines()
            print("[" + self.c.color("GREEN","+") + f"] Successfully Loaded '{self.c.color('GREEN','target.txt')}'")
            if len(open(name_file).read().splitlines()) == 0:
                print("[" + self.c.color("GREEN","+") + f"] Please Open File '{self.c.color('GREEN','target.txt')}' And Enter Target\n[{self.c.color('GREEN','+')}] Press Enter To Exit")
                input()
                exit(0)
            else:
                pass
        except FileNotFoundError:
            self.create_file_target = open('target.txt', 'a')
            print("[" + self.c.color("GREEN","+") + f"] Successfully Create File '{self.c.color('GREEN','target.txt')}'\n[{self.c.color('GREEN','+')}] Please Open File '{self.c.color('GREEN','target.txt')}' And Enter Target\n[{self.c.color('GREEN','+')}] Press Enter To Exit")
            input()
            exit(0)
class MonitorUsersInstagram:
    def __init__(self):
        self.q = Queue()
        self.HTTP = HTTP()
        self.Color = Color()
        self.discord = SendDiscord()
        self.attempts = 0
        self.error = 0
        self.rs = 0
        self.successfully = 0
        self.file_target = open('target.txt').read().splitlines()
    def use_queue(self):
        for self.x in self.file_target:
            self.q.put(self.x)
    def Main(self):
        while 1:
            usernameo = self.q.get()
            self.MonitorUsersInstagramS(usernameo)
    def thread(self, thread, function):
        for _ in range(thread):
            threading.Thread(target=function).start()
        rs_thread = threading.Thread(target=self.requestPS)
        rs_thread.setDaemon(True)
        rs_thread.start()
    def delete_target(self, username):
        self.file_target.remove(username)
    def save_target(self, username):
        with open('MonitroUserDone.txt', 'a') as self.save:
            self.save.write(f'@{username}' + '\n')
    def MonitorUsersInstagramS(self, username):
        try:
            self.req_check_target = self.HTTP.http_request('POST', 'https://www.instagram.com/accounts/web_create_ajax/attempt/', {'Host': 'www.instagram.com', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'X-Csrftoken': 'missing'}, {'username':username}, {'https': f"http://{random.choice(open('proxies.txt').read().splitlines())}", 'http': f"http://{random.choice(open('proxies.txt').read().splitlines())}", 'socks4': f"http://{random.choice(open('proxies.txt').read().splitlines())}", 'socks5': f"http://{random.choice(open('proxies.txt').read().splitlines())}"})
            if self.req_check_target.json()['errors']['username'][0]['message'] == "This username isn't available.":
                self.attempts +=1
                print(f"\r[+] Monitor Users Instagram | Attempts {self.attempts:,} | Get {self.successfully} | ERROR {self.error}", end='')
            elif self.req_check_target.json()['errors']['username'][0]['message'] == "This username isn't available. Please try another.":
                self.successfully +=1
                print(f"\r[+] Monitor Users Instagram | Attempts {self.attempts:,} | Get {self.successfully} | ERROR {self.error}", end='')
                self.discord.Send(username)
                self.save_target(username)
                self.delete_target(username)
            else:
                self.error +=1
            self.q.put(self.x)
        except requests.exceptions.ConnectionError:
            pass
        except:
            pass
class SendDiscord:
    def __init__(self):
        self.url_webhook = ''
    def Send(self, username):
        self.url = DiscordWebhook(url=self.url_webhook)
        self.data_discord = DiscordEmbed(title=f'Users : @{username}', color=000000)
        self.url.add_embed(self.data_discord)
        self.url.execute()
if __name__ == '__main__':
    CC = Color()
    F = Files()
    F.check_file_proxies()
    F.check_file_target()
    Instagram = MonitorUsersInstagram()
    Instagram.use_queue()
    print(f'[{CC.color("GREEN","+")}] Thread : ', end='')
    thread = int(input())
    Instagram.thread(thread, Instagram.Main)
