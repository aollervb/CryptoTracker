from selenium import webdriver
import pygsheets
import pandas as pd


def scrape_price():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
    names = ['bitcoin', 'ethereum', 'cardano', 'tether', 'dogecoin', 'stellar']

    prices = {}

    for name in names:
        driver.get("https://coinmarketcap.com/currencies/" + name + "/")
        price_str = driver.find_element_by_class_name("priceValue").text
        price = price_str.split("$")[1].replace(",", "")

        try:
            prices[name] = float(price)
            print(name, " ", price)
        except ValueError:
            print("Order value is invalid ", price)

    print(prices)

    return prices


def modify_g_sheet(price):
    gc = pygsheets.authorize(service_file='client_secret.json')
    keys = list(price.keys())
    values = list(price.values())
    df = pd.DataFrame(values)
    sh = gc.open('CryptoPriceTracker')
    wks = sh[0]
    df = df.transpose()
    df.columns = keys
    wks.set_dataframe(df, (1, 1))
    return


def main():
    """
        get prices and after modify the google sheet
    """
    price = scrape_price()
    modify_g_sheet(price)
    return


if __name__ == '__main__':
    main()
