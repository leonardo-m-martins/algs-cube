import tkinter as tk
from tkinter import ttk, messagebox
from src.stickers import StickersCube, Subcubes, Colors, OFFSETS
from src.cube import Cube, get_state_lup, grafo, nos, get_heuristic
from src.BuscaNP import buscaNP
from src.BuscaP import buscaP
import numpy as np
import math

# Cores padrão do Cubo Mágico
COLORS = {Colors.WHITE: 'white', Colors.RED: 'red', Colors.BLUE: 'blue', Colors.ORANGE: 'orange', Colors.GREEN: 'green', Colors.YELLOW: 'yellow'}
COLORS_REVERSED_MAP = {value: key for key, value in COLORS.items()}

MOVE_NAMES = ['U', 'U2', 'U3', 'R', 'R2', 'R3', 'F', 'F2', 'F3']

busca = buscaNP()
p_busca = buscaP()

def stringify_path(path: list) -> str:
    moves = []
    for i in range(len(path) - 1):
        move_idx = np.where(grafo[path[i]] == path[i+1])[0][0]
        moves.append(MOVE_NAMES[move_idx])
    return ' '.join(moves)


def apply_algorithm(algo: str, initial, objective, lim: int=14, weights: tuple=None, heuristic: np.ndarray=None):
    algos = ('Amplitude', 'Profundidade', 'Profundidade Limitada', 
             'Aprofundamento Iterativo', 'Bidirecional', 'Custo Uniforme', 
             'Greedy', 'A*', 'IDA* (AIA)')
    if algo == algos[0]:
        caminho = busca.amplitude_grafo(initial, objective, nos=nos, grafo=grafo)
        return caminho, len(caminho) - 1
    elif algo == algos[1]:
        caminho = busca.profundidade_grafo(initial, objective, nos, grafo)
        return caminho, len(caminho) - 1
    elif algo == algos[2]:
        caminho = busca.prof_limitada_grafo(initial, objective, nos, grafo, lim)
        return caminho, len(caminho) - 1
    elif algo == algos[3]:
        caminho = busca.aprof_iterativo_grafo(initial, objective, nos, grafo, lim)
        return caminho, len(caminho) - 1
    elif algo == algos[4]:
        caminho = busca.bidirecional_grafo(initial, objective, nos, grafo)
        return caminho, len(caminho) - 1
    elif algo == algos[5]:
        return p_busca.custo_uniforme_grafo(initial, objective, nos, grafo, weights)
    elif algo == algos[6]:
        return p_busca.greedy_grafo(initial, objective, nos, grafo, weights, heuristic)
    # elif algo == algos[7]:
    #     return p_busca.a_estrela_grafo(initial, objective, nos, grafo, weights)
    # elif algo == algos[8]:
    #     return p_busca.aia_estrela_grafo(initial, objective, nos, grafo, weights)
    else: 
        raise Exception("Não implementado")

std_font = ("Arial", 10, "bold")

class ColorSelector(tk.Frame):
    """A reusable widget containing 6 color blocks that map to values 0-5."""
    def __init__(self, parent, on_select_callback=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Callback to notify the parent when a color is picked
        self.on_select_callback = on_select_callback
        
        # Attribute to store the number (0 to 5)
        self.selected_value = None
        
        # Keep track of the button widgets to update their states
        self.buttons = [None for _ in range(len(COLORS))]
        
        self._setup_ui()

    def _setup_ui(self):
        for i, color in COLORS.items():
            # Create the button. 
            # We use a lambda with a default argument (idx=i) to capture the correct index for each button.
            btn = tk.Button(
                self, 
                bg=color, 
                activebackground=color, # Keep the color same when clicked
                width=4, 
                height=2, 
                relief=tk.RAISED,
                command=lambda idx=i: self._select_color(idx)
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.buttons[i] = btn

        self._select_color(0)

    def _select_color(self, index):
        """Handles the logic when a color button is clicked."""
        
        # 1. Reset all buttons to their default state (clickable and raised)
        for btn in self.buttons:
            btn.config(state=tk.NORMAL, relief=tk.RAISED, borderwidth=2)
            
        # 2. Highlight the selected button (make it sunken, thicker border, and disable it)
        selected_btn = self.buttons[index]
        selected_btn.config(state=tk.DISABLED, relief=tk.SUNKEN, borderwidth=4)
        
        # 3. Save the index (0 to 5) to the attribute
        self.selected_value = index
        
        # 4. If a callback was provided, send the chosen number back to the parent
        if self.on_select_callback:
            self.on_select_callback(self.selected_value)


class CubeNet(tk.Canvas):
    """Componente gráfico que desenha a planificação de um cubo 2x2x2."""
    def __init__(self, master, color_selector: ColorSelector, on_click_callback=None, sticker_size=30, editable=True, cube: StickersCube=None, **kwargs):
        super().__init__(master, width=sticker_size*8, height=sticker_size*6, bg='#f0f0f0', highlightthickness=0, **kwargs)
        self.size = sticker_size
        self.editable = editable
        self.stickers = {} # Armazena os IDs dos retângulos
        self.color_selector = color_selector
        self.on_click_callback = on_click_callback

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
            

    def on_click(self, event):
        item = self.find_withtag("current")
        if item:
            rect_id = item[0]
            next_color_idx = self.color_selector.selected_value
            next_color = COLORS[next_color_idx]
            self.itemconfig(rect_id, fill=next_color)
            key, idx = self.stickers[rect_id]
            self.cube.state[key][idx] = next_color_idx

            if self.on_click_callback:
                self.on_click_callback()

class LimParam(tk.Frame):
    """Component for single integer input (Depth Limit)."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        tk.Label(self, text="Limite Máx:", font=std_font).pack(side=tk.LEFT, padx=(5, 2))
        
        self.val_var = tk.IntVar(value=10)
        self.spin = tk.Spinbox(self, from_=1, to=100, textvariable=self.val_var, width=5, font=std_font)
        self.spin.pack(side=tk.LEFT)

    def get(self):
        try:
            return self.val_var.get()
        except tk.TclError:
            raise ValueError("O limite deve ser um número inteiro válido.")


class WeightsParam(tk.Frame):
    """Component for 9 integer inputs arranged in a compact grid."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        tk.Label(self, text="Pesos:", font=std_font).pack(side=tk.LEFT, padx=(5, 10))
        
        # We use an internal frame to grid the 9 inputs neatly
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(side=tk.LEFT)
        
        self.weight_vars = {}
        
        # Populate a 3x3 grid for the 9 moves
        for i in range(len(MOVE_NAMES)):
            row = i // 3
            col = i % 3
            
            cell = tk.Frame(self.grid_frame)
            cell.grid(row=row, column=col, padx=5, pady=2)
            
            tk.Label(cell, text=f"{MOVE_NAMES[i]}:", font=("Arial", 9)).pack(side=tk.LEFT)
            
            var = tk.IntVar(value=10)  # Default weight is 10
            self.weight_vars[i] = var
            tk.Spinbox(cell, from_=0, to=100, textvariable=var, width=3).pack(side=tk.LEFT)

    def get(self):
        try:
            # Returns a dictionary of { 'U': 1, 'U2': 2, ... }
            return [self.weight_vars[move].get() for move in range(len(MOVE_NAMES))]
        except tk.TclError:
            raise ValueError("Os pesos devem ser números inteiros válidos.")


class ControlPanel(tk.Frame):
    """Encapsulates the top control bar (Algorithm selection, dynamic params, and Solve button)."""
    def __init__(self, parent, on_solve_callback, **kwargs):
        super().__init__(parent, pady=10, **kwargs)
        self.on_solve_callback = on_solve_callback
        
        # Categorize algorithms
        self.algos_lim = ['Profundidade Limitada', 'Aprofundamento Iterativo']
        self.algos_weights = ['Custo Uniforme', 'Greedy', 'A*', 'IDA* (AIA)']
        
        self._setup_ui()

    def _setup_ui(self):
        # --- Top Row (Combo and Button) ---
        self.top_row = tk.Frame(self)
        self.top_row.pack(fill=tk.X)

        tk.Label(self.top_row, text="Método de Busca:", font=std_font).pack(side=tk.LEFT, padx=10)
        
        self.algo_var = tk.StringVar()
        algos = ['Amplitude', 'Profundidade', 'Profundidade Limitada', 'Aprofundamento Iterativo', 
                 'Bidirecional', 'Custo Uniforme', 'Greedy', 'A*', 'IDA* (AIA)']
        self.algo_combo = ttk.Combobox(self.top_row, textvariable=self.algo_var, values=algos, state="readonly", width=25)
        self.algo_combo.current(0)
        self.algo_combo.pack(side=tk.LEFT, padx=10)
        self.algo_combo.bind("<<ComboboxSelected>>", self._update_dynamic_params)

        self.btn_solve = tk.Button(self.top_row, text="Resolver Cubo", bg="#4CAF50", fg="white",  
                                   activebackground="#0A480C", activeforeground="white",
                                   font=std_font, command=self._trigger_solve)
        self.btn_solve.pack(side=tk.LEFT, padx=20)

        # --- Bottom Row (Dynamic Parameters) ---
        self.param_row = tk.Frame(self)
        self.param_row.pack(fill=tk.X, pady=(10, 0)) # Slight padding from top row

        # Instantiate both parameter panels, but don't pack them yet
        self.lim_param = LimParam(self.param_row)
        self.weights_param = WeightsParam(self.param_row)

        # Ensure correct UI state on load
        self._update_dynamic_params()

    def _update_dynamic_params(self, event=None):
        """Hides/Shows the relevant parameter configuration."""
        algo = self.algo_var.get()
        
        # Hide both first
        self.lim_param.pack_forget()
        self.weights_param.pack_forget()
        
        # Show the correct one
        if algo in self.algos_lim:
            self.lim_param.pack(side=tk.LEFT, padx=10)
        elif algo in self.algos_weights:
            self.weights_param.pack(side=tk.LEFT, padx=10)

    def _trigger_solve(self):
        algo = self.algo_var.get()
        
        try:
            # Extract parameters if the algorithm requires them
            if algo in self.algos_lim:
                lim = self.lim_param.get()
                weights = None
            elif algo in self.algos_weights:
                lim = None
                weights = self.weights_param.get()
            else:
                lim = None
                weights = None
        except ValueError as e:
            # Catches the Tkinter TclError (blank input or letters) raised in our param classes
            messagebox.showwarning("Entrada Inválida", str(e))
            return
            
        # Pass the selected algorithm and a dict of params back to the main controller
        self.on_solve_callback(algo, lim, weights)


class StatesPanel(tk.Frame):
    """Encapsulates the Initial, Goal, and Result viewers, plus step navigation."""
    def __init__(self, parent, color_selector: ColorSelector, **kwargs):
        super().__init__(parent, **kwargs)
        self.solution_path = []
        self.current_step = 0
        self._setup_ui(color_selector)
        self.update_heuristic()

    def _setup_ui(self, color_selector: ColorSelector):
        self.alert_banner = AlertBanner(self)

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
        self.cube_initial = CubeNet(self, color_selector)
        self.cube_initial.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        # Estado Objetivo
        lbl_goal = tk.Label(self, text="Estado Objetivo", font=std_font)
        lbl_goal.grid(row=0, column=1, sticky="s")
        self.cube_goal = CubeNet(self, color_selector, self.update_heuristic)
        self.cube_goal.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        # Visualizador do Resultado Gráfico
        lbl_result = tk.Label(self, text="Visualizador do Caminho", font=std_font)
        lbl_result.grid(row=0, column=2, sticky="s")
        self.cube_result = CubeNet(self, color_selector, editable=False)
        self.cube_result.grid(row=1, column=2, padx=10, pady=10, sticky="n")

        # --- ROW 2: Nav, buttons ---

        self.btns_frame_1 = tk.Frame(self)
        self.btns_frame_1.grid(row=2, column=0, sticky="n")

        self.scramble_btn_initial = tk.Button(self.btns_frame_1, text="Embaralhar", command=lambda net=self.cube_initial: self.scramble(cubeNet=net))
        self.scramble_btn_initial.pack(side="left")

        self.reset_btn_initial = tk.Button(self.btns_frame_1, text="Resetar", command=lambda net=self.cube_initial: self.reset_cube(cubeNet=net))
        self.reset_btn_initial.pack(side="left")

        self.btns_frame_2 = tk.Frame(self)
        self.btns_frame_2.grid(row=2, column=1, sticky="n")

        self.scramble_btn_goal = tk.Button(self.btns_frame_2, text="Embaralhar", command=lambda net=self.cube_goal: self.scramble(cubeNet=net))
        self.scramble_btn_goal.pack(side="left")

        self.reset_btn_goal = tk.Button(self.btns_frame_2, text="Resetar", command=lambda net=self.cube_goal: self.reset_cube(cubeNet=net))
        self.reset_btn_goal.pack(side="left")

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
        if cubeNet.on_click_callback:
            cubeNet.on_click_callback()

    def reset_cube(self, cubeNet: CubeNet):
        cubeNet.cube = StickersCube()
        cubeNet.draw_net()
        if cubeNet.on_click_callback:
            cubeNet.on_click_callback()

    def validate_cube(self, name: str, cube: StickersCube) -> bool:
        if not cube.validate_stickers():
            self.alert_banner.show(f"{name} inválido: arranjo de stickers inválido")
            return False
        try:
            cube_arr = cube.get_cube()
        except:
            self.alert_banner.show(f"{name} inválido: Orientação inválida")
            return False
        if not cube_arr.validate_ori():
            self.alert_banner.show(f"{name} inválido: Orientação inválida")
            return False
        return True
    
    def validate_cube_silent(self, cube: StickersCube) -> bool:
        if not cube.validate_stickers():
            return False
        try:
            cube_arr = cube.get_cube()
        except:
            return False
        return cube_arr.validate_ori()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self._update_viewer()

    def next_step(self):
        if self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self._update_viewer()

    def update_heuristic(self):
        cube = self.cube_goal.cube
        if not self.validate_cube_silent(cube):
            return
        id_goal = cube.get_cube().get_id()
        self.heuristic = get_heuristic(id_goal)

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

class AlertBanner(tk.Frame):
    """A floating notification banner for errors or success messages."""
    def __init__(self, parent, **kwargs):
        # We use a solid red background for errors by default
        super().__init__(parent, bg="#f44336", bd=2, relief=tk.RAISED, **kwargs)
        
        # The label that holds the actual text
        self.lbl_message = tk.Label(self, text="", bg="#f44336", fg="white", font=std_font)
        self.lbl_message.pack(side=tk.LEFT, padx=(15, 5), pady=5)
        
        # A manual close button just in case the user doesn't want to wait
        self.btn_close = tk.Button(self, text="✖", bg="#f44336", fg="white", bd=0, 
                                   activebackground="#d32f2f", activeforeground="white", 
                                   command=self.hide)
        self.btn_close.pack(side=tk.RIGHT, padx=(5, 10), pady=5)

        # Store the timer ID so we can cancel it if a new message appears quickly
        self._timer_id = None

    def show(self, message, duration_ms=3000, is_error=True):
        """Displays the banner with the message."""
        # Cancel any existing auto-hide timer if we are showing a new message
        if self._timer_id is not None:
            self.after_cancel(self._timer_id)

        # Change colors based on whether it's an error or success
        bg_color = "#f44336" if is_error else "#4CAF50" # Red for error, Green for success
        self.config(bg=bg_color)
        self.lbl_message.config(text=message, bg=bg_color)
        self.btn_close.config(bg=bg_color, activebackground=bg_color)

        # Place the banner floating near the top center of the parent window.
        # relx=0.5 puts the center of the widget exactly in the middle of the screen.
        self.place(relx=0.5, rely=0, anchor=tk.N)
        self.lift()

        # Automatically hide it after 'duration_ms' milliseconds
        if duration_ms > 0:
            self._timer_id = self.after(duration_ms, self.hide)

    def hide(self):
        """Removes the banner from the screen."""
        self.place_forget()
        self._timer_id = None

class RubiksSolverGUI:
    """The Main App Controller/Mediator. Orchestrates the sub-panels."""
    def __init__(self, root):
        self.root = root
        self.root.title("Cubo Mágico 2x2x2 - Buscas em IA")
        self.root.geometry("850x650")
        
        # Instantiate UI Components
        self.control_panel = ControlPanel(self.root, on_solve_callback=self.solve)
        self.control_panel.pack(fill=tk.X)

        self.color_selector = ColorSelector(self.root)

        self.states_panel = StatesPanel(self.root, self.color_selector)
        self.states_panel.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.color_selector.pack()

        self.results_panel = ResultsPanel(self.root)
        self.results_panel.pack(fill=tk.BOTH, expand=True)

    def solve(self, algo, lim, weights):
        """Called by the ControlPanel when the solve button is clicked."""
        start_sticker_cube = self.states_panel.cube_initial.cube
        goal_sticker_cube = self.states_panel.cube_goal.cube

        if not self.states_panel.validate_cube("Estado Inicial", start_sticker_cube):
            return
        if not self.states_panel.validate_cube("Estado Objetivo", goal_sticker_cube):
            return
        
        goal_sticker_cube = goal_sticker_cube.copy_match_BLD(start_sticker_cube.get_BLD())

        if not self.states_panel.validate_cube("Estado Objetivo", goal_sticker_cube):
            return

        id_start = start_sticker_cube.get_cube().get_id()
        id_goal = goal_sticker_cube.get_cube().get_id()

        heuristic = self.states_panel.heuristic
        
        # Backend Processing
        solution_path, mock_cost = apply_algorithm(algo, id_start, id_goal, lim, weights, heuristic)
        
        # Data formatting
        mock_path_str = stringify_path(solution_path)
        
        # Dispatch data to the presentation layer (UI components)
        self.results_panel.display_results(algo, mock_cost, mock_path_str)
        self.states_panel.load_solution(solution_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = RubiksSolverGUI(root)
    root.mainloop()