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
        self.exchange_rate = self.get_nbp_rate()

    def get_nbp_rate(self):
        try:
            res = requests.get("https://api.nbp.pl/api/exchangerates/rates/a/eur/?format=json", timeout=5)
            return res.json()['rates'][0]['mid']
        
        except Exception:
            print("Could not fetch NBP rate. Using default: 4.3")
            return 4.3
        
    def get_product(self, sku):
        try:
            price, stock, weight = 0, 0, 0
            
            search_res = requests.get(self.base_url, params={'search': sku}, headers=self.headers, timeout=10)
            soup = BeautifulSoup(search_res.text, 'html.parser')

            product_url = None
            if not soup.find('h1', class_='product-detail-name'):
                link_tag = soup.find('a', class_='product-name')
                if link_tag:
                    product_url = link_tag.get('href')
            
            if product_url:
                res = requests.get(product_url, headers=self.headers, timeout=10)
                soup = BeautifulSoup(res.text, 'html.parser')
            
            # PRICE
            p_tag = soup.find('meta', {'itemprop': 'price'}) or soup.find('p', class_='product-detail-price')
            if p_tag:
                val = p_tag.get('content') if p_tag.name == 'meta' else p_tag.get_text()
                price = float(re.sub(r'[^\d.]', '', str(val).replace(',', '.')))

            # STOCK 
            stock_info = soup.find('p', class_='stock-information')
            if stock_info:
                txt = stock_info.get_text().lower()
                if "out of stock" in txt or "no longer available" in txt:
                    stock = 0
                else:
                    nums = re.findall(r'\d+', txt)
                    stock = int(nums[0]) if nums else 1

            # WEIGHT 
            weight = 0.0
            
            weight_label = soup.find(['span', 'td', 'th'], string=re.compile(r'Weight|Gewicht', re.I))
            
            if weight_label:
                parent_row = weight_label.find_parent('tr')
                if parent_row:
                    cells = parent_row.find_all('td')
                    if len(cells) > 1:
                        w_txt = cells[-1].get_text(strip=True)
                    else:
                        w_txt = parent_row.get_text(strip=True)
                else:
                    val_tag = weight_label.find_next(['span', 'div'], class_=re.compile(r'value|content', re.I))
                    w_txt = val_tag.get_text(strip=True) if val_tag else ""

                w_txt = w_txt.replace(',', '.')
                w_match = re.findall(r'\d+\.?\d*', w_txt)
                if w_match:
                    weight = float(w_match[0])

            return price, stock, weight
        except Exception as e:
            print(f"Błąd dla {sku}: {e}")
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
                'Exchange Rate': self.exchange_rate,
                'Total Value PLN': round(price * qty * self.exchange_rate, 2)
            })

            time.sleep(random.uniform(1, 2))

        return results

if __name__ == "__main__":
    
    try:
        df1 = pd.read_excel("inquiry.xlsx")
        customer_inqury = dict(zip(df1["sku"], df1["qty"]))

    except FileNotFoundError:
        print("File not found")
        exit()

    except KeyError:
        print("Error. File does not have columns 'sku' and 'qty'")
        exit()

    app = KemmlerB2BTool()
    data = app.create_offer(customer_inqury)

    df = pd.DataFrame(data)
    filename = "KEMMLER_OFERTA.xlsx"
    df.to_excel(filename, index=False)
    
    print(f"\n✅ Ready! File {filename} created.")
    print(f"📈 EUR/PLN rate (NBP): {app.exchange_rate}")