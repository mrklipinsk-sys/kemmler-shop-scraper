import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re

class KemmlerB2BTool:
    def __init__(self):
        self.base_url = "https://www.kemmler-shop.de/en/search" 
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
        self.kurs_eur = self.get_nbp_rate()

    def get_nbp_rate(self):
        try:
            res = requests.get("https://api.nbp.pl/api/exchangerates/rates/a/eur/?format=json", timeout=5)
            return res.json()['rates'][0]['mid']
        except:
            return 4.3
        
    def get_product(self, sku):
        try:
            res = requests.get(self.base_url, params = {'search': sku}, headers=self.headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')

            price_tag = soup.find('meta', {'itemprop': 'price'})
            price = float(price_tag['content']) if price_tag else 0 

            stock = 0
            stock_tag = soup.find('p', class_='stock-information')
            if stock_tag:
                stock_nums = re.findall(r'\d+', stock_tag.get_text())
                if stock_nums:
                    stock = int(stock_nums[0])

            weight = 0
            weight_tag = soup.find('span', string=re.compile('Weight'))
            if weight_tag:
                weight_val = weight_tag.find_next('span', class_='custom-field-value')
                weight = float(weight_val.get_text().strip()) if weight_val else 0

            return price, stock, weight
        except:
            return 0, 0, 0 
    
    def create_offer(self, sku_qty_list):

        results = []

        for sku, qty in sku_qty_list.items():
            price, stock, weight = self.get_product(sku)
            
            results.append({
                'SKU': sku,
                'Order Qty': qty,
                'Stock Available': stock,
                'Unit Weight (kg)': weight,
                'Base Price EUR': price,
                'Discount %': 0.0, 
                'Exchange Rate': self.kurs_eur
            })

            time.sleep(random.uniform(1, 2))

        return results

if __name__ == "__main__":
    
    klient_zamowienie = {
        "DC.402.P2.20.100": 10,
        "DC.403.02.10.1": 5
    }

    app = KemmlerB2BTool()
    data = app.create_offer(klient_zamowienie)

    
    df = pd.DataFrame(data)
    filename = "KEMMLER_OFERTA.xlsx"
    df.to_excel(filename, index=False)
    
    print(f"\n✅ Gotowe! Plik {filename} wygenerowany.")
    print(f"📈 Zastosowany kurs EUR (NBP): {app.kurs_eur}")