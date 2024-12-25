import tkinter as tk
from tkinter import messagebox
import random
import time


class MemoryGame:
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the Memory Game.

        Args:
            root (tk.Tk): The root window for the game.
        """
        self.root = root
        self.root.title("Memory Puzzle Game")
        self.root.geometry("800x600")  # Increase the size of the window

        # Styles
        self.style = {
            "button": {"font": ("Helvetica", 14), "width": 10, "height": 5},
            "label": {"font": ("Helvetica", 16, "bold")},
            "timer": {"font": ("Helvetica", 16, "bold"), "fg": "red"}
        }
        
        # Difficulty settings
        self.difficulty = tk.StringVar(value="Easy")  # Default difficulty
        self.difficulty_options = {"Easy": (4, 4), "Medium": (6, 6), "Hard": (8, 8)}
        
        self.create_difficulty_selection()
        self.cards = []
        self.buttons = []
        self.flipped = []  # Store flipped card indexes
        self.start_time = 0

    def create_difficulty_selection(self) -> None:
        """Create difficulty selection buttons."""
        label = tk.Label(self.root, text="Select Difficulty Level:", **self.style["label"])
        label.grid(row=0, column=0, columnspan=3, pady=10)

        for idx, (level, (rows, cols)) in enumerate(self.difficulty_options.items()):
            button = tk.Button(self.root, text=level, command=lambda l=level: self.start_game(l), **self.style["button"])
            button.grid(row=1, column=idx, padx=10)

    def start_game(self, level: str) -> None:
        """Start the game with the selected difficulty level."""
        rows, cols = self.difficulty_options[level]
        self.cards = list(range(1, (rows * cols // 2) + 1)) * 2
        random.shuffle(self.cards)

        # Reset game state
        self.buttons = []
        self.flipped = []
        self.start_time = time.time()

        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_widgets(rows, cols)
        self.check_time()

    def create_widgets(self, rows: int, cols: int) -> None:
        """Create the buttons and layout for the game."""
        for row_index in range(rows):
            row = []
            for column_index in range(cols):
                button = tk.Button(
                    self.root,
                    text='',
                    **self.style["button"],
                    command=lambda i=row_index, j=column_index: self.reveal_card(i, j)
                )
                button.grid(row=row_index + 2, column=column_index, padx=5, pady=5)  # Offset by 2 for difficulty selection
                row.append(button)
            self.buttons.append(row)

        # Timer label
        self.timer_label = tk.Label(self.root, text="Time Remaining: 60s", **self.style["timer"])
        self.timer_label.grid(row=rows + 2, column=0, columnspan=cols, pady=10)

    def reveal_card(self, row: int, column: int) -> None:
        """Reveal the selected card at the specified row and column."""
        if len(self.flipped) < 2 and self.buttons[row][column]['text'] == '' and self.buttons[row][column]['state'] != 'disabled':
            self.buttons[row][column].config(text=self.cards[row * len(self.buttons[0]) + column], state='disabled')  # Reveal card
            self.flipped.append((row, column))
            if len(self.flipped) == 2:
                self.root.after(1000, self.check_match)

    def check_match(self) -> None:
        """Check if two flipped cards match and update their state accordingly."""
        first_row, first_column = self.flipped[0]
        second_row, second_column = self.flipped[1]
        
        if self.cards[first_row * len(self.buttons[0]) + first_column] == self.cards[second_row * len(self.buttons[0]) + second_column]:
            self.buttons[first_row][first_column].config(bg='green')
            self.buttons[second_row][second_column].config(bg='green')
        else:
            self.buttons[first_row][first_column].config(text='', state='normal')
            self.buttons[second_row][second_column].config(text='', state='normal')

        self.flipped = []

        if all(button['bg'] == 'green' for row in self.buttons for button in row):
            messagebox.showinfo("Congratulations!", "You won the game! Starting next stage...")
            self.start_game_next_stage()

    def start_game_next_stage(self) -> None:
        """Start the next stage of the game."""
        current_level = self.difficulty.get()
        rows, cols = self.difficulty_options[current_level]
        self.difficulty.set(current_level)
        self.start_game(current_level)

    def check_time(self) -> None:
        """Check if the time is up and update the timer label."""
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = 60 - elapsed_time
        self.timer_label.config(text=f"Time Remaining: {remaining_time}s")

        if remaining_time <= 0:
            for row in self.buttons:
                for button in row:
                    button.config(state='disabled')
            messagebox.showinfo("Game Over", "Time's up! You lost!")
            self.create_difficulty_selection()  # Show difficulty selection again
        else:
            self.root.after(1000, self.check_time)


if __name__ == "__main__": 
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
