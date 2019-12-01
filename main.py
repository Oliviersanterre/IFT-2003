import argparse
import chess
import copy
import math
import random

#Les valeurs heuristiques peuvent être modifiées ici
PIECE_TYPES = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] = range(1, 7)
VALEUR_PIECES = {1:10, 2:40, 3:50, 4:80, 5:100, 6:math.inf}
VALEUR_CHECK = 5
VALEUR_CHECKMATE = math.inf
VALEUR_CASTLING = 0
VALEUR_PROMOTION = {1:0, 2:35, 3:45, 4:75, 5:95}


def tester(board, equipe, niveauDifficulte, algoType):

    #Les blancs commencent, si le joueur a choisi les noirs il ne commence pas
    tourJoueur = equipe == 'B'

    #condition d'arrêt de la boucle de jeu
    partieTerminee = False

    #Boucle de jeu
    while not partieTerminee:
        #printBoard(board.__str__())
        if tourJoueur:
            #La fonction joueurJoue retourne True si le joueur veut quitter
            partieTerminee = joueurJoue(board)
        else:
            partieTerminee = iaJoue(board, niveauDifficulte, algoType)
           

        #Si la partie est terminée, on sort de la boucle
        if (board.is_game_over()):
            if tourJoueur:
                print("La partie est terminée, vous avez gagné contre l'IA")
            else:
                print("La partie est terminée, vous avez perdu contre l'IA")
            partieTerminee = True

        #Changement de tour
        tourJoueur = not tourJoueur

def jouer(equipe, niveauDifficulte):
    #Initialisation du plateau
    board = chess.Board()

    #Les blancs commencent, si le joueur a choisi les noirs il ne commence pas
    tourJoueur = equipe == 'B'

    #Mot de bienvenue
    print("Bienvenue dans le jeu d'echec de l'Équipe 29!\n")
    print("Pour jouer, inscrivez le nom de la case à laquelle se trouve le pion que vous")
    print("voulez déplacer et la case à laquelle vous voulez le déplacer.")
    print("Par exemple, pour bouger le pion en B2 à la case B4, écrivez b2b4")

    #condition d'arrêt de la boucle de jeu
    partieTerminee = False

    #Boucle de jeu
    while not partieTerminee:
        printBoard(board.__str__())
        if tourJoueur:
            #La fonction joueurJoue retourne True si le joueur veut quitter
            partieTerminee = iaJoue(board, niveauDifficulte, 1)
        else:
            partieTerminee = iaJoue(board, 3, 2)

        #Si la partie est terminée, on sort de la boucle
        if (board.is_game_over()):
            if (board.is_insufficient_material()):
                print("Partie nulle")
            else:
                if tourJoueur:
                    print("La partie est terminée, vous avez gagné contre l'IA")
                else:
                    print("La partie est terminée, vous avez perdu contre l'IA")
            partieTerminee = True

        #Changement de tour
        tourJoueur = not tourJoueur


def joueurJoue(board):

    #index de la piece capturé par l'utilisateur (s'il y a lieu)
    player_captures_piece = 0;

    #On imprime le plateau
    printBoard(board.__str__())
    #On récupère le tour du joueur
    move = input("\nInscrivez votre coup ici (vous pouvez quitter en écrivant 'q') : ")
    #Si le joueur veut quitter l'application
    if (move == 'q'):
        return True
    #On crée une liste des moves légaux
    legal_moves = [element.__str__() for element in board.legal_moves]

    #Tant que le move du joueur n'est pas légal on redemande
    while (move not in legal_moves):
        print("Ce coup n'est pas légal")
        move = input("Inscrivez votre coup ici : ")
        if (move == 'q'):
            return True
    #On push le move
    move = chess.Move.from_uci(move)
    if (board.is_capture(move)):
        player_captures_piece = board.piece_at(move.to_square);
    board.push(move)

    if (player_captures_piece):
        print("L'IA a perdu la piece : " + (player_captures_piece.symbol()) + "\n")

    #Retourne false, comme quoi le joueur ne veut pas quitter
    return False

def iaJoue(board, niveauDeDifficulte, typeMinimax):

    #Index de la piece capturé par l'IA (s'il y a lieu)
    ia_captures_piece = 0;

    #On crée la racine de l'arbre des mouvements
    racine = Node(None, None, -math.inf, math.inf, 0)

    #On fait un parcour miniMax génératif de cet arbre en considérant l'état actuel du jeu
    copy_board = copy.deepcopy(board)
    miniMax(0, racine, True, niveauDeDifficulte, copy_board, typeMinimax)

    #On récupère le move choisi par l'IA
    move = racine.get_next_move()

    if (board.is_capture(move)):
        ia_captures_piece = board.piece_at(move.to_square);

    #On push le move
    board.push(move)

    print("L'IA a joué: {}".format(move) + "\n")

    if(ia_captures_piece):
        print("Vous avez perdu la piece : " + (ia_captures_piece.symbol()) + "\n")



    #Retourne false, comme quoi le joueur ne veut pas quitter
    return False


def printBoard(board):
    #Le board ici est une liste de caractères, on imprime ici les 8 rangés et on ajoute
    #les index pour faciliter la lecture
    print("    A B C D E F G H\n")
    for i in range(8):
        print(str(abs(i - 8)) + "   " + board[i * 16: i * 16 + 15] + "   " + str(abs(i - 8)))
    print("\n    A B C D E F G H")

    
def getHeuristicValueDefenseOriented(current_board:chess.Board, move:chess.Move) -> int:
    #Retourne la valeur heuristique d'un move sur un état de jeu donné

    value = 0
    current_board.pop()

    #gain de valeur s'il y a capture
    if(current_board.is_capture(move)):
        current_board.push(move)
        piece = current_board.piece_at(move.to_square)
        current_board.pop()
        piece_type = piece.piece_type
        value += VALEUR_PIECES[piece_type]

    #gain de valeur s'il y a castling
    if(current_board.is_castling(move)):
        value += VALEUR_CASTLING

    #gain de valeur s'il y a promotion
    if(move.promotion):
        current_board.push(move)
        piece = current_board.piece_at(move.to_square)
        current_board.pop()
        piece_type = piece.piece_type
        value += VALEUR_PROMOTION[piece_type]

    #parce que les fonctions qui suivent ne peuvent pas prendre un move en argument
    current_board.push(move)

    #gain de valeur s'il y a echec
    if(current_board.is_check()):
        value += VALEUR_CHECK

    #gain de valeur s'il y a echec et mat
    if(current_board.is_checkmate()):
        value = VALEUR_CHECKMATE

    return value
   

def getHeuristicValueAttackOriented(board:chess.Board, move:chess.Move) -> int:
    board.pop()
    square = move.from_square
    color = board.piece_at(square).color
    board.push(move)
    white_score = 0
    black_score = 0
    bonus_attaque = 3
    for i in range(0, 64):
        # s'il y a une pièce
        if board.piece_type_at(i) != None:
            # si la piece est noire
            if board.piece_at(i).color:
                # ajout du score pour les noirs
                if i < 32:
                    white_score += int(board.piece_type_at(i))
                else:
                    white_score += int(board.piece_type_at(i)) + bonus_attaque
            # sinon elle est blanche
            else:
                # ajout du score pour les blancs
                if i >= 32:
                    black_score += int(board.piece_type_at(i))
                else:
                    black_score += int(board.piece_type_at(i)) + bonus_attaque


    value = white_score - black_score

    if (move.promotion):
        piece = board.piece_at(move.to_square)
        piece_type = piece.piece_type
        value += VALEUR_PROMOTION[piece_type]

    if (board.is_check()):
        value += VALEUR_CHECK

    if (board.is_checkmate()):
        value = VALEUR_CHECKMATE

    return value

"Le premier appel recoit None, None, -inf, +inf, None"
class Node():
    #Classe qui construit un arbre des moves, et de leur valeur
    def __init__(self, move:chess.Move, value:int, alpha:int, beta:int, val_move:int):
        self.move = move
        self.val_move = val_move
        self.children = []
        self.value = value
        self.alpha = alpha
        self.beta = beta
    def add(self, child_move:chess.Move, child_value:int, child_alpha:int, child_beta:int, child_val_move:int):
        self.children.append(Node(child_move, child_value, child_alpha, child_beta, child_val_move))
    def get_next_move(self):
        best_moves = []
        print("Taille de la liste des moves possibles: " + str(len(self.children)) + "\n")
        for i in range(len(self.children)):
            #print(str(self.children[i].value) + "\n")
            if(self.children[i].value == self.value):
                best_moves.append(self.children[i].move)
                #print("Best moves: " + str(self.children[i].move) + "\n")
        return random.choice(best_moves)

def miniMax(current_depth:int, node:Node, is_max:bool,
            max_depth:int, current_board:chess.Board, heuristique_type:int) -> int:
    #Calcul minimax avec alpha-beta qui prend en entrée la profondeur actuelle, un
    #Node, la profondeur de recherche maximum et une copie de l'état de jeu
    
    if(current_depth == max_depth):
        if (heuristique_type == 1):
            if is_max:
                node.value = node.val_move - getHeuristicValueAttackOriented(current_board, node.move)
            else:
                node.value = node.val_move + getHeuristicValueAttackOriented(current_board, node.move)
            return 0
        else:
            if is_max:
                node.value = node.val_move - getHeuristicValueDefenseOriented(current_board, node.move)
            else:
                node.value = node.val_move + getHeuristicValueDefenseOriented(current_board, node.move)
            return 0
    
    if is_max:
        "tant que move generetor n'est pas vide, faire un move sur une copie"
        node.value = -math.inf
        if(node.move != None):
            if (heuristique_type == 1):
                node.val_move -= getHeuristicValueAttackOriented(current_board, node.move)
            else:
                node.val_move -= getHeuristicValueDefenseOriented(current_board, node.move)
        for move in current_board.legal_moves:
            node.add(move, None, node.alpha, node.beta, node.val_move)
            current_board.push(move)
            miniMax(current_depth+1, node.children[-1], False, max_depth, current_board, heuristique_type)
            current_board.pop()
            node.value = max(node.value, node.children[-1].value)
            node.alpha = max(node.alpha, node.value)
            
            if node.beta <= node.alpha:
                break
        
        return 1
    
    else:
        node.value = math.inf
        if(node.move != None):
            if (heuristique_type == 1):
                node.val_move += getHeuristicValueAttackOriented(current_board, node.move)
            else:
                node.val_move += getHeuristicValueDefenseOriented(current_board, node.move)
        
        "tant que move generetor n'est pas vide, faire un move sur une copie"
        for move in current_board.legal_moves:
            node.add(move, None, node.alpha, node.beta, node.val_move)
            current_board.push(move)
            miniMax(current_depth+1, node.children[-1], True, max_depth, current_board, heuristique_type)
            current_board.pop()
            node.value = min(node.value, node.children[-1].value)
            node.beta = min(node.beta, node.value)
            
            if node.beta <= node.alpha:
                break
        return 1
    
    
def main():
    #Instantiation du parser
    parser = argparse.ArgumentParser()
    #Premier argument correspond à la couleur que le joueur veut prendre
    #'B' pour blanc ou 'N' pour noir.
    parser.add_argument("equipe", help="L'equipe dans laquelle vous voulez joueur, B pour blanc, N pour noir",
                        type=str, choices=['B', 'N'])
    #Le second argument correspond au niveau de difficulté entre 1 et 5
    parser.add_argument("niveauDifficulte", help="Le niveau de difficulté de L'IA (entre 1 et 5)",
                        type=int, choices=range(1, 6))
    #Parsing des arguments, si ce n'est pas les formats voulu, le programme s'arrête ici
    args = parser.parse_args()

    #Début du jeu
    jouer(args.equipe, args.niveauDifficulte)


if __name__ == '__main__':
    main()
