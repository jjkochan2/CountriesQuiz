import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import json
import os

# SETTINGS
enable_country_range = False
country_range = [0, 3]

# Load country data
with open('countries.json', 'r') as f:
    countries = json.load(f)

if enable_country_range:
    countries = {k: countries[k] for k in list(countries.keys())[country_range[0]:country_range[1]]}

print(len(countries))

country_codes = list(countries.keys())
flag_folder = 'Images'

class FlagQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Flag Quiz")

        self.score = 0
        self.total_questions = 0

        self.flag_label = tk.Label(root)
        self.flag_label.pack(pady=20)

        self.entry = tk.Entry(root, font=("Arial", 14), width=40)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda event: self.check_answer())

        self.submit_btn = tk.Button(root, text="Submit", command=self.check_answer)
        self.submit_btn.pack(pady=5)

        self.reset_btn = tk.Button(root, text="Reset", command=self.reset_quiz)
        self.reset_btn.pack(pady=5)


        self.status_label = tk.Label(root, text="Score: 0/0", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.feedback_label = tk.Label(root, text="", font=("Arial", 12))
        self.feedback_label.pack(pady=10)

        self.next_question()

    def next_question(self):
        self.correct_code = random.choice(country_codes)
        self.correct_name = countries[self.correct_code]

        # Load and display image
        image_path = os.path.join(flag_folder, f"{self.correct_code.lower()}.png")
        try:
            img = Image.open(image_path).resize((200, 120), Image.Resampling.LANCZOS)
            self.flag_img = ImageTk.PhotoImage(img)
            self.flag_label.config(image=self.flag_img, text="")
        except FileNotFoundError:
            self.flag_label.config(text=f"Missing image: {image_path}")
            return

        # Reset entry and feedback
        self.entry.delete(0, tk.END)
        self.feedback_label.config(text="")

    def check_answer(self):
        user_input = self.entry.get()#.strip().lower()
        correct_answer = self.correct_name#.lower()

        if user_input == correct_answer:
            self.score += 1
            self.feedback_label.config(text="✅ Correct!", fg="green")
        else:
            self.feedback_label.config(text=f"❌ Incorrect. It was {self.correct_name}.", fg="red")

        self.total_questions += 1
        self.status_label.config(text=f"Score: {self.score}/{self.total_questions}")

        # Wait briefly before moving on
        self.root.after(1500, self.next_question)

    def reset_quiz(self):
        self.score = 0
        self.total_questions = 0
        self.status_label.config(text="Score: 0/0")
        self.feedback_label.config(text="")
        self.next_question()

if __name__ == '__main__':
    root = tk.Tk()
    app = FlagQuiz(root)
    root.mainloop()
