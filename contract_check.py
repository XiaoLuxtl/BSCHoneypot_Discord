import re
import requests_html

def contract_check(contractaddr):

    if len(contractaddr) != 42:
        message = "¿El contrato está bien escrito? (n>42)"
        print(message)
        return

    _is_valid_contract = re.fullmatch(r'^0x\w*', contractaddr)
    if _is_valid_contract == None:
        message = "¿El contrato está bien escrito? (regexp fail)"
        print(message)
        return

    url = f'https://honeypot.is/?address={contractaddr}'
    url_busd = f'https://honeypot.is/busd.html?address={contractaddr}'

    # Revisar que no diga unable en compra BNB
    session = requests_html.HTMLSession()
    r = session.get(url)
    r.html.render(sleep=5, timeout=8)
    # Do ya'thang
    _all1 = r.html.xpath('//*[@id="shitcoin"]/div//p/text()')

    if "unable" in _all1:
        r = session.get(url_busd)
        r.html.render(sleep=5, timeout=8)
        # Do ya'thang
        _all1 = r.html.xpath('//*[@id="shitcoin"]/div//p/text()')

    # Si dice, intenta compra BUSD

    _final_text = '---- ---- ---- ---- ---- \n'

    if len(_all1) == 7:
        print_order = [2, 1, 0, 3, 4, 5, 6]
        print(_all1)
        for p in print_order:
            _final_text = _final_text + _all1[p] + " \n"
        _final_text = _final_text + f'https://poocoin.app/tokens/{contractaddr}' + " \n"
    elif len(_all1) == 8:
        print_order = [2, 1, 0, 3, 4, 5, 6, 7]
        print(_all1)
        for p in print_order:
            _final_text = _final_text + _all1[p] + " \n"
        _final_text = _final_text + f'https://poocoin.app/tokens/{contractaddr}' + " \n"
    else:
        for p in range(len(_all1)):
            _final_text = _final_text + _all1[p] + " \n"
        _final_text = _final_text + f'https://poocoin.app/tokens/{contractaddr}' + " \n"

    print(_final_text)

    #
    # _final_text = f"Token: {_name[0]} @BSC\n" \
    #               f"{_address[0]} \n" \
    #               f"{_is_scam[0]} \n" \
    #               f"{_tax_buy[0]} \n" \
    #               f"{_tax_sell[0]} \n" \
    #               f"Info extracted from: {url}"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    contractaddr = '0xa6e78ad3c9b4a79a01366d01ec4016eb3075d7a0'
    contract_check(contractaddr)