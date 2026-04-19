import tkinter as tk
from tkinter import ttk
from src.stickers import StickersCube, Subcubes, Colors, OFFSETS
from src.cube import Cube, get_state_lup, grafo, nos
from src.BuscaNP import buscaNP
import numpy as np

# Cores padrão do Cubo Mágico
COLORS = {Colors.WHITE: 'white', Colors.RED: 'red', Colors.BLUE: 'blue', Colors.ORANGE: 'orange', Colors.GREEN: 'green', Colors.YELLOW: 'yellow'}
COLORS_REVERSED_MAP = {value: key for key, value in COLORS.items()}

busca = buscaNP()

def stringify_path(path: list) -> str:
    MOVE_NAMES = ['U', 'U2', 'U\'', 'R', 'R2', 'R\'', 'F', 'F2', 'F\'']
    moves = []
    for i in range(len(path) - 1):
        move_idx = np.where(grafo[path[i]] == path[i+1])[0][0]
        moves.append(MOVE_NAMES[move_idx])
    return ' '.join(moves)


def apply_algorithm(algo: str, initial, objective):
    algos = ('Amplitude', 'Profundidade', 'Profundidade Limitada', 
             'Aprofundamento Iterativo', 'Bidirecional', 'Custo Uniforme', 
             'Greedy', 'A*', 'IDA* (AIA)')
    if algo == algos[0]:
        return busca.amplitude_grafo(initial, objective, nos=nos, grafo=grafo)
    if algo == algos[1]:
        return busca.profundidade_grafo(initial, objective, nos, grafo)
    if algo == algos[2]:
        return busca.prof_limitada_grafo(initial, objective, nos, grafo, 14)
    if algo == algos[3]:
        return busca.aprof_iterativo_grafo(initial, objective, nos, grafo, 14)
    if algo == algos[4]:
        return busca.bidirecional_grafo(initial, objective, nos, grafo)
    else: 
        raise Exception("Não implementado")

std_font = ("Arial", 10, "bold")

class CubeNet(tk.Canvas):
    """Componente gráfico que desenha a planificação de um cubo 2x2x2."""
    def __init__(self, master, sticker_size=30, editable=True, cube: StickersCube=None, scramble: bool=False, **kwargs):
        super().__init__(master, width=sticker_size*8, height=sticker_size*6, bg='#f0f0f0', highlightthickness=0, **kwargs)
        self.size = sticker_size
        self.editable = editable
        self.stickers = {} # Armazena os IDs dos retângulos
        if cube:
            self.cube = cube
        else:
            self.cube = StickersCube()

        if scramble:
            self.cube.scramble()
        
        self.draw_net()
        if self.editable:
            self.bind("<Button-1>", self.on_click)

    def draw_net(self):
        for i, OFFSET in enumerate(OFFSETS):
            for key in self.cube.state.keys():
                if key not in OFFSET: continue

                x1, y1 = OFFSET[key]
                x1 *= self.size
                y1 *= self.size
                x2 = x1 + self.size
                y2 = y1 + self.size

                color_idx = self.cube.state[key][i % 3]
                color = COLORS[color_idx]

                rect_id = self.create_rectangle(x1, y1, x2, y2, fill=color, outline='black', width=2)
                self.stickers[rect_id] = (key, i % 3)
            

    def on_click(self):
        item = self.find_withtag("current")
        if item:
            rect_id = item[0]
            current_color = self.itemcget(rect_id, "fill")
            next_color_idx = (COLORS_REVERSED_MAP[current_color] + 1) % len(COLORS)
            next_color = COLORS[next_color_idx]
            self.itemconfig(rect_id, fill=next_color)
            key, idx = self.stickers[rect_id]
            self.cube.state[key][idx] = next_color_idx

class RubiksSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cubo Mágico 2x2x2 - Buscas em IA")
        self.root.geometry("850x650")
        
        self.setup_ui()
        
        # Variáveis para controle da visualização da solução
        self.solution_path = []
        self.current_step = 0

    def setup_ui(self):
        # --- PAINEL DE CONTROLE (Topo) ---
        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack(fill=tk.X)

        tk.Label(control_frame, text="Método de Busca:", font=std_font).pack(side=tk.LEFT, padx=10)
        
        self.algo_var = tk.StringVar()
        algos = ['Amplitude', 'Profundidade', 'Profundidade Limitada', 
                 'Aprofundamento Iterativo', 'Bidirecional', 'Custo Uniforme', 
                 'Greedy', 'A*', 'IDA* (AIA)']
        self.algo_combo = ttk.Combobox(control_frame, textvariable=self.algo_var, values=algos, state="readonly", width=25)
        self.algo_combo.current(0)
        self.algo_combo.pack(side=tk.LEFT, padx=10)

        self.btn_solve = tk.Button(control_frame, text="Resolver Cubo", bg="#4CAF50", fg="white", font=std_font, command=self.solve)
        self.btn_solve.pack(side=tk.LEFT, padx=20)

        # --- PAINEL DE ESTADOS (Meio) ---
        states_frame = tk.Frame(self.root)
        states_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Estado Inicial
        frame_initial = tk.Frame(states_frame)
        frame_initial.pack(side=tk.LEFT, expand=True)
        tk.Label(frame_initial, text="Estado Inicial (Clique para alterar)", font=std_font).pack()
        self.cube_initial = CubeNet(frame_initial, scramble=True)
        self.cube_initial.pack(pady=10)

        # Estado Objetivo
        frame_goal = tk.Frame(states_frame)
        frame_goal.pack(side=tk.LEFT, expand=True)
        tk.Label(frame_goal, text="Estado Objetivo", font=std_font).pack()
        self.cube_goal = CubeNet(frame_goal, editable=False)
        self.cube_goal.pack(pady=10)

        # Visualizador do Resultado Gráfico
        frame_result = tk.Frame(states_frame)
        frame_result.pack(side=tk.LEFT, expand=True)
        tk.Label(frame_result, text="Visualizador do Caminho", font=std_font).pack()
        self.cube_result = CubeNet(frame_result, editable=False)
        self.cube_result.pack(pady=10)
        
        # Controles do visualizador
        nav_frame = tk.Frame(frame_result)
        nav_frame.pack()
        self.btn_prev = tk.Button(nav_frame, text="< Anterior", command=self.prev_step, state=tk.DISABLED)
        self.btn_prev.pack(side=tk.LEFT, padx=5)
        self.lbl_step = tk.Label(nav_frame, text="Passo: 0/0")
        self.lbl_step.pack(side=tk.LEFT, padx=5)
        self.btn_next = tk.Button(nav_frame, text="Próximo >", command=self.next_step, state=tk.DISABLED)
        self.btn_next.pack(side=tk.LEFT, padx=5)

        # --- PAINEL DE RESULTADOS TEXTUAIS (Base) ---
        results_frame = tk.Frame(self.root, padx=20, pady=10)
        results_frame.pack(fill=tk.BOTH, expand=True)

        self.lbl_cost = tk.Label(results_frame, text="Custo do Caminho: -", font=("Arial", 11, "bold"), fg="blue")
        self.lbl_cost.pack(anchor=tk.W)

        tk.Label(results_frame, text="Caminho Encontrado (Movimentos):").pack(anchor=tk.W, pady=(10, 0))
        self.txt_path = tk.Text(results_frame, height=5, width=80, state=tk.DISABLED)
        self.txt_path.pack(fill=tk.BOTH, expand=True)

    def solve(self):
        """Método chamado ao clicar em Resolver. Aqui você conectará seu backend."""
        algo = self.algo_var.get()

        print(self.cube_initial.cube.validate_stickers())

        id_start = self.cube_initial.cube.get_cube().get_id()
        id_goal = self.cube_result.cube.get_cube().get_id()
        self.solution_path = apply_algorithm(algo, id_start, id_goal)
        
        # SIMULAÇÃO DE RESULTADO:
        mock_cost = len(self.solution_path) - 1
        mock_path_str = stringify_path(self.solution_path)
        
        # ==========================================

        # Atualizando a UI com os resultados textuais
        self.lbl_cost.config(text=f"Custo do Caminho: {mock_cost} | Algoritmo: {algo}")
        
        self.txt_path.config(state=tk.NORMAL)
        self.txt_path.delete(1.0, tk.END)
        self.txt_path.insert(tk.END, mock_path_str)
        self.txt_path.config(state=tk.DISABLED)

        # Resetando o visualizador gráfico
        self.current_step = 0
        if self.solution_path:
            self.update_viewer()

    def update_viewer(self):
        """Atualiza o cubo do visualizador e os botões de navegação."""
        total_steps = len(self.solution_path) - 1
        self.lbl_step.config(text=f"Passo: {self.current_step}/{total_steps}")
        
        current_state = self.solution_path[self.current_step]
        sticker_cube = StickersCube(cube=get_state_lup(current_state), BLD=self.cube_initial.cube.get_BLD())
        self.cube_result.cube = sticker_cube
        self.cube_result.draw_net()

        self.btn_prev.config(state=tk.NORMAL if self.current_step > 0 else tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL if self.current_step < total_steps else tk.DISABLED)

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_viewer()

    def next_step(self):
        if self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.update_viewer()

if __name__ == "__main__":
    root = tk.Tk()
    app = RubiksSolverGUI(root)
    root.mainloop()