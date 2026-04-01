import tkinter as tk
from tkinter import ttk

# Cores padrão do Cubo Mágico
COLORS = ['white', 'red', 'blue', 'orange', 'green', 'yellow']

std_font = ("Arial", 10, "bold")

class CubeNet(tk.Canvas):
    """Componente gráfico que desenha a planificação de um cubo 2x2x2."""
    def __init__(self, master, sticker_size=30, editable=True, **kwargs):
        super().__init__(master, width=sticker_size*8, height=sticker_size*6, bg='#f0f0f0', highlightthickness=0, **kwargs)
        self.size = sticker_size
        self.editable = editable
        self.stickers = {} # Armazena os IDs dos retângulos
        self.state = []    # Armazena as cores atuais
        
        # Mapeamento das faces na planificação (coluna, linha) em blocos 2x2
        # U(Top), L(Left), F(Front), R(Right), B(Back), D(Bottom)
        faces_layout = {
            'U': (2, 0),
            'L': (0, 2),
            'F': (2, 2),
            'R': (4, 2),
            'B': (6, 2),
            'D': (2, 4)
        }
        
        self.draw_net(faces_layout)
        if self.editable:
            self.bind("<Button-1>", self.on_click)

    def draw_net(self, layout):
        idx = 0
        for face, (col_offset, row_offset) in layout.items():
            for row in range(2):
                for col in range(2):
                    x1 = (col_offset + col) * self.size
                    y1 = (row_offset + row) * self.size
                    x2 = x1 + self.size
                    y2 = y1 + self.size
                    
                    # Cor inicial padrão (pode ser alterada)
                    color = COLORS[list(layout.keys()).index(face)]
                    
                    rect_id = self.create_rectangle(x1, y1, x2, y2, fill=color, outline='black', width=2)
                    self.stickers[rect_id] = idx
                    self.state.append(color)
                    idx += 1

    def on_click(self, event):
        item = self.find_withtag("current")
        if item:
            rect_id = item[0]
            current_color = self.itemcget(rect_id, "fill")
            next_color = COLORS[(COLORS.index(current_color) + 1) % len(COLORS)]
            self.itemconfig(rect_id, fill=next_color)
            idx = self.stickers[rect_id]
            self.state[idx] = next_color

    def get_state(self):
        return self.state.copy()

    def set_state(self, new_state):
        self.state = new_state.copy()
        for rect_id, idx in self.stickers.items():
            self.itemconfig(rect_id, fill=self.state[idx])

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
        self.cube_initial = CubeNet(frame_initial)
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
        start_state = self.cube_initial.get_state()
        goal_state = self.cube_goal.get_state()
        
        # ==========================================
        # TODO: SUBSTITUIR PELO SEU ALGORITMO REAL
        # ==========================================
        # Aqui é onde o programa enviará `start_state` e `goal_state`
        # para o seu motor de busca em Python.
        
        # SIMULAÇÃO DE RESULTADO:
        mock_cost = 3
        mock_path_str = "R U R'"
        
        # Simulando os estados do cubo a cada passo (para o visualizador gráfico)
        # Em um cenário real, seu algoritmo retornará a lista de estados intermediários
        self.solution_path = [
            start_state,
            start_state, # Mock do estado 1
            start_state, # Mock do estado 2
            goal_state   # Estado final
        ]
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
        self.cube_result.set_state(current_state)

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