import numpy as np
import random
import copy
import math
import time
import matplotlib.pyplot as plt
max = 200
n = 50

# -------------------------------- MATRICES D'ADJACENCE ------------------------------------------------

# -------------------------------- GENERATION DES FAMILLES DE GRAPHE ------------------------------------
def graphe_cyclique():
    """ PARTIE 1: Génération d'un graphe cyclique représenté par une matrice d'adjacence """
    G = np.zeros((n,n), dtype=int)
    E = []
    for i in range(n-1):
        G[i][i+1] = 1
        G[i+1][i] = 1
        E.append((i+1, i+2))
    G[n-1][0] = 1
    G[0][n-1] = 1
    E.append((1, n))
    return [G, n, E]

def graphe_complet():
    """ PARTIE 1: Génération d'un graphe complet représenté par une matrice d'adjacence """
    G = np.ones((n,n), dtype=int)
    E = []
    for i in range(n):
        G[i][i] = 0
    for i in range(n):
        for j in range(i+1, n):
            E.append((i+1, j+1))
    return [G, n, E]

def graphe_aleatoire():
    """ PARTIE 1: Génération d'un graphe aléatoire représenté par une matrice d'adjacence """
    G = np.zeros((n,n), dtype=int)
    E = []
    for i in range(n):
        for j in range(i+1, n):
            if(random.uniform(0,1)<0.5):
                G[i][j] = 1
                G[j][i] = 1
                E.append((i+1, j+1))
    return [G, n, E]

def graphe_biparti_complet():
    """ PARTIE 1: Génération d'un graphe biparti complet sous forme de matrice d'adjacence """
    G = np.zeros((n,n), dtype=int)
    E = []
    k = n//2
    for i in range(k):
        for j in range(k, n):
            G[i][j] = 1
            G[j][i] = 1
            E.append((i+1, j+1))
    return [G, n, E]

# -------------------------------- ALGORITHME DE KARGER ------------------------------------------------

""" g[0][i] = -x => i appartient à la contraction de x """
def contract(M, e):
    """PARTIE 1: Fonction de contraction de l'arete e dans le graphe M, sous forme d'une matrice d'adjacence """
    i, j = e
    while(M[0][i-1] < 0):               #mise à jour des indices
        i = -M[0][i-1]                  #si la première ligne de l'indice est négatif, on redirige au premier indice non négatif

    while(M[0][j-1] < 0):
        j = -M[0][j-1]

    if( i != j):
        if(i>j):
            temp = i
            i = j
            j = temp

        #addition des colonnes
        for k in range(n):
            M[k][i-1] = M[k][i-1] + M[k][j-1]
            if(M[i-1][k] >= 0):
                M[i-1][k] = M[k][i-1]
        
        M[0][j-1] = -i

    return i,j

#G = [M, n, E]
def karger(G):
    """ PARTIE 1: Algorithme de Karger sur un graphe représenté par une matrice d'adjacence """
    while(G[1] > 2):
        e = random.choice(G[2])
        i, j = contract(G[0], e)
        G[2].remove(e)
        if( i != j):
            G[1] = G[1] - 1
    v1 = [1]
    v2 = []
    for i in range(1, n):
        if(G[0][0][i] >= 0):
            v2.append(i+1)
        else:
            if((-G[0][0][i]) in v1):
                v1.append(i+1)
            else:
                v2.append(i+1)
    cardinal = G[0][v1[0]-1][v2[0]-1]
    return v1, cardinal


# -------------------------------- ALGORITHME DE KARGER ITERE ------------------------------------------------
def karger_itere(Gr, T):
    """ PARTIE 2: Algorithme de Karger sur un graphe représenté par une matrice d'adjacence, répété T fois """
    m = float('inf')
    S = []
    for i in range(T):
        G = copy.deepcopy(Gr)
        v1, cardinal = karger(G)
        if(cardinal < m):
            m = cardinal
            S = v1
    return S, m



# -------------------------------- ALGORITHME DE KARGER STEIN ------------------------------------------------
""" G(g, V, E)"""
def contraction_partielle(G, t):
    """ PARTIE 3: Contraction partielle d'une arete dans un graphe représenté par une matrice d'adjacence """
    while(G[1] > t):
        e = random.choice(G[2])
        i, j = contract(G[0], e)
        G[2].remove(e)
        if(i != j):
            G[1] = G[1] - 1
    return G

def karger_stein(G, T):
    """ PARTIE 3: Algorithme de Karger-Stein sur un graphe représenté par une matrice d'adjacence """
    if(G[1] <= 6):
        return karger_itere(G, T)
    else:
        t = (int) (1 + G[1] / math.sqrt(2))
        G1 = contraction_partielle(copy.deepcopy(G), t)
        S1, m1 = karger_stein(G1, T)

        G2 = contraction_partielle(copy.deepcopy(G), t)
        S2, m2 = karger_stein(G2, T)
        if(m1<m2):
            return S1, m1
        else:
            return S2, m2


# -------------------------------- GENERATION DES COURBES ------------------------------------------------
def graph(t):
    """ Permet de representer sur une courbe le temps d'execution par rapport au nombre d'instances """
    plt.plot([i for i in range(1, n+1, n//10)], t, "-o")
    plt.xlabel("Nombre d'instances")
    plt.ylabel('Temps')
    #plt.title("Evolution du temps de calcul de Karger en fonction du nombre d'instances")
    plt.title("Evolution du temps d'exécution de la contraction en fonction du nombre d'instances")
    plt.show()

def graphIter(p, T):
    """ Permet de représenter sur une courbe les probabilité de réussite en fonction de nombre de répétitions """
    plt.plot([i for i in range(1, T+1, T//10)], p, "-o")
    plt.xlabel("Nombre de répétitions")
    plt.ylabel("Probabilité de succès")
    plt.title("Evolution de la proba de succès de karger en fonction du nombre de répétitions")
    plt.show()

def courbe_contraction():
    t = []
    m = 10
    for i in range(max//10, max+1, max//10):      #boucle qui commence à max/10 et se termine à max, avec itération max/10 à chaque fois
        temp_t = 0
        global n
        n = i
        for j in range(0, m):
            G = graphe_aleatoire()
            E = G[2]
            e = random.choice(E)                # on choisit une arete aléatoire
            begin = time.time()                 #debut
            contract(G[0], e)              
            end = time.time() - begin           #fin
            temp_t = temp_t + end               #sommer le temps
        t.append(temp_t/m)                      #moyenne
    graph(t)

def courbe_karger():
    t = []
    m = 10
    for i in range(max//10, max+1, max//10):      #boucle qui commence à max/10 et se termine à max, avec itération max/10 à chaque fois
        temp_t = 0
        global n
        n = i
        for j in range(0, m):
            G = graphe_aleatoire()
            begin = time.time()                 #debut
            karger(G)              
            end = time.time() - begin           #fin
            temp_t = temp_t + end               #sommer le temps
        t.append(temp_t/m)                      #moyenne
    graph(t)

def courbe_karger_itere():
    probas = []
    m = 10
    for T in range(0, 100, 10):
        pMoy = 0
        for j in range(0, m):
            G = graphe_biparti_complet()
            S, cardinal = karger_itere(G, T)
            if cardinal == 24:                     #resultat qu'on est sensé obtenir avec un graphe cyclique
                pMoy+=1
        probas.append(pMoy/m)
    graphIter(probas, T)


def courbe_prob_succes_karger(s_karger, e_karger, s_karger_itere, e_karger_itere):
    width = 0.3
    y1 = [s_karger, e_karger]
    y2 = [s_karger_itere, e_karger_itere]
    x1 = range(len(y1)) # Position des barres de la catégorie 1
    x2 = [i + width for i in x1] # Position des barres de la cat 2    
    plt.title("Probabilite de karger sur un graphe complet à 50 sommet sur 100 itération")
    plt.xticks([r + width / 2 for r in range(len(y1))], ['Succes', 'Erreur'])
    plt.bar(x1, y1, width, color='c', label='karger')
    plt.bar(x2, y2, width, color='m', label='karger itéré T = 3')
    plt.legend()
    plt.show()

def prob_succes_karger():
    global n
    n = 50
    s_karger = 0
    s_karger_itere = 0
    e_karger = 0
    e_karger_itere = 0
    for i in range(100):
        G1 = graphe_complet()
        G2 = graphe_complet()
        v1, cardinal1 = karger(G1)
        v2, cardinal2 = karger_itere(G2, 3)
        if(cardinal1 == n-1):
            s_karger = s_karger + 1
        else:
            e_karger = e_karger + 1
        if(cardinal2 == n-1):
            s_karger_itere = s_karger_itere + 1
        else:
            e_karger_itere = e_karger_itere + 1
    courbe_prob_succes_karger(s_karger, e_karger, s_karger_itere, e_karger_itere)


def graph_kargerStein(t):
    """ Permet de representer sur une courbe la pprobabilité de succes par rapport au nombre d'instances """
    plt.plot([i for i in range(n*10, n-1, (-n))], t, "-o")
    plt.gca().invert_xaxis()
    plt.grid()
    plt.xlabel("Nombre d'instances")
    plt.ylabel('Probabilite')
    plt.title("Evolution de la probabilité de succès en fonction du nombre d'instances")
    plt.show()

def prob_succes_kargerStein():
    global n
    m = 10
    probas = []
    for i in range(max, (max//10)-1, -(max//10)): 
        n = i
        pMoy = 0
        for j in range(0, m):
            G = graphe_complet()
            S, cardinal = karger_stein(G, 1)
            if cardinal == n-1:                     #resultat qu'on est sensé obtenir avec un graphe biparti cyclique
                pMoy+=1
        probas.append(pMoy/m)
    graph_kargerStein(probas)


# -------------------------------- FONCTIONS DE TEST DES DIFFERENTES VERSIONS DE KARGER ------------------------------------------
def testKarger(s, G):
    print(s + ":")
    g = copy.deepcopy(G)
    begin = time.time()  
    s, cardinal = karger(g)
    end = time.time() - begin
    print("\tCardinal : ", cardinal)
    print("\tTemps d'execution : ", end)

def testKargerItere(s, G):
    print(s + ":")
    g = copy.deepcopy(G)
    begin = time.time()  
    s, cardinal = karger_itere(g, 3)
    end = time.time() - begin
    print("\tCardinal : \t\t", cardinal)
    print("\tTemps d'execution : ", end)

def testKargerStein(s, G):
    print(s + ":")
    g = copy.deepcopy(G)
    begin = time.time()  
    s, cardinal = karger_stein(g, 3)
    end = time.time() - begin
    print("\tCardinal : ", cardinal)
    print("\tTemps d'execution : ", end)


def testMatrices():
    """ Jeux de tests avec des graphes sous forme de matrices d'adjacence """
    G = graphe_cyclique()
    G1 = graphe_complet()
    G2 = graphe_aleatoire()
    G3 = graphe_biparti_complet()

    """ Test Karger """
    print("\n\n--------------------TEST KARGER SUR", n, "SOMMETS--------------------\n\n")
    testKarger("Cyclique", G)
    testKarger("Complet", G1)
    testKarger("Aleatoire", G2)
    testKarger("Biparti complet", G3)

    print("\n\n--------------------TEST KARGER ITERE SUR", n, "SOMMETS--------------------\n\n")
    testKargerItere("Cyclique", G)
    testKargerItere("Complet", G1)
    testKargerItere("Aleatoire", G2)
    testKargerItere("Biparti complet", G3)

    print("\n\n--------------------TEST KARGER STEIN SUR", n, "SOMMETS--------------------\n\n")
    testKargerStein("Cyclique", G)
    testKargerStein("Complet", G1)
    testKargerStein("Aleatoire", G2)
    testKargerStein("Biparti complet", G3)

testMatrices()

#prob_succes_kargerStein()
