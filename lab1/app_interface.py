# app_interface.py
import tkinter as tk
from tkinter import messagebox, scrolledtext
from typing import Tuple, Dict, Optional
from api1 import API1Client
from api2 import API2Client

class SentimentAnalyzer:
    
    def __init__(self):
        self.api1_client = API1Client()
        self.api2_client = API2Client()

    def analyze_text(self, text: str) -> Tuple[Optional[Dict], Optional[Dict]]:
        """Analyze text using both APIs."""
        result_api1 = self.api1_client.analyze_sentiment(text)
        result_api2 = self.api2_client.analyze_sentiment(text)
        return result_api1, result_api2

class SentimentApp:
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Text Sentiment Analysis")
        self._init_ui()
        self.analyzer = SentimentAnalyzer()

    def _init_ui(self):
        self.lbl_input = tk.Label(self.root, text="Enter text for analysis:")
        self.lbl_input.pack(pady=5)

        self.txt_input = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, width=60, height=10
        )
        self.txt_input.pack(padx=10, pady=5)

        self.btn_analyze = tk.Button(
            self.root,
            text="Analyze",
            command=self.process_and_display_results
        )
        self.btn_analyze.pack(pady=10)

        self.lbl_output = tk.Label(self.root, text="Results:")
        self.lbl_output.pack(pady=5)

        self.txt_output = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, width=60, height=10
        )
        self.txt_output.pack(padx=10, pady=5)

    def process_and_display_results(self):
        text = self.txt_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text for analysis.")
            return

        try:
            result_api1, result_api2 = self.analyzer.analyze_text(text)

            result_message = "Sentiment Analysis Results:\n\n"
            
            if result_api1:
                result_message += "Text-Analysis API:\n"
                result_message += f"Negative: {result_api1['outputs'].get('negative')}\n"
                result_message += f"Neutral: {result_api1['outputs'].get('neutral')}\n"
                result_message += f"Positive: {result_api1['outputs'].get('positive')}\n\n"
            else:
                result_message += "Text-Analysis API: Failed to get results.\n\n"

            if result_api2:
                result_message += "Comprehend-It API:\n"
                result_message += f"Sentiment: {result_api2['sentiment']}\n"
                result_message += f"Confidence: {float(result_api2['confidence']) * 100:.2f}%\n"
            else:
                result_message += "Comprehend-It API: Failed to get results.\n"

            self.txt_output.delete("1.0", tk.END)
            self.txt_output.insert(tk.END, result_message)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.txt_output.delete("1.0", tk.END)
            self.txt_output.insert(tk.END, "Error occurred during analysis.")