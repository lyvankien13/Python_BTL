import tkinter as tk
from tkinter import messagebox
import random


class HangmanGame:
    def __init__(self, word_file='words.txt'):
        self.word_file = word_file
        self.max_wrong = 6
        self.reset_game()

    def load_word(self):
        try:
            with open(self.word_file, 'r') as f:
                words = [line.strip().upper() for line in f if line.strip()]
            return random.choice(words)
        except FileNotFoundError:
            messagebox.showerror("Lỗi", f"Không tìm thấy file '{self.word_file}'")
            return None

    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            return
        self.guessed_letters.add(letter)
        if letter not in self.secret_word:
            self.wrong_guesses += 1

    def get_display_word(self):
        return ' '.join([c if c in self.guessed_letters else '_' for c in self.secret_word])

    def is_won(self):
        return all(c in self.guessed_letters for c in self.secret_word)

    def is_lost(self):
        return self.wrong_guesses >= self.max_wrong

    def reset_game(self):
        self.secret_word = self.load_word()
        self.guessed_letters = set()
        self.wrong_guesses = 0


class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman")
        self.game = HangmanGame()
        if not self.game.secret_word:
            root.destroy()
            return
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Hangman", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=5)

        self.canvas = tk.Canvas(self.root, width=200, height=220, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(pady=10)

        self.word_label = tk.Label(self.root, text="", font=("Courier", 24))
        self.word_label.pack(pady=5)

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=5)

        self.entry = tk.Entry(input_frame, font=("Helvetica", 16), width=5, justify="center")
        self.entry.grid(row=0, column=0, padx=5)
        self.entry.bind("<KeyRelease>", self.auto_handle_guess)

        self.reset_button = tk.Button(input_frame, text="Chơi lại", font=("Helvetica", 12), command=self.reset_game)
        self.reset_button.grid(row=0, column=1)

        self.info_label = tk.Label(self.root, text="Số lần đoán sai: 0", font=("Helvetica", 12))
        self.info_label.pack(pady=5)

        self.entry.focus_set()  # Tự focus vào ô nhập

    def auto_handle_guess(self, event):
        letter = self.entry.get().strip().upper()
        if len(letter) == 1 and letter.isalpha():
            self.entry.delete(0, tk.END)
            self.handle_guess_with_letter(letter)

    def handle_guess_with_letter(self, letter):
        if letter in self.game.guessed_letters:
            return

        self.game.guess_letter(letter)
        self.update_display()

        if self.game.is_won():
            messagebox.showinfo("Chiến thắng", "Bạn đã thắng!")
            self.disable_input()
        elif self.game.is_lost():
            messagebox.showinfo("Thua cuộc", f"Bạn đã thua! Từ là: {self.game.secret_word}")
            self.disable_input()

    def update_display(self):
        self.word_label.config(text=self.game.get_display_word())
        self.info_label.config(text=f"Số lần đoán sai: {self.game.wrong_guesses}")
        self.draw_hangman()

    def draw_hangman(self):
        self.canvas.delete("all")
        self.canvas.create_line(20, 200, 180, 200)  # chân
        self.canvas.create_line(50, 200, 50, 20)    # cột dọc
        self.canvas.create_line(50, 20, 120, 20)    # ngang trên
        self.canvas.create_line(120, 20, 120, 40)   # móc

        if self.game.wrong_guesses >= 1:
            self.canvas.create_oval(100, 40, 140, 80)  # đầu
        if self.game.wrong_guesses >= 2:
            self.canvas.create_line(120, 80, 120, 130)  # thân
        if self.game.wrong_guesses >= 3:
            self.canvas.create_line(120, 100, 90, 110)  # tay trái
        if self.game.wrong_guesses >= 4:
            self.canvas.create_line(120, 100, 150, 110)  # tay phải
        if self.game.wrong_guesses >= 5:
            self.canvas.create_line(120, 130, 90, 160)  # chân trái
        if self.game.wrong_guesses >= 6:
            self.canvas.create_line(120, 130, 150, 160)  # chân phải

    def disable_input(self):
        self.entry.config(state='disabled')

    def reset_game(self):
        self.game.reset_game()
        if not self.game.secret_word:
            self.root.destroy()
            return
        self.entry.config(state='normal')
        self.update_display()
        self.entry.focus_set()  # Tự focus lại sau khi chơi lại


if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()
