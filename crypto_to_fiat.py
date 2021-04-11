from datetime import datetime
import json
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


def get_converter_cache(url, parameters):
    headers = {'Accepts': 'application/json'}
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        json_cache = json.loads(response.text)

        return json_cache

    except (ConnectionError, Timeout, TooManyRedirects) as exception:
        print(exception)


# function for the preset wallets
def coins_to_euros(amount, coin):
    for i, v in enumerate(cache):
        if v['name'] == coin:
            coin_in_euros = v['quote']['EUR']['price']
            all_euros = round(amount * coin_in_euros, 2)

            return all_euros


def count_euros(ada_euros, btc_euros, dai_euros, eth_euros, xmr_euros):
    counted = round(ada_euros + btc_euros + dai_euros + eth_euros + xmr_euros, 2)
    return counted


# output for .csv tracking
def pretty_print_plot_points():
    today = datetime.now()
    # {:.2f} only desired for wallets ending in '.00'
    prettied_up = f"date, ada, ada_euros, btc, btc_euros, dai, dai_euros, eth, eth_euros, xmr,xmr_euros, total_euros " \
                  f"{today.strftime('%d/%m/%Y')}, {ada:.2f}, {ada_euros}, {btc}, {btc_euros}, {dai:.2f}, {dai_euros}," \
                  f" {eth} {eth_euros}, {xmr}, {xmr_euros}, {total_euros}"

    return prettied_up


def get_coins_currencies_lists():
    coin_list = ''
    currency_list = ''

    for i, v in enumerate(zip(cache, currencies)):
        coin_list += str(f"{cache[i]['name']} {cache[i]['symbol']} \n")
        currency_list += str(f"{currencies[i]['name']} {currencies[i]['symbol']} \n")
        print(coin_list, currency_list)

    return coin_list, currency_list


# preset wallets
ada = float(242.00)
btc = float(6.5591423)
dai = float(2543.00)
eth = float(5.42008404423153487)
xmr = float(42.6592010)

# set conversion output to EUR
json_cache = get_converter_cache('https://web-api.coinmarketcap.com/v1/cryptocurrency/listings/latest', {'convert': 'EUR'})
cache = json_cache['data']
currency_list_cache = get_converter_cache('https://web-api.coinmarketcap.com/v1/fiat/map', '')
currencies = currency_list_cache['data']

ada_euros = coins_to_euros(ada, 'Cardano')
btc_euros = coins_to_euros(btc, 'Bitcoin')
dai_euros = coins_to_euros(dai, 'Dai')
eth_euros = coins_to_euros(eth, 'Ethereum')
xmr_euros = coins_to_euros(xmr, 'Monero')
total_euros = count_euros(ada_euros, btc_euros, dai_euros, eth_euros, xmr_euros)
prettied_up = pretty_print_plot_points()
coin_list, currency_list = get_coins_currencies_lists()
