import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://github.com/login'
LOGIN_URL = 'https://github.com/session'

# 全局的session，因为涉及到一系列的请求，都要公用这个session
SESSION = requests.session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
}


def get_authenticity_token():
    # get请求，获取一个session的resp
    resp = SESSION.get(BASE_URL, headers=HEADERS)
    if resp.status_code != 200:
        raise Exception('Maybe your ip is denied or your network is unnormal')
    soup = BeautifulSoup(resp.text, 'html.parser')

    # 找到auth code
    token = soup.find(attrs={'name': 'authenticity_token'}).get('value')
    return str(token)


def login(name, passwd, token):
    form = {
        'login': name,
        'password': passwd,
        'commit': 'Sign in',
        'authenticity_token': token,
        'utf8': '%E2%9C%93' # 符号：√
    }

    SESSION.post(url=LOGIN_URL, data=form, headers=HEADERS)


if __name__ == '__main__':
    check_url = 'https://github.com/'
    login_name = input('input your name\n')
    login_pass = input('input your password\n')

    # 获取auth code
    authenticity_token = get_authenticity_token()
    print("auth code: ", authenticity_token)

    login(login_name, login_pass, authenticity_token)
    resp = SESSION.get(check_url, headers=HEADERS)
    assert 'Sign out' in resp.text, "login failed, please check your name and password"

    print('login succeeded')
