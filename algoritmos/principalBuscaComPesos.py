from .BuscaP import busca   
import numpy as np
import random as rd           
#--------------------------------------------------------------------------
# IMPORTA DADOS DO ARQUIVO
#--------------------------------------------------------------------------
def Gerar_Problema_Grafo(arq):
    grafo = []
    nos = []
    with open(arq,"r") as f:
        for dados in f:
            dados = dados.strip()
            dados = dados.split(",")
            nos.append(dados[0])
            aux1 = []
            for i in range (1,len(dados),2):
                aux=[]
                aux.append(dados[i])
                aux.append(int(dados[i+1]))
                aux1.append(aux)
            grafo.append(aux1)
        
    return nos, grafo            
#-----------------------------------------------------------------------------
# GERA GRID ALEATÓRIO
#-----------------------------------------------------------------------------
def Gera_Problema_Grid_Ale(nx,ny,qtd):
    mapa = np.zeros((nx,ny),int)
    
    k = 0
    while k<qtd:
        i = rd.randrange(0,nx)
        j = rd.randrange(0,ny)
        if mapa[i][j]==0:
            mapa[i][j] = 9
            k+=1
    return mapa,nx,ny
#-----------------------------------------------------------------------------
# GERA O GRID DE ARQUIVO TEXTO
#-----------------------------------------------------------------------------
def Gera_Problema_Grid_Fixo(arquivo):
    file = open(arquivo)
    mapa = []
    for line in file:
        aux_str = line.strip("\n")
        aux_str = aux_str.split(",")
        aux_int = [int(x) for x in aux_str]
        mapa.append(aux_int)
    nx = len(mapa)
    ny = len(mapa[0])
    return mapa,nx,ny

#--------------------------------------------------------------------------
# MÓDULO PRINCIPAL
#--------------------------------------------------------------------------

# Execução - Grafo
nos, grafo = Gerar_Problema_Grafo("Romenia_Com_Pesos.txt")
inicio = "arad"
final  = ["bucareste","sibiu","mehadia","urziceni"]
inicio = inicio.upper()
for i in range(len(final)):
    final[i]  = final[i].upper()
"""
# Executa Grid
arquivo = "mapa1.txt"
#mapa,dx, dy = Gera_Problema_Grid_Ale(10,10,10)
mapa,dx, dy = Gera_Problema_Grid_Fixo(arquivo)

origem  = tuple(map(int, input("Digite a origem (x y): ").split()))
destino = tuple(map(int, input("Digite a destino (x y): ").split()))
"""
# Executa buscas
sol = busca()
caminho = []

#caminho, custo = sol.custo_uniforme(inicio,final,nos,grafo)
#caminho, custo = sol.custo_uniforme(origem,destino,mapa,dx,dy)
#print("\n===> Custo Uniforme")
#if caminho!=None:
#    print("Caminho: ",caminho)
#    print("Custo: ",custo)
#else:
#    print("Caminho não encontrado")

#caminho, custo = sol.greedy(inicio,final,nos,grafo)
#caminho, custo = sol.greedy(origem,destino,mapa,dx,dy)
#print("\n===> Greedy")
#if caminho!=None:
#    print("Caminho: ",caminho[::-1])
#    print("Custo: ",custo)
#else:
#    print("Caminho não encontrado")

#caminho, custo = sol.a_estrela(inicio,final,nos,grafo)
#caminho, custo = sol.a_estrela(origem,destino,mapa,dx,dy)
#print("\n===> A Estrela")
#if caminho!=None:
#    print("Caminho: ",caminho[::-1])
#    print("Custo: ",custo)
#else:
#    print("Caminho não encontrado")

#caminho, custo = sol.aia_estrela(inicio,final,nos,grafo)
#caminho, custo = sol.aia_estrela(origem,destino,mapa,dx,dy)
#print("\n===> AIA Estrela")
#if caminho!=None:
#    print("Caminho: ",caminho[::-1])
#    print("Custo: ",custo)
#else:
#    print("Caminho não encontrado")
caminho, custo = sol.a_estrela_multi(inicio,final,nos,grafo)
print("\n===> A Estrela")
if caminho!=None:
    print("Caminho: ",caminho[::-1])
    print("Custo: ",custo)
else:
    print("Caminho não encontrado")
