import tkinter as tk
from tkinter import ttk
from src.stickers import StickersCube, Subcubes, Colors, OFFSETS
from src.cube import Cube, get_state_lup, grafo, nos
from src.BuscaNP import buscaNP
import numpy as np
import math

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
    def __init__(self, master, sticker_size=30, editable=True, cube: StickersCube=None, **kwargs):
        super().__init__(master, width=sticker_size*8, height=sticker_size*6, bg='#f0f0f0', highlightthickness=0, **kwargs)
        self.size = sticker_size
        self.editable = editable
        self.stickers = {} # Armazena os IDs dos retângulos
        if cube:
            self.cube = cube
        else:
            self.cube = StickersCube()
        
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

class ControlPanel(tk.Frame):
    """Encapsulates the top control bar (Algorithm selection and Solve button)."""
    def __init__(self, parent, on_solve_callback, **kwargs):
        super().__init__(parent, pady=10, **kwargs)
        self.on_solve_callback = on_solve_callback
        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self, text="Método de Busca:", font=std_font).pack(side=tk.LEFT, padx=10)
        
        self.algo_var = tk.StringVar()
        algos = ['Amplitude', 'Profundidade', 'Profundidade Limitada', 'Aprofundamento Iterativo', 
                 'Bidirecional', 'Custo Uniforme', 'Greedy', 'A*', 'IDA* (AIA)']
        self.algo_combo = ttk.Combobox(self, textvariable=self.algo_var, values=algos, state="readonly", width=25)
        self.algo_combo.current(0)
        self.algo_combo.pack(side=tk.LEFT, padx=10)

        self.btn_solve = tk.Button(self, text="Resolver Cubo", bg="#4CAF50", fg="white",  
                                   activebackground="#0A480C", activeforeground="white",
                                   font=std_font, command=self._trigger_solve)
        self.btn_solve.pack(side=tk.LEFT, padx=20)

    def _trigger_solve(self):
        # Pass the selected algorithm back to the main controller
        self.on_solve_callback(self.algo_var.get())


class StatesPanel(tk.Frame):
    """Encapsulates the Initial, Goal, and Result viewers, plus step navigation."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.solution_path = []
        self.current_step = 0
        self._setup_ui()

    def _setup_ui(self):
        # Instead of packing the whole self, we'll use grid inside it
        # Configure columns to distribute weight evenly
        for i in range(3):
            self.columnconfigure(i, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- ROW 0, 1: THE CUBES ---
        
        # Estado Inicial
        lbl_initial = tk.Label(self, text="Estado Inicial (Clique para alterar)", font=std_font)
        lbl_initial.grid(row=0, column=0, sticky="s")
        self.cube_initial = CubeNet(self)
        self.cube_initial.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        # Estado Objetivo
        lbl_goal = tk.Label(self, text="Estado Objetivo", font=std_font)
        lbl_goal.grid(row=0, column=1, sticky="s")
        self.cube_goal = CubeNet(self, editable=False)
        self.cube_goal.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        # Visualizador do Resultado Gráfico
        lbl_result = tk.Label(self, text="Visualizador do Caminho", font=std_font)
        lbl_result.grid(row=0, column=2, sticky="s")
        self.cube_result = CubeNet(self, editable=False)
        self.cube_result.grid(row=1, column=2, padx=10, pady=10, sticky="n")

        # --- ROW 2: Nav, buttons ---

        self.scramble_btn_initial = tk.Button(self, text="Embaralhar", command=lambda net=self.cube_initial: self.scramble(cubeNet=net))
        self.scramble_btn_initial.grid(row=2, column=0, sticky="n")

        self.scramble_btn_goal = tk.Button(self, text="Embaralhar", command=lambda net=self.cube_goal: self.scramble(cubeNet=net))
        self.scramble_btn_goal.grid(row=2, column=1, sticky="n")

        nav_frame = tk.Frame(self)
        nav_frame.grid(row=2, column=2, sticky="n")

        # Inside the nav_frame, we can still use pack for the buttons 
        # because they are just a simple horizontal line.
        self.btn_prev = tk.Button(nav_frame, text="<<", command=self.prev_step, state=tk.DISABLED)
        self.btn_prev.pack(side="left", padx=3)
        
        self.lbl_step = tk.Label(nav_frame, text="Passo: 0/0")
        self.lbl_step.pack(side="left", padx=3)

        self.btn_next = tk.Button(nav_frame, text=">>", command=self.next_step, state=tk.DISABLED)
        self.btn_next.pack(side="left", padx=3)
        

    def load_solution(self, path):
        self.solution_path = path
        self.current_step = 0
        if self.solution_path:
            self._update_viewer()

    def _update_viewer(self):
        total_steps = len(self.solution_path) - 1
        self.lbl_step.config(text=f"Passo: {self.current_step}/{total_steps}")
        
        current_state = self.solution_path[self.current_step]
        # Uses BLD from the initial cube as requested
        sticker_cube = StickersCube(cube=get_state_lup(current_state), BLD=self.cube_initial.cube.get_BLD())
        self.cube_result.cube = sticker_cube
        self.cube_result.draw_net()

        self.btn_prev.config(state=tk.NORMAL if self.current_step > 0 else tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL if self.current_step < total_steps else tk.DISABLED)

    def scramble(self, cubeNet: CubeNet):
        cubeNet.cube.scramble()
        cubeNet.draw_net()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self._update_viewer()

    def next_step(self):
        if self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self._update_viewer()


class ResultsPanel(tk.Frame):
    """Encapsulates the textual path output, cost, and pagination logic."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, padx=20, pady=10, **kwargs)
        self.full_path_str = ""
        self.current_page = 0
        self.chars_per_page = 380
        self._setup_ui()

    def _setup_ui(self):
        self.lbl_cost = tk.Label(self, text="Custo do Caminho: -", font=("Arial", 11, "bold"), fg="blue")
        self.lbl_cost.pack(anchor=tk.W)

        self.txt_path = tk.Text(self, height=5, width=80, state=tk.DISABLED, wrap=tk.CHAR)
        self.txt_path.pack(fill=tk.BOTH, expand=True)

        self.pagination_frame = tk.Frame(self)
        self.pagination_frame.pack(fill=tk.X, pady=(5, 0))

        self.btn_prev_page = tk.Button(self.pagination_frame, text="< Anterior", command=self.prev_page, state=tk.DISABLED)
        self.btn_prev_page.pack(side=tk.LEFT)

        self.lbl_page = tk.Label(self.pagination_frame, text="Página 1 de 1")
        self.lbl_page.pack(side=tk.LEFT, expand=True)

        self.btn_next_page = tk.Button(self.pagination_frame, text="Próximo >", command=self.next_page, state=tk.DISABLED)
        self.btn_next_page.pack(side=tk.RIGHT)

    def display_results(self, algo, cost, path_str):
        self.lbl_cost.config(text=f"Custo do Caminho: {cost} | Algoritmo: {algo}")
        self.full_path_str = path_str
        self.current_page = 0
        self._update_page_view()

    def _update_page_view(self):
        total_len = len(self.full_path_str)
        total_pages = max(1, math.ceil(total_len / self.chars_per_page))
        
        start_idx = self.current_page * self.chars_per_page
        end_idx = start_idx + self.chars_per_page
        page_text = self.full_path_str[start_idx:end_idx]
        
        self.txt_path.config(state=tk.NORMAL)
        self.txt_path.delete(1.0, tk.END)
        self.txt_path.insert(tk.END, page_text)
        self.txt_path.config(state=tk.DISABLED)
        
        self.lbl_page.config(text=f"Página {self.current_page + 1} de {total_pages}")
        self.btn_prev_page.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        self.btn_next_page.config(state=tk.NORMAL if self.current_page < total_pages - 1 else tk.DISABLED)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self._update_page_view()

    def next_page(self):
        total_pages = math.ceil(len(self.full_path_str) / self.chars_per_page)
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self._update_page_view()


class RubiksSolverGUI:
    """The Main App Controller/Mediator. Orchestrates the sub-panels."""
    def __init__(self, root):
        self.root = root
        self.root.title("Cubo Mágico 2x2x2 - Buscas em IA")
        self.root.geometry("850x650")
        
        # Instantiate UI Components
        self.control_panel = ControlPanel(self.root, on_solve_callback=self.solve)
        self.control_panel.pack(fill=tk.X)

        self.states_panel = StatesPanel(self.root)
        self.states_panel.pack(fill=tk.BOTH, expand=True, pady=10)

        self.results_panel = ResultsPanel(self.root)
        self.results_panel.pack(fill=tk.BOTH, expand=True)

    def solve(self, algo):
        """Called by the ControlPanel when the solve button is clicked."""
        id_start = self.states_panel.cube_initial.cube.get_cube().get_id()
        id_goal = self.states_panel.cube_goal.cube.get_cube().get_id()
        
        # Backend Processing
        solution_path = apply_algorithm(algo, id_start, id_goal)
        
        # Data formatting
        mock_cost = len(solution_path) - 1
        mock_path_str = stringify_path(solution_path)
        
        # Dispatch data to the presentation layer (UI components)
        self.results_panel.display_results(algo, mock_cost, mock_path_str)
        self.states_panel.load_solution(solution_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = RubiksSolverGUI(root)
    root.mainloop()