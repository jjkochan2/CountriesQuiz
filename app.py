import tkinter as tk
from PIL import Image, ImageTk
import random
import json
import os

# SETTINGS
enable_country_range = True
country_range = [0, 10]

# Load country data
with open('countries.json', 'r', encoding='utf-8') as f:
    countries = json.load(f)

if enable_country_range:
    countries = {k: countries[k] for k in list(countries.keys())[country_range[0]:country_range[1]]}

flag_folder = 'Images'
font = "Consolas"

class FlagQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Flag Quiz")

        self.score = 0
        self.total_questions = 0

        self.all_country_codes = list(countries.keys())  # full list
        self.remaining_codes = self.all_country_codes.copy()

        self.flag_label = tk.Label(root)
        self.flag_label.pack(pady=20)

        self.entry = tk.Entry(root, font=(font, 14), width=40)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda event: self.check_answer())

        self.submit_btn = tk.Button(root, text="Submit", command=self.check_answer)
        self.submit_btn.pack(pady=5)

        self.reset_btn = tk.Button(root, text="Reset", command=self.reset_quiz)
        self.reset_btn.pack(pady=5)
        self.reset_btn.bind("<Return>", lambda event: self.reset_quiz())

        self.status_label = tk.Label(root, text="Score: 0/0", font=(font, 12))
        self.status_label.pack(pady=10)

        self.feedback_label = tk.Label(root, text="", font=(font, 12))
        self.feedback_label.pack(pady=10)

        self.next_question()

    def next_question(self):
        if not self.remaining_codes:
            self.flag_label.config(image='', text="🎉 Quiz complete!")
            self.entry.config(state='disabled')
            self.submit_btn.config(state='disabled')
            return

        self.correct_code = random.choice(self.remaining_codes)
        self.remaining_codes.remove(self.correct_code)
        self.correct_name = countries[self.correct_code]

        image_path = os.path.join(flag_folder, f"{self.correct_code.lower()}.png")
        try:
            img = Image.open(image_path)
            max_width, max_height = 1920 // 2, 1080 // 2
            original_width, original_height = img.size

            scale = min(max_width / original_width, max_height / original_height)
            new_size = (int(original_width * scale), int(original_height * scale))

            img = img.resize(new_size, Image.Resampling.LANCZOS)
            self.flag_img = ImageTk.PhotoImage(img)
            self.flag_label.config(image=self.flag_img, text="")
        except FileNotFoundError:
            self.flag_label.config(text=f"Missing image: {image_path}")
            return

        self.entry.config(state='normal')
        self.entry.delete(0, tk.END)
        self.feedback_label.config(text="")


    def check_answer(self):
        user_input = self.entry.get()
        correct_answer = self.correct_name

        if user_input == correct_answer:
            self.score += 1
            self.feedback_label.config(text="✅ Correct!", fg="green")
            self.total_questions += 1
            self.status_label.config(text=f"Score: {self.score}/{self.total_questions}")
            self.next_question()  # Instantly go to next question
        else:
            self.feedback_label.config(text=f"❌ Incorrect. It was {self.correct_name}.", fg="red")
            self.total_questions += 1
            self.status_label.config(text=f"Score: {self.score}/{self.total_questions}")
            self.root.after(1500, self.next_question)  # Wait 1.5 seconds before next

    def reset_quiz(self):
        self.score = 0
        self.total_questions = 0
        self.remaining_codes = self.all_country_codes.copy()
        self.status_label.config(text="Score: 0/0")
        self.feedback_label.config(text="")
        self.entry.config(state='normal')
        self.submit_btn.config(state='normal')
        self.next_question()

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1912x1000+0+0")
    app = FlagQuiz(root)
    root.mainloop()
