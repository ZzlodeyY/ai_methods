import tkinter as tk
from tkinter import messagebox
from text_generator import load_tokenizer_and_model, generate_text
import config

class TextGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генерация текста с использованием ruGPT-3.x")
        self.root.geometry("800x600")  

        
        self.tokenizer, self.model = load_tokenizer_and_model()

       
        self.prompt_label = tk.Label(root, text="Введите начальный текст:")
        self.prompt_label.pack()
        self.prompt_entry = tk.Text(root, wrap=tk.WORD, height=10, width=60)  
        self.prompt_entry.pack()

        
        self.add_parameter_fields()

        
        self.generate_button = tk.Button(root, text="Сгенерировать текст", command=self.generate_text)
        self.generate_button.pack()

        
        self.result_text = tk.Text(root, wrap=tk.WORD, height=15, width=80)
        self.result_text.pack()


    def add_parameter_fields(self):
        self.max_length_label = tk.Label(self.root, text="Максимальная длина:")
        self.max_length_label.pack()
        self.max_length_entry = tk.Entry(self.root, width=10)
        self.max_length_entry.insert(0, str(config.DEFAULT_MAX_LENGTH))
        self.max_length_entry.pack()

        self.repetition_penalty_label = tk.Label(self.root, text="Штраф за повторение:")
        self.repetition_penalty_label.pack()
        self.repetition_penalty_entry = tk.Entry(self.root, width=10)
        self.repetition_penalty_entry.insert(0, str(config.DEFAULT_REPETITION_PENALTY))
        self.repetition_penalty_entry.pack()

        self.top_k_label = tk.Label(self.root, text="Top-k:")
        self.top_k_label.pack()
        self.top_k_entry = tk.Entry(self.root, width=10)
        self.top_k_entry.insert(0, str(config.DEFAULT_TOP_K))
        self.top_k_entry.pack()

        self.top_p_label = tk.Label(self.root, text="Top-p:")
        self.top_p_label.pack()
        self.top_p_entry = tk.Entry(self.root, width=10)
        self.top_p_entry.insert(0, str(config.DEFAULT_TOP_P))
        self.top_p_entry.pack()

        self.temperature_label = tk.Label(self.root, text="Температура:")
        self.temperature_label.pack()
        self.temperature_entry = tk.Entry(self.root, width=10)
        self.temperature_entry.insert(0, str(config.DEFAULT_TEMPERATURE))
        self.temperature_entry.pack()

        self.num_beams_label = tk.Label(self.root, text="Количество лучей (num_beams):")
        self.num_beams_label.pack()
        self.num_beams_entry = tk.Entry(self.root, width=10)
        self.num_beams_entry.insert(0, str(config.DEFAULT_NUM_BEAMS))
        self.num_beams_entry.pack()

        self.no_repeat_ngram_size_label = tk.Label(self.root, text="Запрет на повторение n-грамм:")
        self.no_repeat_ngram_size_label.pack()
        self.no_repeat_ngram_size_entry = tk.Entry(self.root, width=10)
        self.no_repeat_ngram_size_entry.insert(0, str(config.DEFAULT_NO_REPEAT_NGRAM_SIZE))
        self.no_repeat_ngram_size_entry.pack()

    def generate_text(self):
        prompt = self.prompt_entry.get("1.0", "end").strip()

        try:
            
            max_length = int(self.max_length_entry.get())
            repetition_penalty = float(self.repetition_penalty_entry.get())
            top_k = int(self.top_k_entry.get())
            top_p = float(self.top_p_entry.get())
            temperature = float(self.temperature_entry.get())
            num_beams = int(self.num_beams_entry.get()) if self.num_beams_entry.get() else None
            no_repeat_ngram_size = int(self.no_repeat_ngram_size_entry.get())

            generated_text = generate_text(
                self.model, self.tokenizer, prompt,
                max_length=max_length,
                repetition_penalty=repetition_penalty,
                top_k=top_k, top_p=top_p,
                temperature=temperature,
                num_beams=num_beams,
                no_repeat_ngram_size=no_repeat_ngram_size
            )

            
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, generated_text)

        except ValueError as ve:
            messagebox.showerror("Ошибка", f"Неверный формат параметров: {ve}")

