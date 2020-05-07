import random
import chess
class EngineWrapper:

    def __init__(self, board, commands, options=None, silence_stderr=False):
        pass

    def set_time_control(self, game):
        pass

    def first_search(self, board, movetime):
        pass

    def search(self, board, wtime, btime, winc, binc):
        pass

    def print_stats(self):
        pass

    def name(self):
        return self.engine.name

    def quit(self):
        self.engine.quit()

    def print_handler_stats(self, info, stats):
        for stat in stats:
            if stat in info:
                print("    {}: {}".format(stat, info[stat]))

    def get_handler_stats(self, info, stats):
        stats_str = []
        for stat in stats:
            if stat in info:
                stats_str.append("{}: {}".format(stat, info[stat]))

        return stats_str
class Dummy:
    def __init__(self):
        pass
    def stop(self):
        pass
    def ponderhit(self):
        pass
material = {chess.PAWN : 1,
                chess.QUEEN : 9,
                chess.KNIGHT : 3.1,
                chess.BISHOP : 3.25,
                chess.ROOK : 5}
class RangeEngine(EngineWrapper):
    def __init__(self, board, commands, options, silence_stderr=False):
        self.engine = Dummy()
        self.board = board
        self.inf = pow(10,8)
        self.depth = 4
        self.count = 0
        self.map = dict()
    def first_search(self, board, movetime):
        # return random.choice(list(board.legal_moves))
        return self.alphabeta(-self.inf-1,self.inf+1,self.board.turn,self.depth)[1]

    def search_with_ponder(self, board, wtime, btime, winc, binc, ponder=False):
        # return random.choice(list(board.legal_moves)),chess.Move.from_uci('e2e4')
        return self.alphabeta(-self.inf-1,self.inf+1,self.board.turn,self.depth)[1],chess.Move.from_uci('e2e4')

    def search(self, board, wtime, btime, winc, binc):
        # return random.choice(list(board.legal_moves))
        return self.alphabeta(-self.inf-1,self.inf+1,self.board.turn,self.depth)[1]

    def quit(self):
        pass
    def stop(self):
        pass
    def name(self):
        return 'Rangefish'
        # self.engine.stop()


    def print_stats(self):
        return 'print_stats'


    def get_stats(self):
        # return self.get_handler_stats(self.engine.info_handlers[0].info, ["depth", "nps", "nodes", "score"])
        return 'get_stats'

    def eval(self):
        return self.material_eval()
    def material_eval(self):
        # TODO need to give higher eval for less pieces
        board = self.board
        b,w = 0,0
        for i in range(1,6):
            w+=len(board.pieces(i,chess.WHITE))*material[i]
            b-=len(board.pieces(i,chess.BLACK))*material[i]
        return (w+b)*(32/len(board.piece_map()))

    def alphabeta(self,alpha,beta,ismax,depth):
        board = self.board
        self.count+=1
        moves = list(self.board.legal_moves)
        # moves = self.order_moves()

        # if there are no legal moves, check for checkmate / stalemate
        if board.is_checkmate():
            if board.result() == "1-0":
                return 1000000,chess.Move.from_uci('e4e5')
            elif board.result() == "0-1":
                return -1000000,chess.Move.from_uci('e4e5')
        elif board.can_claim_draw():
            return 0,chess.Move.from_uci('e4e5')
        if depth <= 0:
            return self.eval(),chess.Move.from_uci('e4e5')
        if board.board_fen() in self.map:
            return self.map[board.board_fen()]
        if ismax:
            best = -self.inf
            bmove = None
            for move in board.legal_moves:
                board.push(move)
                value,_= self.alphabeta(alpha,beta,False,depth-1)
                board.pop()
                if value>best:
                    best = value
                    bmove=move
                alpha = max(alpha,best)
                if beta<=alpha:
                    break
            self.map[board.board_fen()] = (value,bmove)
            return best,bmove
        else:
            best = self.inf
            bmove = None
            for move in board.legal_moves:
                board.push(move)
                value,_= self.alphabeta(alpha,beta,True,depth-1)
                board.pop()
                if value<best:
                    best=  value
                    bmove = move
                beta = min(beta,best)
                if beta<=alpha:
                    break
            self.map[board.board_fen()] = (value,bmove)
            return best,bmove
    def iterative_alphabeta(self,alpha,beta,ismax,depth):
        dfs = []
        dfs.append((self.board,alpha,beta,ismax,depth))
        while dfs:
            board,alpha,beta,ismax,depth = dfs.pop()


if __name__ == '__main__':
    # fen = input()
    fen = 'r1bqkb1r/pppp1ppp/5n2/1B2p3/3nP3/2N2N2/PPPP1PPP/R1BQK2R w KQkq - 6 5'
    # fen2 = 'r1bqkb1r/pppp1ppp/5n2/1B2p3/3nP3/2N2N2/PPPP1PPP/R1BQK2R w KQkq - 6 5'
    board = chess.Board(fen)    
    # board2 = chess.Board(fen2)
    # print(board1 == board2)
    engine = RangeEngine(board,None,None)
    engine.search(board,1,1,1,1)
    print(engine.count)
    # print(engine.alphabeta(-engine.inf-1,engine.inf+1,board.turn,2))
    # print(engine.material_eval())
    
    # print(len(board.piece_map()))
    