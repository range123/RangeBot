from requests.exceptions import ConnectionError, HTTPError, ReadTimeout
import backoff,requests
from urllib3.exceptions import ProtocolError
import chess,random
try:
    from http.client import RemoteDisconnected
    # New in version 3.5: Previously, BadStatusLine('') was raised.
except ImportError:
    from http.client import BadStatusLine as RemoteDisconnected

class OpeningExplorer:
    def __init__(self):
        self.url = 'https://explorer.lichess.ovh/master'

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
    def get_best_move(self,board):
        response = self.api_get(self.url+'?fen='+board.fen()+'&'+','.join(map(str,board.move_stack)))
        if len(response['moves']) == 0:
            return None
        move = chess.Move.from_uci(response['moves'][0]['uci'])
        return move
    def get_random_move(self,board):
        response = self.api_get(self.url+'?fen='+board.fen()+'&'+','.join(map(str,board.move_stack)))
        if len(response['moves']) == 0:
            return None
        move = chess.Move.from_uci(random.choice(response['moves'])['uci'])
        return move