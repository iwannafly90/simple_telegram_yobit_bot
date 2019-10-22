from unittest import TestCase
from unittest.mock import patch
from bot import app, get_price_in_usd


class Test(TestCase):
    INPUT_COINS = ['btc',
                   'wrong_coin']

    REQUEST_INPUTS = [
        {
            'ticker': {
                'last': '12345'
            }
        },
        {
            'error': 'wrong_input'
        }
    ]

    EXPECTED_OUTPUTS = [
        '12345 usd',
        'Указана неверная валюта. Валюту нужно указывать так, как она называется на сайте Yobit. ' \
               'Например, btc, eth, ltc'
    ]

    REQUEST_ANSWER = {
        'message': {
            'chat': {
                'id': 123
            },
            'text': 'btc'
        }
    }

    @patch('bot.send_message')
    def test_bot_run(self, send_message_mock):
        send_message_mock.return_value = True
        rv = app.test_client().post('/', json=self.REQUEST_ANSWER)
        assert send_message_mock.call_count == 1

    @patch('bot.requests.get')
    def test_get_price_in_usd(self, requests_get_mock):
        real_outputs = []
        for ind, val in enumerate(self.INPUT_COINS):
            requests_get_mock.return_value.json.return_value = self.REQUEST_INPUTS[ind]
            res = get_price_in_usd(val)
            real_outputs.append(res)

        assert real_outputs == self.EXPECTED_OUTPUTS
