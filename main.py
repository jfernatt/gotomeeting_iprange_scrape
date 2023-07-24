import requests
from bs4 import BeautifulSoup
from ipaddress import IPv4Network


def main():
    list_url = 'https://support.goto.com/meeting/help/allowlisting-and-firewall-configuration'
    response = requests.get(list_url)
    network_list = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, features='html.parser')
        tables = soup.find_all('table')
        table = [i for i in tables if i.attrs['id'] in 'd418e28'][0]
        rows = table.find_all('tr')
        cols = [i for i in rows[1::]]
        tds = [i.td for i in cols]
        for td in tds:
            sibs = [i for i in td.next_siblings]
            try:
                network_list.append(IPv4Network(sibs[-2].text.rstrip()))
            except Exception as e:
                print(e)
                print(f'Error Converting {sibs[-2].text} to IPv4 Network')
        print('IP Networks:')
        [print(f' {i.exploded}') for i in network_list]

    else:
        print(f'Error retrieving {list_url}\nStatus Code: {response.status_code}')


if __name__ == '__main__':
    main()
