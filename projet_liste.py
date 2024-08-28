import random
import time
import matplotlib.pyplot as plt
n = 30
max = 500

# --------------------------------- LISTES D'ADJACENCE ------------------------------------------------

# -------------------------------- GENERATION DES FAMILLES DE GRAPHE -----------------------------------
def liste_adj_test():
    L = []
    E = [(1,2), (1,4), (2,3), (2,4), (3,5), (4,5)]
    for k in range(n):
        lk = []
        for e in range(len(E)):
            i, j = E[e]
            if i == k+1:
                lk.append(j)
            if j == k+1:
                lk.append(i)
        L.append(lk)
    return [L, E]

def liste_graphe_cyclique():
    """ PARTIE 1: Génération d'un graphe cyclique représenté par des listes d'adjacence """
    L = [[2, n]]
    E = [(1,2), (1,n)]
    for k in range(2, n):
        lk = []
        lk.append(k-1)
        lk.append(k+1)
        E.append((k, k+1))
        L.append(lk)
    L.append([1, n-1])
    return [L, E]

def liste_graphe_complet():
    """ PARTIE 1: Génération d'un graphe complet représenté par des listes d'adjacence """
    L = []
    E = []
    for k in range(1, n+1):
        lk = []
        for i in range (k, n+1):
            if(k != i):
                lk.append(i)
                E.append((k, i))
        L.append(lk)
    return [L, E]

def liste_graphe_biparti():
    """ PARTIE 1: Génération d'un graphe biparti complet représenté par des listes d'adjacence """
    L = [[] for _ in range(n)]
    E = []
    k = n//2
    for i in range(k):
        for j in range(k, n):
            L[i].append(j+1)    
            L[j].append(i+1)
            E.append((i+1, j+1))
    return [L, E]

def liste_graphe_aleatoire():
    """ PARTIE 1: Génération d'un graphe aléatoire représenté par des listes d'adjacence """
    L = [[] for _ in range(n)]
    E = []
    for i in range(n):
        for j in range(i+1, n):
            if(random.uniform(0,1)<0.5):
                L[i].append(j+1)    
                L[j].append(i+1)
                E.append((i+1, j+1))
    return [L, E]


# -------------------------------- ALGORITHME DE KARGER -----------------------------------

# contracter une arête (I, J) avec les listes d'adjacence 
# => L[I] = [], L[J] = []
def contractListe(L, e):
    """ PARTIE 1: Contraction d'une arete e dans le graphe G représenté par des listes d'adjacence L """
    i, j = e
    L[i-1] = L[i-1]+L[j-1] # on met les sommets adjacents de j dans i avec i<j
    L[j-1] = [] # on vide la liste d'adjacence du sommet j
    L[i-1] = [x for x in L[i-1] if x != i]
    for l in L:
        if L.index(l) != i-1:
            for k in range(len(l)):
                if l[k] == j:
                    l[k] = i

# parametre G = [L, E] avec L = listes d'adjacence, E = aretes
def kargerListe(G): 
    """ PARTIE 1: Algorithme de Karger sur un graphe représenté par une liste d'adjacence """
    z = len([x for x in G[0] if x != []])
    E = G[1].copy()
    while(z > 2):
        e = random.choice(E)
        i, j = sorted(e)
        contractListe(G[0], (i,j))
        for k in range(len(E)):
            x, y = E[k]
            if x == j:
                x = i
            if y == j:
                y = i
            E[k] = x, y # on remplace les aretes impliquant le sommet j par des aretes impliquant le sommet i

        E = [(x, y) for (x, y) in E if x!= y] # on enleve les aretes reflexives        
        z = len([x for x in G[0] if x != []])

    ind = []
    for l in G[0]:
        if l:
            ind.append(G[0].index(l))
    if ind[0]+1 in G[0][ind[1]]:
        G[0][ind[1]] = [x for x in G[0][ind[1]] if x != ind[0]+1]
    if ind[1]+1 in G[0][ind[0]]:
        G[0][ind[0]] = [x for x in G[0][ind[0]] if x != ind[1]+1]
    
    v1 = set([ind[0]+1]+G[0][ind[0]])
    v2 = set([ind[1]+1]+G[0][ind[1]])
    return v1, len(E)


def graph(t):
    """ Permet de representer sur une courbe le temps d'execution par rapport au nombre d'instances """
    plt.plot([i for i in range(1, n+1, n//10)], t, "-o")
    plt.xlabel("Nombre d'instances")
    plt.ylabel('Temps')
    plt.title("Evolution du temps de calcul de Karger en fonction du nombre d'instances")
    #plt.title("Evolution du temps d'exécution de la contraction en fonction du nombre d'instances")
    plt.show()

def courbe_contraction():
    t = []
    m = 10
    for i in range(max//10, max+1, max//10):      #boucle qui commence à max/10 et se termine à max, avec itération max/10 à chaque fois
        temp_t = 0
        global n
        n = i
        for j in range(0, m):
            G = liste_graphe_aleatoire()
            E = G[1]
            e = random.choice(E)                # on choisit une arete aléatoire
            begin = time.time()                 #debut
            contractListe(G[0], e)              
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
            G = liste_graphe_aleatoire()
            begin = time.time()                 #debut
            kargerListe(G)              
            end = time.time() - begin           #fin
            temp_t = temp_t + end               #sommer le temps
        t.append(temp_t/m)                      #moyenne
    graph(t)


def testListes():
    """ Jeux de tests avec des graphes sous forme de listes d'adjacence """
    Gcycle = liste_graphe_cyclique()
    Gcomp = liste_graphe_complet()
    Galea = liste_graphe_aleatoire()
    Gbipar = liste_graphe_biparti()

    print("\n\n---------------- GRAPHE CYCLIQUE ----------------\n\n")
    v, m = kargerListe(Gcycle)
    print(m)
    print("\n\n---------------- GRAPHE COMPLET ----------------\n\n")
    v, m = kargerListe(Gcomp)
    print(m)
    print("\n\n---------------- GRAPHE ALEATOIRE ----------------\n\n")
    v, m = kargerListe(Galea)
    print(m)
    print("\n\n---------------- GRAPHE BIPARTI COMPLET ----------------\n\n")
    v, m = kargerListe(Gbipar)
    print(m)

testListes()