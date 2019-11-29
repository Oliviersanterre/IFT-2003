import chess
import main

PIECE = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] = range(1, 7)
WHITE = 1
BLACK = 0
NIVEAU_DIFFICULTE = 2

# On cree le board de jeu
board = chess.Board()

#on retire les pieces de sur le jeu
board.clear_board()

#on cree des pieces qui ne sont pas encore sur le jeu
pion_w = chess.Piece(1,WHITE)
cheval_w = chess.Piece(2,WHITE)
fou_w = chess.Piece(3,WHITE)
tour_w = chess.Piece(4,WHITE)
reine_w = chess.Piece(5,WHITE)
roi_w = chess.Piece(6,WHITE)

pion_b = chess.Piece(1,BLACK)
cheval_b = chess.Piece(2,BLACK)
fou_b = chess.Piece(3,BLACK)
tour_b = chess.Piece(4,BLACK)
reine_b = chess.Piece(5,BLACK)
roi_b = chess.Piece(6,BLACK)

#on met certaines piece sur le jeu pour creer une situation (de test) precise
#pieces noirs
board.set_piece_at(40, pion_w, False)
board.set_piece_at(34, pion_w, False)

#pieces blanches
board.set_piece_at(51, reine_b, False)


#on ajoute les rois pour que la game soit dans un etat "normal"
board.set_piece_at(7, roi_w, False)
board.set_piece_at(23, roi_b, False)

#Permet de voir le board avant que l'IA fasse son tour
main.printBoard(board.__str__())

#on debute le jeu
main.tester(board, 'N', NIVEAU_DIFFICULTE)

