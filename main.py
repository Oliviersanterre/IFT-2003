import argparse
import chess
import copy
import math

#Les valeurs heuristiques peuvent être modifiées ici
PIECE_TYPES = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] = range(1, 7)
VALEUR_PIECES = {1:10, 2:40, 3:50, 4:80, 5:100, 6:math.inf}
VALEUR_CHECK = 50
VALEUR_CHECKMATE = math.inf
VALEUR_CASTLING = 0


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
        if tourJoueur:
            #La fonction joueurJoue retourne True si le joueur veut quitter
            partieTerminee = joueurJoue(board)
        else:
            partieTerminee = iaJoue(board, niveauDifficulte)
            # TODO mettre le code de l'IA ici
            #Pour l'instant c'est nous qui jouons
            # Ca serait bien d'avoir un retour console qui nous écrit le move que
            #vient de faire l'IA

        #Si la partie est terminée, on sort de la boucle
        if (board.is_game_over()):
            partieTerminee = True

        #Changement de tour
        tourJoueur = not tourJoueur


def joueurJoue(board):

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

    #On push le move
    move = chess.Move.from_uci(move)
    board.push(move)

    #Retourne false, comme quoi le joueur ne veut pas quitter
    return False

def iaJoue(board, niveauDeDifficulte):

    #On crée la racine de l'arbre des mouvements
    racine = Node(None, None, -math.inf, math.inf)
    #On fait un parcour miniMax génératif de cet arbre en considérant l'état actuel du jeu
    racine.value = miniMax(0, racine, True, niveauDeDifficulte, board)
    #On récupère le move choisi par l'IA
    move = racine.get_next_move()
    #On push le move
    board.push(move)

    #Retourne false, comme quoi le joueur ne veut pas quitter
    return False


def printBoard(board):
    #Le board ici est une liste de caractères, on imprime ici les 8 rangés et on ajoute
    #les index pour faciliter la lecture
    print("    A B C D E F G H\n")
    for i in range(8):
        print(str(abs(i - 8)) + "   " + board[i * 16: i * 16 + 15] + "   " + str(abs(i - 8)))
    print("\n    A B C D E F G H")

    
def getHeuristicValue(current_board:chess.Board, move:chess.Move) -> int:
    #Retourne la valeur heuristique d'un move sur un état de jeu donné
    value = 0
    if(current_board.is_capture(move)):
        piece = current_board.piece_at(move.to_square)
        piece_type = piece.piece_type
        value += VALEUR_PIECES[piece_type]
    if(current_board.is_check(move)):
        value += VALEUR_CHECK
    if(current_board.is_checkmate(move)):
        value = VALEUR_CHECKMATE
    if(current_board.is_castling(move)):
        value += VALEUR_CASTLING
    return value

"Le premier appel recoit None, None, -inf, +inf"
class Node():
    #Classe qui construit un arbre des moves, et de leur valeur
    def __init__(self, move:chess.Move, value:int, alpha:int, beta:int):
        self.move = move
        self.children = []
        self.value = value
        self.alpha = alpha
        self.beta = beta
    def add(self, child_move:chess.Move, child_value:int, child_alpha:int, child_beta:int):
        self.children.append(Node(child_move, child_value, child_alpha, child_beta))
    def get_next_move(self):
        best = self.value
        for i in range(len(self.children)):
            if(self.children[i].value == self.value):
                best_move = self.children[i].move
                break
        return best_move

def miniMax(current_depth:int, node:Node, is_max:bool,
            max_depth:int, current_board:chess.Board) -> int:
    #Calcul minimax avec alpha-beta qui prend en entrée la profondeur actuelle, un
    #Node, la profondeur de recherche maximum et une copie de l'état de jeu
    if(current_depth == max_depth):
        return getHeuristicValue(current_board, node.move)
    
    copy_board = copy.deepcopy(current_board)
    if is_max:
        arbre.value = -math.inf
        
        "tant que move generetor n'est pas vide, faire un move sur une copie"
        for move in current_board.legal_moves:
            node.add(move, None, node.alpha, node.beta)
            node.children[-1].value = miniMax(current_depth+1, node.children[-1], False,
                              max_depth, copy_board)
            node.value = max(node.value, node.children[-1].value)
            node.alpha = max(node.alpha, node.value)
            
            if node.beta <= node.alpha:
                break
        
        return node.value
    
    else:
        node.value = math.inf
        
        "tant que move generetor n'est pas vide, faire un move sur une copie"
        for move in current_board.legal_moves:
            node.add(move, None, node.alpha, node.beta)
            node.children[-1].value = miniMax(current_depth+1, node.children[-1], True,
                              max_depth, copy_board)
            node.value = min(node.value, node.children[-1].value)
            node.beta = min(node.beta, node.value)
            
            if node.beta <= node.alpha:
                break
        return node.value
    
    
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
