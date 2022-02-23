from selenium import webdriver
import pygsheets
import pandas as pd
import numpy as np
import gspread


def scrape_price():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
    names = ['bitcoin', 'ethereum', 'cardano', 'tether', 'dogecoin', 'stellar', 'solana']

    assets = []
    value = []

    for name in names:
        driver.get("https://coinmarketcap.com/currencies/" + name + "/")
        price_str = driver.find_element_by_class_name("priceValue").text
        price = price_str.split("$")[1].replace(",", "")

        try:
            value.append(float(price))
            assets.append(name)
            print(name, " ", price)

        except ValueError:
            print("Order value is invalid ", price)

    array = [assets, value]

    return array


# def modify_g_sheet(price):
#     gc = pygsheets.authorize(service_file='client_secret.json')
#     keys = list(price.keys())
#     values = list(price.values())
#     df = pd.DataFrame(values)
#     sh = gc.open('CryptoPriceTracker')
#     wks = sh[0]
#     df = df.transpose()
#     df.columns = keys
#     wks.set_dataframe(df, (1, 1))
#     return

def modify_g_sheet(price):
    gc = gspread.service_account('client_secret.json')
    sh = gc.open('CryptoPriceTracker')
    wks = sh.get_worksheet(0)

    array = wks.get_all_values()

    for i in range(1,len(array)):
        array[i] = [n.replace(',', '') for n in array[i]]
        array[i] = list(map(float, array[i]))

    if len(array) == 0:
        array.append(price[0])
        array.append(price[1])
    else:
        array.append(price[1])

    l = len(array)
    cell_range = "A2:G" + str(l)
    wks.update('A1', array)

    wks.format(cell_range, {'numberFormat': {'type': "NUMBER"}})
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
