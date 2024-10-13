import datetime
import html
import pickle
import requests
import re
import smtplib

def set_data(data):
    try:
        with open("Database.pkl", "wb") as file:
            pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)
    except pickle.PicklingError as e:
        print(str(e))

def get_data():
    try:
        with open("Database.pkl", "rb") as file:
            data = pickle.load(file)
        return data
    except FileNotFoundError:
        set_data({})
        return {}
    except pickle.UnpicklingError as e:
        print(str(e))
        return {}

def notify_user(msg):
    my_email = ""
    my_passkey = ""
    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user = my_email, password = my_passkey)
            connection.sendmail(from_addr = my_email, to_addrs = email, msg = msg)
    except Exception as e:
        print(str(e))

def get_product():
    headers = {"Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Accept-Encoding": "gzip, deflate, br"
            }

    for i in range(10):
        try:
            response = requests.get(url = url, headers = headers)
            webpage = response.text

            name = re.search(name_pattern, webpage)
            price = re.search(price_pattern, webpage)
            if name and price:
                name = html.unescape(name.group().strip())
                price = float(price.group()[1:].replace(",", ""))
                break

        except requests.exceptions.RequestException as e:
            print(str(e))
            name = price = None

    return name, price

def delete_unresponsive():
    data[email][url][-1] += 1
    if data[email][url][-1] == 7:
            msg = f"Subject:Urgent Action Required: Unresponsive Product Link\n\nThe product link you provided has been unresponsive for the past week and appears to be inaccessible or experiencing technical difficulties.\n\nProduct Link: {url}\n\nTo prevent any further incovenience and maintain integrity of the service, please take the following actions:\n\n1. Verify accuracy of the product link provided and make necessary corrections.\n2.If the link has been changed please provide us with an updated link.\n3. If the product link is no longer available or product is out of stock please proceed to delete it from our database.\n\n Please note that if the product continues to remain unavailable it will be automatically erased from our database in the next 3 days.\nApologies for the inconvenience caused and your cooperation is appreciated."
            notify_user(msg)
    elif data[email][url][-1] == 10:
        delete_urls.append((email, url))

def monthly_check():
    if today.day == 1 and len(prices) > 1:
        min_price = prices[0]
        min_dates = [f"{str(key)}|{today.month - 1}|{today.year}" if today.month != 1 else f"{str(key)}|12|{today.year}" for key, value in data[email][url].items() if value == min_price and key > 0]
        min_dates = ", ".join(min_dates)

        max_price = prices[-1]
        max_dates = [f"{str(key)}|{today.month - 1}|{today.year}" if today.month != 1 else f"{str(key)}|12|{today.year}" for key, value in data[email][url].items() if value == max_price and key > 0]
        max_dates= ", ".join(max_dates)

        frange = max_price - min_price

        mean = sum(prices) / len(prices)
        
        mid = len(prices) // 2
        median = prices[mid] if len(prices) % 2 != 0 else (prices[mid - 1] + prices[mid]) / 2

        cov = (sum((price - mean) ** 2 for price in prices) / len(prices)) ** 0.5 / mean * 100
        if cov <= 5:
            cov_info = "Very Stable"
        elif cov <= 10:
            cov_info = "Stable"
        elif cov <= 20:
            cov_info = "Moderate"
        elif cov <= 40:
            cov_info = "Volatile"
        else:
            cov_info = "Very Volatile"

        msg = f"Subject:Monthly Price Insights: Discover Monthly Bargains on Your Favourite Picks\n\nProduct Name:  {name}\nYour Budget:  ₹{budget}\nCurrent Price:  ₹{price}\n\nGet ready to unleash the power of savings with our personally curated monthly Price Report on your top wishlisted item!\nWe have compiled the latest data to bring you exclusive insights and trends on the price dynamics of the market, helping you save big on your must have items.\n\nProduct Link:  {url}\n\nLowest Price =  ₹{min_price}  (on the dates {min_dates})\nHighest Price =  ₹{max_price}  (on the dates {max_dates})\nFluctuation Range =  ₹{frange}\nMean Price =  ₹{mean}\nMedian Price =  ₹{median}\nCoefficient of Variation =  {cov}%  ({cov_info})\n\nWith these invaluable insights at your fingertips, you can now strategize your purchasing decisions and optimize your savings to get the most bang for your buck.".encode("utf-8")
        notify_user(msg)

        data[email][url] = {-1: 0, 0: budget}

def daily_check():
    data[email][url][today.day] = price

    drop = round((budget - price)/budget * 100)
    if drop > 0:
        msg = f"Subject:{domain.title()} Price Slash: Huge Savings on Your Favourite Picks\n\nProduct Name:  {name}\nYour Budget:  ₹{budget}\nCurrent Price:  ₹{price}\n\nYour top wishlisted item is now {drop}% less than your specified budget!\nTo make sure you don't miss out on this opportunity, simply click on the link below to proceed with your purchase.\n\nProduct Link:  {url}\n\nHURRY NOW!".encode("utf-8")
        notify_user(msg)

delete_urls = []
data = get_data()

for email in data:
        urls = data[email]
        for url in urls:
            domain = re.search(r'(https?://(?:www\.)?)([a-z]+)(?=\.)', url).group(2)
            if domain == "amazon":
                name_pattern = r'(?<=class="a-size-large product-title-word-break">).+?(?=</span>)'
                price_pattern = r'(?<=<span class="a-offscreen">)[₹\d,.]+(?=</span>)'
            else:
                name_pattern = r'(?<=<span class="B_NuCI">)(.+?)(?=</span>)'
                price_pattern = r'(?<=<div class="_30jeq3 _16Jk6d">)[₹\d,.]+(?=</div>)'
    
            name, price = get_product()
            if not (name and price):
                delete_unresponsive()
                continue
            data[email][url][-1] = 0

            budget = data[email][url][0]
            prices = sorted(list(data[email][url].values())[2:])
            today = datetime.datetime.now()

            monthly_check()
            daily_check()

for email, url in delete_urls:
    del data[email][url]
    if not data[email]:
        del data[email]

set_data(data)

