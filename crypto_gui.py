from guizero import App, Box, Combo, Picture, PushButton, Text, TextBox, Window
import crypto_to_euro as crypto


def wallet_selection(selected_value):

    coin_dict = {
        'Bitcoin': crypto.btc_euros,
        'Cardano': crypto.ada_euros,
        'Dai': crypto.dai_euros,
        'Ethereum': crypto.eth_euros,
        'Monero': crypto.xmr_euros,
        'All wallets totalled': crypto.total_euros,
        'Pretty print totals for .csv input': crypto.prettied_up
    }

    if selected_value in coin_dict:
        final_result.clear()
        final_result.append(coin_dict[selected_value])


def get_user_input():
    amount = amount_input_box.value
    coin = coin_input_box.value
    currency = currency_input_box.value

    def compute_conversion(amount, coin, currency):
        wallet = crypto.get_converter_cache('https://pro-api.coinmarketcap.com/v2/tools/price-conversion',
                                            {'amount': amount, 'symbol': coin, 'convert': currency})
        amount, coin = wallet['data'][0]['amount'], wallet['data'][0]['name']
        conversion_output = Text(input_box, grid=[1, 4], text='')
        conversion_output.clear()
        amount_input_box.clear()
        coin_input_box.clear()
        currency_input_box.clear()
        for currency in wallet['data'][0]['quote']:
            price = round(wallet['data'][0]['quote'][currency]['price'], 2)
            text_string = f'{amount} {coin} is {round(price, 2)} {currency}'
            conversion_output.append(text_string)

        return amount, coin, currency, price

    compute_conversion(amount, coin, currency)

    return amount, coin, currency


def new_window_coins():
    coins_or_currencies_list = Window(input_box, 'Coins')
    coins_or_currencies_list.bg = 'aquamarine4'
    coinlist = TextBox(coins_or_currencies_list, text=crypto.coin_list, height='fill', width='fill', multiline=True,
                       scrollbar=True)
    coinlist.text_size = 10


def new_window_currencies():
    coins_or_currencies_list = Window(input_box, 'Currencies')
    coins_or_currencies_list.bg = 'aquamarine4'
    currencylist = TextBox(coins_or_currencies_list, text=crypto.currency_list, height='fill', width='fill',
                           multiline=True, scrollbar=True)
    currencylist.text_size = 10


# GUI code
app = App('CryptoLuv', height=900, width=1424)
app.bg = 'aquamarine4'
font = 'Garamond'

title_box = Box(app, align='top')
title = Text(title_box, text='Choose a wallet to see how many € it is currently valued at', font=font, align='left')
title.text_size = 18
title.text_color = 'black'

wallet_box = Box(app, align='top', layout='grid')
wallet_title = Text(wallet_box, text='wallets  ', grid=[0, 0])
wallet_title.text_size = 20
wallet_title.text_color = 'gray18'

wallets_combo = Combo(wallet_box, grid=[2, 0], options=['Bitcoin', 'Cardano', 'Dai', 'Ethereum', 'Monero', 'All wallets '
                                                        'totalled', 'Pretty print totals for .csv input'], command=wallet_selection)
final_result = TextBox(wallet_box, grid=[3, 0])

content_box = Box(app, align='top')
request_user_input = Text(content_box, text='Convert crypto into fiat by entering data in format shown', align='top')
input_box = Box(content_box, layout='grid', align='left')

amount_input_label = Text(input_box, text='Amount [0.000]', grid=[0, 0], align='left')
amount_input_box = TextBox(input_box, grid=[1, 0])
coin_input_label = Text(input_box, text='Crypto [XMR]', grid=[0, 1], align='left')
coin_input_box = TextBox(input_box, grid=[1, 1])
currency_input_label = Text(input_box, text='Currency [EUR] ', grid=[0, 2], align='left')
currency_input_box = TextBox(input_box, grid=[1, 2],)
submit_compute_conversion = PushButton(input_box, text='Convert', grid=[2, 1], command=get_user_input)

get_coins_list = PushButton(input_box, text='Available coins', grid=[3, 1], command=new_window_coins)
get_coins_list.text_size = 8
get_currencies_list = PushButton(input_box, text='Available currencies', grid=[4, 1], command=new_window_currencies)
get_currencies_list.text_size = 8

image_box = Box(app, align='top')
genesis_block = Picture(image_box, align='right', height=550, width=950, image='GenesisBlock.png')

quote_box = Box(app, align='bottom')
quote3 = Text(quote_box, text='', align='bottom')
quote2 = Text(quote_box, text='violently out of the hands of government, all we can do is by some sly roundabout way '
                              'introduce something that they can’t stop."   ', font=font, align='bottom')
quote2.text_size = 13
quote2.text_color = 'white'
quote = Text(quote_box, text='   "I don’t believe we shall ever have a good money again before we take the thing out of '
                             'the hands of government, that is, we can’t take them   ', font=font, align='bottom')
quote.text_size = 13
quote.text_color = 'white'

app.display()
