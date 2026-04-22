from collections import deque
from src.Node import Node
import numpy as np
from numba import njit, uint32, int32, typed, types

caminho_type = types.ListType(types.uint32)

#--------------------------------------------------------------------------    
# EXIBE O CAMINHO ENCONTRADO NA ÁRVORE DE BUSCA
#--------------------------------------------------------------------------  
@njit(caminho_type(uint32, uint32, uint32[::1]))
def exibir_caminho(inicio,fim,pai):
    atual = fim
    caminho = typed.List.empty_list(types.uint32)
    while atual != inicio:
        caminho.append(atual)
        atual = pai[atual]
    caminho.append(atual)
    caminho.reverse()
    return caminho
#--------------------------------------------------------------------------    
# EXIBE O CAMINHO ENCONTRADO NA ÁRVORE DE BUSCA - BIDIRECIONAL
#--------------------------------------------------------------------------
@njit(caminho_type(uint32, uint32, uint32, uint32[::1], uint32[::1]))
def exibir_caminho_bid(inicio,encontro,fim,pai1,pai2):
    caminho = typed.List.empty_list(uint32)
    # bid 1
    atual = encontro
    while atual != inicio:
        caminho.append(atual)
        atual = pai1[atual]
    caminho.append(atual)
    caminho.reverse()

    # bid 2
    atual = encontro
    while atual != fim:
        atual = pai2[atual]
        caminho.append(atual)
    
    return caminho
#--------------------------------------------------------------------------
# BUSCA EM AMPLITUDE - GRAFO
#--------------------------------------------------------------------------
@njit(caminho_type(uint32, uint32, uint32[:, ::1]))
def amplitude_grafo(inicio,fim,grafo):
    if inicio == fim:
        caminho = typed.List.empty_list(types.uint32)
        caminho.append(inicio)
        return caminho
    
    fila = np.empty(len(grafo), dtype=np.uint32)
    fila[0] = inicio
    head = 0
    tail = 1

    pai = np.empty(len(grafo), dtype=np.uint32)

    # 255 == False, qualquer outro == True
    visitado = np.full(len(grafo), 255, dtype=np.uint8)
    visitado[inicio] = 0

    while head < tail:
        atual = fila[head]
        filhos = grafo[atual]

        for novo in filhos:
            # verifica se foi visitado
            if visitado[novo] != 255: continue
            # marca como visitado (com valor = v1)
            visitado[novo] = visitado[atual] + 1
            # adiciona à fila
            fila[tail] = novo
            tail += 1
            # guarda o pai de "novo"
            pai[novo] = atual
            # verifica se é o objetivo
            if novo == fim:
                return exibir_caminho(inicio,fim,pai)
        
        head += 1
    
    return typed.List.empty_list(uint32)
#--------------------------------------------------------------------------
# BUSCA EM PROFUNDIDADE - GRAFO
#--------------------------------------------------------------------------
@njit(caminho_type(uint32, uint32, uint32[:, ::1]))
def profundidade_grafo(inicio, fim, grafo):
    if inicio == fim:
        caminho = typed.List.empty_list(types.uint32)
        caminho.append(inicio)
        return caminho
    
    pilha = np.empty(len(grafo), dtype=np.uint32)
    pilha[0] = inicio
    top = 0

    pai = np.empty(len(grafo), dtype=np.uint32)

    # 255 == False, qualquer outro == True
    visitado = np.full(len(grafo), 255, dtype=np.uint8)
    visitado[inicio] = 0

    while top >= 0:
        # retira da pilha
        atual = pilha[top]
        top -= 1
        filhos = grafo[atual]

        for novo in filhos:
            # verifica se foi visitado
            if visitado[novo] != 255: continue
            # marca como visitado (com valor = 1)
            visitado[novo] = 1
            # adiciona à pilha
            top += 1
            pilha[top] = novo
            # guarda o pai de "novo"
            pai[novo] = atual
            # verifica se é o objetivo
            if novo == fim:
                return exibir_caminho(inicio,fim,pai)

    return typed.List.empty_list(uint32)
#--------------------------------------------------------------------------
# BUSCA EM PROFUNDIDADE LIMITADA - GRAFO
#--------------------------------------------------------------------------
@njit(caminho_type(uint32, uint32, uint32[:, ::1], int32))
def prof_limitada_grafo(inicio,fim,grafo,lim):
    if inicio == fim:
        caminho = typed.List.empty_list(types.uint32)
        caminho.append(inicio)
        return caminho
    
    pilha = np.empty(len(grafo), dtype=np.uint32)
    pilha[0] = inicio
    top = 0

    pai = np.empty(len(grafo), dtype=np.uint32)

    visitado = np.full(len(grafo), -1, dtype=np.int32)
    visitado[inicio] = 0

    while top >= 0:
        # retira da pilha
        atual = pilha[top]
        top -= 1
        filhos = grafo[atual]

        if visitado[atual] >= lim: continue

        for novo in filhos:
            # verifica se foi visitado
            if visitado[novo] != -1 and visitado[novo] <= visitado[atual] + 1: continue
            # marca como visitado (com valor = v1)
            visitado[novo] = visitado[atual] + 1
            # adiciona à pilha
            top += 1
            pilha[top] = novo
            # guarda o pai de "novo"
            pai[novo] = atual
            # verifica se é o objetivo
            if novo == fim:
                return exibir_caminho(inicio,fim,pai)

    return typed.List.empty_list(uint32)
#--------------------------------------------------------------------------
# BUSCA EM APROFUNDAMENTO ITERATIVO - GRAFO
#--------------------------------------------------------------------------
@njit(caminho_type(uint32, uint32, uint32[:, ::1], int32))
def aprof_iterativo_grafo(inicio,fim,grafo,lim_max):
    if inicio == fim:
        caminho = typed.List.empty_list(types.uint32)
        caminho.append(inicio)
        return caminho
    
    for lim in range(1, lim_max + 1):
        pilha = np.empty(len(grafo), dtype=np.uint32)
        pilha[0] = inicio
        top = 0

        pai = np.empty(len(grafo), dtype=np.uint32)

        visitado = np.full(len(grafo), -1, dtype=np.int32)
        visitado[inicio] = 0

        while top >= 0:
            # retira da pilha
            atual = pilha[top]
            top -= 1
            filhos = grafo[atual]

            if visitado[atual] >= lim: continue

            for novo in filhos:
                # verifica se foi visitado
                if visitado[novo] != -1 and visitado[novo] <= visitado[atual] + 1: continue
                # marca como visitado (com valor = v1)
                visitado[novo] = visitado[atual] + 1
                # adiciona à pilha
                top += 1
                pilha[top] = novo
                # guarda o pai de "novo"
                pai[novo] = atual
                # verifica se é o objetivo
                if novo == fim:
                    return exibir_caminho(inicio,fim,pai)

    return typed.List.empty_list(uint32)
#--------------------------------------------------------------------------
# BUSCA BIDIRECIONAL - GRAFO
#--------------------------------------------------------------------------
def bidirecional_grafo(inicio,fim,grafo):
    if inicio == fim:
        caminho = typed.List.empty_list(uint32)
        caminho.append(inicio)
        return caminho
    
    fila1 = np.empty(len(grafo), dtype=np.uint32)
    fila1[0] = inicio
    head1 = 0
    tail1 = 1
    pai1 = np.empty(len(grafo), dtype=np.uint32)

    fila2 = np.empty(len(grafo), dtype=np.uint32)
    fila2[0] = fim
    head2 = 0
    tail2 = 1
    pai2 = np.empty(len(grafo), dtype=np.uint32)

    # 255 == False, qualquer outro == True
    visitado1 = np.full(len(grafo), 255, dtype=np.uint8)
    visitado1[inicio] = 0

    visitado2 = np.full(len(grafo), 255, dtype=np.uint8)
    visitado2[fim] = 0

    while head1 < tail1 and head2 < tail2:
        for _ in range(head1, tail1):
            atual1 = fila1[head1]
            filhos1 = grafo[atual1]

            for novo in filhos1:
                # verifica se foi visitado
                if visitado1[novo] != 255: continue
                # marca como visitado (com valor = v1)
                visitado1[novo] = visitado1[atual1] + 1
                # adiciona à fila
                fila1[tail1] = novo
                tail1 += 1
                # guarda o pai de "novo"
                pai1[novo] = atual1
                # verifica se é o objetivo
                if visitado2[novo] != 255:
                    return exibir_caminho_bid(inicio,novo,fim,pai1,pai2)
            head1 += 1

        for _ in range(head2, tail2):
            atual2 = fila2[head2]
            filhos2 = grafo[atual2]

            for novo in filhos2:

                if visitado2[novo] != 255: continue

                visitado2[novo] = visitado2[atual2] + 1

                fila2[tail2] = novo
                tail2 += 1

                pai2[novo] = atual2

                if visitado1[novo] != 255:
                    return exibir_caminho_bid(inicio,novo,fim,pai1,pai2)
            head2 += 1
    
    return typed.List.empty_list(uint32)
