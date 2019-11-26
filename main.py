import argparse
import chess


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
            # TODO mettre le code de l'IA ici
            #Pour l'instant c'est nous qui jouons
            # Ca serait bien d'avoir un retour console qui nous écrit le move que
            #vient de faire l'IA
            joueurJoue(board)

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


def printBoard(board):
    #Le board ici est une liste de caractères, on imprime ici les 8 rangés et on ajoute
    #les index pour faciliter la lecture
    print("    A B C D E F G H\n")
    for i in range(8):
        print(str(abs(i - 8)) + "   " + board[i * 16: i * 16 + 15] + "   " + str(abs(i - 8)))
    print("\n    A B C D E F G H")


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
