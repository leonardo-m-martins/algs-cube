from src.gui import tk, RubiksSolverGUI

def main():
    root = tk.Tk()
    app = RubiksSolverGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()