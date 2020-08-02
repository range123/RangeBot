from requests.exceptions import ConnectionError, HTTPError, ReadTimeout
import backoff,requests
from urllib3.exceptions import ProtocolError
import chess
try:
    from http.client import RemoteDisconnected
    # New in version 3.5: Previously, BadStatusLine('') was raised.
except ImportError:
    from http.client import BadStatusLine as RemoteDisconnected

class TableBase:
    def __init__(self):
        self.url = 'http://tablebase.lichess.ovh/standard'

    def is_final(exception):
        return isinstance(exception, HTTPError) and exception.response.status_code < 500

    @backoff.on_exception(backoff.constant,
        (RemoteDisconnected, ConnectionError, ProtocolError, HTTPError, ReadTimeout),
        max_time=60,
        interval=0.1,
        giveup=is_final)
    def api_get(self, url):
        response = requests.get(url, timeout=2)
        response.raise_for_status()
        return response.json()
    def get_eval_and_move(self,fen):
        response = self.api_get(self.url+'?fen='+fen)
        wdl = response['wdl']
        move = chess.Move.from_uci(response['moves'][0]['uci'])
        if wdl == 2:
            return 1000000,move
        elif wdl == -2:
            return -1000000,move
        else:
            return 0,move
