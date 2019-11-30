import chess
import main

PIECE = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] = range(1, 7)
WHITE = 1
BLACK = 0
NIVEAU_DIFFICULTE = 3
ALGO_DEFENSIF = 0
ALGO_OFFENSIF = 1

# On cree le board de jeu
board = chess.Board()

#on retire les pieces de sur le jeu
board.clear_board()

#on cree des pieces qui ne sont pas encore sur le jeu
pion_w = chess.Piece(PAWN, WHITE)
cheval_w = chess.Piece(KNIGHT, WHITE)
fou_w = chess.Piece(BISHOP, WHITE)
tour_w = chess.Piece(ROOK, WHITE)
reine_w = chess.Piece(QUEEN, WHITE)
roi_w = chess.Piece(KING, WHITE)

pion_b = chess.Piece(PAWN, BLACK)
cheval_b = chess.Piece(KNIGHT, BLACK)
fou_b = chess.Piece(BISHOP, BLACK)
tour_b = chess.Piece(ROOK, BLACK)
reine_b = chess.Piece(QUEEN, BLACK)
roi_b = chess.Piece(KING, BLACK)

#on met certaines piece sur le jeu pour creer une situation (de test) precise

#TEST 1 : Priorite des pieces a capturer (pion vs reine)
#board.set_piece_at(25, pion_w, False)
#board.set_piece_at(34, reine_b, False)
#board.set_piece_at(32, pion_b, False)

#TEST 2 : Priorite entre promotion et capture
board.set_piece_at(49, pion_w, False)
board.set_piece_at(34, reine_b, False)
board.set_piece_at(25, pion_w, False)

#on ajoute les rois pour que la game soit dans un etat "normal"
board.set_piece_at(7, roi_w, False)
board.set_piece_at(23, roi_b, False)

#Permet de voir le board avant que l'IA fasse son tour
main.printBoard(board.__str__())

#on debute le jeu
main.tester(board, 'N', NIVEAU_DIFFICULTE, ALGO_OFFENSIF)

