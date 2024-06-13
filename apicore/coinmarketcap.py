# scraper/coinmarketcap.py

import requests
from bs4 import BeautifulSoup

class CoinMarketCap:
    BASE_URL = "https://coinmarketcap.com/currencies/"

    def __init__(self, coin):
        self.coin = coin.lower()
        self.url = f"{self.BASE_URL}{self.coin}/"

    def scrape(self):
        page_content = self.fetch_page()
        soup = BeautifulSoup(page_content, 'html.parser')
        data = {
            "market_cap": self.extract_market_cap(soup),
            "volume_24h": self.extract_volume_24h(soup),
            "circulating_supply": self.extract_circulating_supply(soup),
            "total_supply": self.extract_total_supply(soup),
            "fully_diluted_market_cap": self.extract_fully_diluted_market_cap(soup),
            "contracts": self.extract_contracts(soup),
            "official_links": self.extract_official_links(soup),
            "socials": self.extract_socials(soup),
            "network_information": self.extract_network_information(soup),
            "ucid": self.extract_ucid(soup)
        }
        print(data)
        return data

    def fetch_page(self):
        response = requests.get(self.url)
        response.raise_for_status()
        return response.text

    def extract_market_cap(self, soup):
        try:
            market_cap = soup.find('div', string='Market cap').find_next('dd', class_='sc-d1ede7e3-0 hPHvUM base-text').text.strip()
            return market_cap
        except AttributeError:
            return None

    def extract_volume_24h(self, soup):
        try:
            volume_24h = soup.find('div', string='Volume (24h)').find_next('dd', class_='sc-d1ede7e3-0 hPHvUM base-text').text.strip()
            return volume_24h
        except AttributeError:
            return None

    def extract_circulating_supply(self, soup):
        try:
            circulating_supply = soup.find('div', string='Circulating supply').find_next('dd', class_='sc-d1ede7e3-0 hPHvUM base-text').text.strip()
            return circulating_supply
        except AttributeError:
            return None

    def extract_total_supply(self, soup):
        try:
            total_supply = soup.find('div', string='Total supply').find_next('dd', class_='sc-d1ede7e3-0 hPHvUM base-text').text.strip()
            return total_supply
        except AttributeError:
            return None

    def extract_fully_diluted_market_cap(self, soup):
        try:
            fully_diluted_market_cap = soup.find('div', string='Fully diluted market cap').find_next('dd', class_='sc-d1ede7e3-0 hPHvUM base-text').text.strip()
            return fully_diluted_market_cap
        except AttributeError:
            return None

    def extract_contracts(self, soup):
        contracts = []
        try:
            contracts_section = soup.find('div', {'data-role': 'stats-block'}).find_next('div', string='Contracts').find_next('div', class_='sc-d1ede7e3-0 bwRagp')
            for contract in contracts_section.find_all('a', class_='chain-name'):
                chain_name = contract.find('span', class_='sc-71024e3e-0 dEZnuB').text.strip()
                address = contract.find('span', class_='sc-71024e3e-0 eESYbg address').text.strip()
                link = contract['href']
                contracts.append({'chain_name': chain_name, 'address': address, 'link': link})
            return contracts
        except AttributeError:
            return None

    def extract_official_links(self, soup):
        official_links = []
        try:
            official_links_section = soup.find('div', {'data-role': 'stats-block'}).find_next('div', string='Official links').find_next('div', class_='sc-d1ede7e3-0 bwRagp')
            for link in official_links_section.find_all('a', rel='nofollow noopener'):
                name = link.text.strip()
                url = link['href']
                official_links.append({'name': name, 'url': url})
            return official_links
        except AttributeError:
            return None

    def extract_socials(self, soup):
        socials = []
        try:
            socials_section = soup.find('div', {'data-role': 'stats-block'}).find_next('div', string='Socials').find_next('div', class_='sc-d1ede7e3-0 bwRagp')
            for link in socials_section.find_all('a', rel='nofollow noopener'):
                name = link.text.strip()
                url = link['href']
                socials.append({'name': name, 'url': url})
            return socials
        except AttributeError:
            return None

    def extract_network_information(self, soup):
        network_info = {}
        try:
            network_info_section = soup.find('div', {'data-role': 'stats-block'}).find_next('div', string='Network information').find_next('div', class_='sc-d1ede7e3-0 bwRagp')
            chain_explorers = network_info_section.find('div', string='Chain explorers').find_next('a', rel='nofollow noopener')['href']
            supported_wallets = network_info_section.find('div', string='Supported wallets').find_next('a', rel='nofollow noopener')['href']
            network_info = {
                'chain_explorers': chain_explorers,
                'supported_wallets': supported_wallets
            }
            return network_info
        except AttributeError:
            return None

    def extract_ucid(self, soup):
        try:
            ucid = soup.find('div', {'data-role': 'stats-block'}).find_next('div', string='UCID').find_next('div', class_='BaseChip_labelWrapper__lZ4ii').text.strip()
            return ucid
        except AttributeError:
            return None

# Example usage
if __name__ == "__main__":
    coin_name = "duko"  # Just provide the coin name
    coin_scraper = CoinMarketCap(coin_name)
    data = coin_scraper.scrape()
    print(data)
