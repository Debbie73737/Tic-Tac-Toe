import tkinter as tk
from tkinter import messagebox
import winsound  # Add this import
import time  # Add this import for pauses between notes
from tkinter import simpledialog  # For symbol selection dialogs
import math  # For trigonometric functions in firework
import pygame  # For background music

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.symbol_choices = ['♥', '☀', 'X', 'O', '★', '☾']
        self.player_symbols = self.choose_symbols()
        if not self.player_symbols or None in self.player_symbols:
            return  # Exit __init__ if dialog was cancelled
        self.player = self.player_symbols[0]  # Player 1 starts
        self.board = [None] * 9
        self.buttons = []
        self.scores = {self.player_symbols[0]: 0, self.player_symbols[1]: 0}
        self.rounds_to_win = 5
        self.create_widgets()
        self.update_scoreboard()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        # Start background music using pygame
        pygame.mixer.init()
        pygame.mixer.music.load(r'559832__migfus20__cute-music.mp3')
        pygame.mixer.music.play(-1)  # Loop indefinitely

    def choose_symbols(self):
        # Symbol names for display and lookup
        symbol_names = {
            '♥': 'heart',
            '☀': 'sun',
            'X': 'X',
            'O': 'O',
            '★': 'star',
            '☾': 'moon'
        }
        # Create a lookup for both symbol and name (case-insensitive)
        symbol_lookup = {s: s for s in self.symbol_choices}
        symbol_lookup.update({v.lower(): k for k, v in symbol_names.items()})
        # Dialog for Player 1
        while True:
            choices_str = ', '.join([f"{symbol_names[s]} = {s}" for s in self.symbol_choices])
            p1_input = simpledialog.askstring(
                "Player 1 Symbol",
                f"Player 1, choose your symbol by entering the symbol or its name:\n{choices_str}",
                parent=self.root
            )
            if p1_input is None:
                self.root.destroy()
                return None, None
            if not p1_input.strip():
                continue
            p1_key = p1_input.strip().lower()
            p1 = symbol_lookup.get(p1_key, symbol_lookup.get(p1_input.strip()))
            if p1 in self.symbol_choices:
                break
            messagebox.showerror("Invalid Symbol", "Please choose a valid symbol or name.")
        # Dialog for Player 2
        choices_p2 = [s for s in self.symbol_choices if s != p1]
        symbol_lookup_p2 = {s: s for s in choices_p2}
        symbol_lookup_p2.update({symbol_names[s].lower(): s for s in choices_p2})
        while True:
            choices_str_p2 = ', '.join([f"{symbol_names[s]} = {s}" for s in choices_p2])
            p2_input = simpledialog.askstring(
                "Player 2 Symbol",
                f"Player 2, choose your symbol by entering the symbol or its name:\n{choices_str_p2}",
                parent=self.root
            )
            if p2_input is None:
                self.root.destroy()
                return None, None
            if not p2_input.strip():
                continue
            p2_key = p2_input.strip().lower()
            p2 = symbol_lookup_p2.get(p2_key, symbol_lookup_p2.get(p2_input.strip()))
            if p2 in choices_p2:
                break
            messagebox.showerror("Invalid Symbol", "Please choose a valid symbol or name that is not taken.")
        return (p1, p2)
        self.root.deiconify()

    def create_widgets(self):
        # Set the background color of the main window to light pink
        self.root.configure(bg='#FFD1DC')  # Light pink
        # Scoreboard
        self.score_label = tk.Label(self.root, text="", font=('Arial', 14), bg='#FFD1DC')
        self.score_label.grid(row=0, column=0, columnspan=3, pady=10)
        # Board frame with white background for grid lines
        self.board_frame = tk.Frame(self.root, bg='white')
        self.board_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        # Board buttons
        for i in range(9):
            btn = tk.Button(
                self.board_frame,
                text="",
                font=('Arial', 32),
                width=5,
                height=2,
                command=lambda i=i: self.make_move(i),
                bg='#FFD1DC',  # Light pink background
                activebackground='#FFD1DC',
                bd=0,  # No default border
                relief='flat',
            )
            btn.grid(row=i // 3, column=i % 3, padx=3, pady=3)  # Padding for white grid lines
            self.buttons.append(btn)
        # Reset button
        self.reset_btn = tk.Button(self.root, text="Restart Game", font=('Arial', 12), command=self.reset_game, bg='#FFD1DC')
        self.reset_btn.grid(row=4, column=0, columnspan=3, pady=10)

    def show_firework_and_message(self, winner):
        # Create a new top-level window
        firework_win = tk.Toplevel(self.root)
        firework_win.configure(bg='black')
        firework_win.geometry('500x400')
        firework_win.title('Congratulations!')
        firework_win.transient(self.root)  # Keep on top of main window
        firework_win.focus_set()           # Focus the popup
        canvas = tk.Canvas(firework_win, width=500, height=300, bg='black', highlightthickness=0)
        canvas.pack(pady=10)
        msg_label = tk.Label(firework_win, text='', font=('Arial', 24, 'bold'), fg='magenta', bg='black')
        msg_label.pack(pady=10)

        import random
        def draw_firework():
            canvas.delete('all')
            x, y = 250, 150
            colors = ['red', 'yellow', 'magenta', 'cyan', 'lime', 'orange', 'white', 'blue']
            for _ in range(12):
                angle = random.uniform(0, 2*math.pi)
                length = random.randint(80, 130)
                color = random.choice(colors)
                x2 = x + length * math.cos(angle)
                y2 = y + length * math.sin(angle)
                canvas.create_line(x, y, x2, y2, fill=color, width=4)
            # Draw a burst
            for _ in range(20):
                rx = x + random.randint(-40, 40)
                ry = y + random.randint(-40, 40)
                canvas.create_oval(rx, ry, rx+8, ry+8, fill=random.choice(colors), outline='')

        def animate_firework(frames=10):
            if frames > 0:
                draw_firework()
                firework_win.after(200, lambda: animate_firework(frames-1))
            else:
                type_message()

        def play_celebration_melody():
            # Play a celebratory melody (non-blocking)
            import threading
            def melody():
                notes = [
                    (1047, 200), # C6
                    (1319, 200), # E6
                    (1568, 200), # G6
                    (1760, 200), # A6
                    (2093, 400), # C7
                    (1760, 200), # A6
                    (1568, 200), # G6
                    (1319, 200), # E6
                    (1047, 400), # C6
                ]
                for freq, dur in notes:
                    winsound.Beep(freq, dur)
            threading.Thread(target=melody, daemon=True).start()

        def type_message():
            message = 'YOU WON ! YIPPIE ! <3'
            def type_char(i=0):
                if i <= len(message):
                    msg_label.config(text=message[:i])
                    firework_win.after(120, lambda: type_char(i+1))
                else:
                    play_celebration_melody()
                    # Keep window open for 5 seconds after message
                    firework_win.after(5000, firework_win.destroy)
            type_char()

        animate_firework()
        # Removed grab_set() and wait_window() to keep main window responsive

    def make_move(self, idx):
        if self.board[idx] is None and not self.check_winner():
            self.board[idx] = self.player
            self.buttons[idx].config(text=self.player)
            # Play different sounds for each symbol
            if self.player == self.player_symbols[0]:
                winsound.Beep(784, 100)  # Player 1 sound
            else:
                winsound.Beep(523, 100)  # Player 2 sound
            winner = self.check_winner()
            if winner:
                self.scores[winner] += 1
                self.update_scoreboard()
                # Play a fun 5-note melody when a player wins
                melody = [
                    (880, 150),  # A5
                    (988, 150),  # B5
                    (1047, 150), # C6
                    (784, 150),  # G5
                    (1319, 250)  # E6 (longer)
                ]
                for freq, dur in melody:
                    winsound.Beep(freq, dur)
                    time.sleep(0.05)  # Short pause between notes
                if self.scores[winner] >= self.rounds_to_win:
                    self.show_firework_and_message(winner)
                    self.reset_game(full=True)
                else:
                    messagebox.showinfo("Round Over", f"Player {winner} wins the round!")
                    self.reset_board()
            elif all(self.board):
                messagebox.showinfo("Draw", "It's a draw!")
                self.reset_board()
            else:
                # Switch player
                self.player = self.player_symbols[1] if self.player == self.player_symbols[0] else self.player_symbols[0]

    def check_winner(self):
        wins = [
            [0,1,2], [3,4,5], [6,7,8], # rows
            [0,3,6], [1,4,7], [2,5,8], # cols
            [0,4,8], [2,4,6]           # diags
        ]
        for a, b, c in wins:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def update_scoreboard(self):
        p1, p2 = self.player_symbols
        self.score_label.config(text=f"Player {p1}: {self.scores[p1]}   Player {p2}: {self.scores[p2]}")

    def reset_board(self):
        self.board = [None] * 9
        for btn in self.buttons:
            btn.config(text="")
        self.player = self.player_symbols[0]

    def reset_game(self, full=False):
        if full:
            self.scores = {self.player_symbols[0]: 0, self.player_symbols[1]: 0}
            self.update_scoreboard()
        self.reset_board()

    def on_close(self):
        # Stop background music
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception:
            pass
        winsound.PlaySound(None, winsound.SND_PURGE)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    game = TicTacToe(root)
    # If the user cancelled the dialog, destroy the window and exit
    if not hasattr(game, 'player') or game.player is None:
        root.destroy()
    else:
        root.deiconify()
        root.mainloop()
