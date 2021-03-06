import random
import chess,time
import chess.syzygy as syzygy
from NetworkTableBase import TableBase
from types import GeneratorType
# For making recursion iterative
def bootstrap(f, stack=[]):
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to

    return wrappedfunc
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
                chess.ROOK : 5,
                chess.KING : 100000}
class RangeEngine(EngineWrapper):
    def __init__(self, board, commands, options, silence_stderr=False):
        self.engine = Dummy()
        self.board = board
        self.inf = pow(10,8)
        self.depth = 4
        self.count = 0
        self.piece_values = material
        self.tb = TableBase()
        self.table = {}
        self.square_table = square_table = {
            1: [
                0, 0, 0, 0, 0, 0, 0, 0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                5, 5, 10, 25, 25, 10, 5, 5,
                0, 0, 0, 20, 20, 0, 0, 0,
                5, -5, -10, 0, 0, -10, -5, 5,
                5, 10, 10, -20, -20, 10, 10, 5,
                0, 0, 0, 0, 0, 0, 0, 0
            ],
            2: [
                -50, -40, -30, -30, -30, -30, -40, -50,
                -40, -20, 0, 0, 0, 0, -20, -40,
                -30, 0, 10, 15, 15, 10, 0, -30,
                -30, 5, 15, 20, 20, 15, 5, -30,
                -30, 0, 15, 20, 20, 15, 0, -30,
                -30, 5, 10, 15, 15, 10, 5, -30,
                -40, -20, 0, 5, 5, 0, -20, -40,
                -50, -40, -30, -30, -30, -30, -40, -50,
            ],
            3: [
                -20, -10, -10, -10, -10, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 5, 5, 10, 10, 5, 5, -10,
                -10, 0, 10, 10, 10, 10, 0, -10,
                -10, 10, 10, 10, 10, 10, 10, -10,
                -10, 5, 0, 0, 0, 0, 5, -10,
                -20, -10, -10, -10, -10, -10, -10, -20,
            ],
            4: [
                0, 0, 0, 0, 0, 0, 0, 0,
                5, 10, 10, 10, 10, 10, 10, 5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                0, 0, 0, 5, 5, 0, 0, 0
            ],
            5: [
                -20, -10, -10, -5, -5, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 5, 5, 5, 0, -10,
                -5, 0, 5, 5, 5, 5, 0, -5,
                0, 0, 5, 5, 5, 5, 0, -5,
                -10, 5, 5, 5, 5, 5, 0, -10,
                -10, 0, 5, 0, 0, 0, 0, -10,
                -20, -10, -10, -5, -5, -10, -10, -20
            ],
            6: [
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -20, -30, -30, -40, -40, -30, -30, -20,
                -10, -20, -20, -20, -20, -20, -20, -10,
                20, 20, 0, 0, 0, 0, 20, 20,
                20, 30, 10, 0, 0, 10, 30, 20
            ]
        }
    def first_search(self, board, movetime):
        # return random.choice(list(board.legal_moves))
        self.board = board.copy()
        self.count =  0
        self.depth = 4
        result =  self.alphabeta(-self.inf-1,self.inf+1,self.board.turn,self.depth)[1]
        # print('Nodes searched : {}, Move : {}',self.count,result)
        return result

    def search_with_ponder(self, board, wtime, btime, winc, binc, ponder=False):
        # return random.choice(list(board.legal_moves)),chess.Move.from_uci('e2e4')
        self.board = board.copy()
        self.count =  0
        
        # if pieces>15:
        #     self.depth = 4
        # elif pieces<=15 and pieces>=8:
        #     self.depth = 6
        self.depth = 4
        if len(board.piece_map()) <= 10:
            self.depth=6
        print('searching for depth = {}'.format(self.depth))
        # result = self.alphabeta(-self.inf-1,self.inf+1,self.board.turn,self.depth)[1],None
        while True:
            try:
                result = self.alphabeta(-self.inf-1,self.inf+1,self.board.turn,self.depth)[1],None
                break
            except:
                pass

        return result

    def search(self, board, wtime, btime, winc, binc):
        # return random.choice(list(board.legal_moves))
        self.board = board.copy()
        self.count =  0
        self.depth = 4
        if len(board.piece_map()) <= 10:
            self.depth=6
        result = self.alphabeta(-self.inf-1,self.inf+1,self.board.turn,self.depth)[1]
        # result = self.optimized_alphabeta(self.board,-self.inf-1,self.inf+1,self.board.turn,self.depth).compute()[1]
        # print('Nodes searched : {}, Move : {}',self.count,result)
        return result

    def quit(self):
        pass
    def stop(self):
        pass
    def name(self):
        return 'Rangefish'
        # self.engine.stop()


    def print_stats(self):
        # print('Depth searched = {}'.format(self.depth+10))
        print('Nodes searched = {}'.format(self.count))


    def get_stats(self):
        # return self.get_handler_stats(self.engine.info_handlers[0].info, ["depth", "nps", "nodes", "score"])
        return 'get_stats'

    def eval(self,board):
        # return self.material_eval(board)
        return self.material_eval(board)+self.position_eval(board)/100
    
    def position_eval(self,board):
        score = 0
        # iterate through the pieces
        for i in range(1, 7):
            # eval white pieces
            w_squares = board.pieces(i, chess.WHITE)
            # score += len(w_squares) * self.piece_values[i]
            for square in w_squares:
                score += self.square_table[i][-square]

            b_squares = board.pieces(i, chess.BLACK)
            # score -= len(b_squares) * self.piece_values[i]
            for square in b_squares:
                score -= self.square_table[i][square]

        return score
    def material_eval(self,board):
        # TODO need to give higher eval for less pieces
        # board = self.board
        b,w = 0,0
        for i in range(1,6):
            w+=len(board.pieces(i,chess.WHITE))*material[i]
            b-=len(board.pieces(i,chess.BLACK))*material[i]
        return (w+b)*(32/len(board.piece_map()))


    def order_moves(self,board):
        # board = board.copy()
        def key_func(move):
            board.push(move)
            val,depth =  self.table.get(hash(str(board)),(self.eval(board),0))
            board.pop()
            return val
        moves = list(board.legal_moves)
        moves.sort(key=key_func,reverse=board.turn)
        return moves


    def addtotable(self,board,val,dep):
        h = hash(str(board))
        if (h in self.table and self.table[h][1]<dep) or (h not in self.table):
            self.table[h] = (val,dep)


    @bootstrap
    def alphabeta(self,alpha,beta,ismax,depth):
        board = self.board
        self.count+=1
        moves = self.order_moves(board)
        if board.is_checkmate():
            if board.result() == "1-0":
                yield 1000000,None
            elif board.result() == "0-1":
                yield -1000000,None
        elif board.can_claim_draw() or len(moves) == 0:
            yield 0,None
        else:

            pieces = len(board.piece_map())
            if pieces<=7 and depth == 4:
                yield self.tb.get_eval_and_move(board.fen())


            if depth <= 0:
                self.depth = depth
                # return self.eval(board),None
                yield self.eval(board),None
            else:
                if ismax:
                    best = -self.inf
                    bmove = None
                    for move in moves:
                        board.push(move)
                        value,_= yield self.alphabeta(alpha,beta,False,depth-1)
                        board.pop()
                        if value>best:
                            best = value
                            bmove=move
                        alpha = max(alpha,best)
                        if beta<=alpha:
                            break
                    self.addtotable(board,best,self.depth-depth)
                    yield best,bmove
                else:
                    best = self.inf
                    bmove = None
                    for move in moves:
                        board.push(move)
                        value,_= yield self.alphabeta(alpha,beta,True,depth-1)
                        board.pop()
                        if value<best:
                            best = value
                            bmove = move
                        beta = min(beta,best)
                        if beta<=alpha:
                            break
                    self.addtotable(board,best,self.depth-depth)
                    yield best,bmove

    def probe(self,board1):
        board = board1.copy()
        with chess.syzygy.open_tablebase("tablebases/") as tablebase:
            # return tablebase.probe_wdl(board)
            return tablebase.probe_wdl(board),tablebase.probe_dtz(board)






def main():
    # fen = '8/2p1P1k1/8/1p3QNP/1P1P1B2/KP3P2/7P/5R2 w - - 1 51'
    # fen = 'r1bqr1k1/pp3pbp/5np1/2np4/5B2/2N1PN2/PP2BPPP/2RQK2R w K - 4 15'
    # fen = 'N2k1b1r/3b1ppp/5n2/4pq2/1Q6/2N5/PP2PPPP/n1BK1B1R w - - 11 21'
    # fen = 'r1b1kb1r/p3pppp/2p5/3pB3/8/2q1PN2/P1P2PPP/R2Q1RK1 b kq - 1 11'
    # fen = '6kr/8/p6p/8/8/3K4/8/8 b - - 17 70'
    board = chess.Board()
    board.push(chess.Move.from_uci('e2e4'))
    board.push(chess.Move.from_uci('e7e5'))
    print(board.move_stack)
    # print(board)
    # tb = TableBase()
    # print(tb.get_eval_and_move(fen))
    # with chess.syzygy.open_tablebase("tablebases/") as tablebase:
    #     print(tablebase.probe_wdl(board))
    #     print(tablebase.probe_dtz(board))
    # engine = RangeEngine(board,None,None)
    # move = engine.search_with_ponder(board,1,1,1,1)[0]


if __name__ == '__main__':
    main()
    