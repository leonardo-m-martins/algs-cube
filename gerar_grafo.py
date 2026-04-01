from cube import gerar_grafo, initial_state
import numpy as np

def salvar_binario_numpy(estados, adjacencias, prefix="grafo"):
    np.save(f"{prefix}_estados.npy", estados)
    np.save(f"{prefix}_adjacencias.npy", adjacencias)


# Chame sua função aqui
estados, adjacencias = gerar_grafo(initial_state)
salvar_binario_numpy(estados, adjacencias)