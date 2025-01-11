import tkinter as tk
from app_interface import SentimentApp

def main():
    
    root = tk.Tk()
    app = SentimentApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()