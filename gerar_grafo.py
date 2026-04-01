from cube import gerar_grafo_mapeado, initial_state
# import cProfile
# import pstats
import numpy as np

def salvar_binario_numpy(lista_estados, adjacencias, prefix="grafo"):
    # Salva estados como uma matriz única (N, 16)
    estados_array = np.frombuffer(b''.join(lista_estados), dtype=np.uint8).reshape(-1, 16)
    np.save(f"{prefix}_estados.npy", estados_array)

    # Como adjacencias é uma lista de listas (irregular), o melhor é "achatar"
    # e salvar os offsets (onde começa cada lista de vizinhos)
    flattened_adj = []
    offsets = [0]
    for v in adjacencias:
        flattened_adj.extend(v)
        offsets.append(len(flattened_adj))
    
    np.save(f"{prefix}_adj_data.npy", np.array(flattened_adj, dtype=np.uint32))
    np.save(f"{prefix}_adj_offsets.npy", np.array(offsets, dtype=np.uint32))

# profiler = cProfile.Profile()
# profiler.enable()

# Chame sua função aqui
lista_estados, adjacencias = gerar_grafo_mapeado(initial_state)
salvar_binario_numpy(lista_estados, adjacencias)

# profiler.disable()
# stats = pstats.Stats(profiler).sort_stats('tottime')
# stats.print_stats(20) # Mostra as 20 funções mais lentas