from collections import deque
from src.NodeP import NodeP
from math import sqrt, fabs
import heapq
import numpy as np
from numba import njit, uint32, uint8, typed, types, typeof

NULL = np.uint32(4294967295)
caminho_type = types.ListType(types.uint32)

#--------------------------------------------------------------------------    
# EXIBE O CAMINHO ENCONTRADO NA ÁRVORE DE BUSCA
#--------------------------------------------------------------------------    
@njit(caminho_type(uint32, uint32, uint32, uint32[::1]))
def exibir_caminho(custo, inicio, fim, pai):
    caminho = typed.List.empty_list(uint32)
    atual = fim
    while atual != inicio:
        caminho.append(atual)
        atual = pai[atual]
    caminho.append(inicio)
    caminho.append(custo)
    caminho.reverse()
    return caminho
# -----------------------------------------------------------------------------
# CUSTO UNIFORME - GRAFO
# -----------------------------------------------------------------------------
@njit(caminho_type(uint32, uint32, uint32[:, ::1], uint32[::1]))
def custo_uniforme_grafo(inicio,fim,grafo,pesos):
    if inicio == fim:
        caminho = typed.List.empty_list(uint32)
        caminho.append(inicio)
        return caminho
    
    lista = [(uint32(0), uint32(inicio))]

    visitado = np.full(len(grafo), NULL, dtype=np.uint32)

    pai = np.empty(len(grafo), dtype=np.uint32)

    while lista:
        tup = heapq.heappop(lista)
        valor = tup[0]
        atual = tup[1]

        if atual == fim:
            return exibir_caminho(valor, inicio, fim, pai)
        
        filhos = grafo[atual]
        for i in range(len(filhos)):
            novo = filhos[i]
            valor_novo = uint32(valor + pesos[i])

            if visitado[novo] != NULL and visitado[novo] <= valor_novo: continue

            heapq.heappush(lista, (valor_novo, novo))
            visitado[novo] = valor_novo
            pai[novo] = atual
    
    return typed.List.empty_list(uint32)
#--------------------------------------------------------------------------    
# EXIBE O CAMINHO ENCONTRADO NA ÁRVORE DE BUSCA
#--------------------------------------------------------------------------    
def exibir_caminho_node(node):
    caminho = []
    while node is not None:
        caminho.append(node.estado)
        node = node.pai
    caminho.reverse()
    return caminho
# -----------------------------------------------------------------------------
# GREEDY - GRAFO
# -----------------------------------------------------------------------------
def greedy_grafo(inicio,fim,grafo,pesos,heuristica):
    # Origem igual a destino
    if inicio == fim:
        return [inicio], 0
    
    # Fila de prioridade baseada em deque + inserção ordenada
    lista = list()
    raiz = NodeP(None, inicio, 0, None, None, 0)
    lista.append(raiz)

    # Controle de nós visitados
    visitado = {inicio: raiz}
    
    # loop de busca
    while lista:
        # remove o primeiro nó
        atual = heapq.heappop(lista)
        valor_atual = atual.v2

        # Chegou ao objetivo
        if atual.estado == fim:
            return exibir_caminho_node(atual), atual.v2

        # Gera sucessores
        ind = atual.estado
        filhos = grafo[ind]

        for i, novo in enumerate(filhos):
            # custo acumulado até o sucessor
            v2 = valor_atual + pesos[i]
            v1 = int(heuristica[novo])

            # Não visitado ou custo melhor
            if (novo not in visitado) or (v2 < visitado[novo].v2):
                filho = NodeP(atual, novo, v1, None, None, v2)
                visitado[novo] = filho
                heapq.heappush(lista, filho)

    return [], -1
# -----------------------------------------------------------------------------
# A ESTRELA - GRAFO
# -----------------------------------------------------------------------------
def a_estrela_grafo(inicio,fim,grafo,pesos,heuristica):
    # Origem igual a destino
    if inicio == fim:
        return [inicio], 0
    
    # Fila de prioridade baseada em deque + inserção ordenada
    lista = list()
    raiz = NodeP(None, inicio, 0, None, None, 0)
    lista.append(raiz)

    # Controle de nós visitados
    visitado = {inicio: raiz}
    
    # loop de busca
    while lista:
        # remove o primeiro nó
        atual = heapq.heappop(lista)
        valor_atual = atual.v2

        # Chegou ao objetivo
        if atual.estado == fim:
            return exibir_caminho_node(atual), atual.v2

        # Gera sucessores
        filhos = grafo[atual.estado]

        for i, novo in enumerate(filhos):
            # custo acumulado até o sucessor
            v2 = valor_atual + pesos[i]
            v1 = v2 + int(heuristica[novo])

            # Não visitado ou custo melhor
            if (novo not in visitado) or (v2 < visitado[novo].v2):
                filho = NodeP(atual, novo, v1, None, None, v2)
                visitado[novo] = filho
                heapq.heappush(lista, filho)

    return [], -1
# -----------------------------------------------------------------------------
# AIA ESTRELA - GRAFO
# -----------------------------------------------------------------------------
def aia_estrela_grafo(inicio,fim,grafo,pesos,heuristica):
    lim = int(heuristica[inicio])
    # Origem igual a destino
    if inicio == fim:
        return [inicio], 0
    
    while True:
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = list()
        raiz = NodeP(None, inicio, 0, None, None, 0)
        lista.append(raiz)
    
        # Controle de nós visitados
        visitado = {inicio: raiz}
        
        # loop de busca
        novo_lim = []
        while lista:
            # remove o primeiro nó
            atual = heapq.heappop(lista)
            valor_atual = atual.v2
    
            # Chegou ao objetivo
            if atual.estado == fim:
                return exibir_caminho_node(atual), atual.v2
    
            # Gera sucessores
            filhos = grafo[atual.estado]
    
            for i, novo in enumerate(filhos):
                # custo acumulado até o sucessor
                v2 = valor_atual + pesos[i]
                v1 = v2 + int(heuristica[novo])
                
                if v1<=lim:
                    # Não visitado ou custo melhor
                    if (novo not in visitado) or (v2 < visitado[novo].v2):
                        filho = NodeP(atual, novo, v1, None, None, v2)
                        visitado[novo] = filho
                        heapq.heappush(lista, filho)
                else:
                    novo_lim.append(int(v1))
        lim = (int)(sum(novo_lim)/(len(novo_lim)))
        lista.clear()
        visitado.clear()
        novo_lim.clear()
        
    return [], -1
