import pyautogui
import cv2
import numpy as np
from tkinter import Tk, Button, filedialog, messagebox, Frame, Label
from PIL import ImageGrab, ImageTk
import threading

class ScreenRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Vision Record 📹")
        self.recording = False
        self.out = None

        self.main_frame = Frame(root, bg="#1E1E1E", padx=20, pady=20)
        self.main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        self.title_label = Label(self.main_frame, text="Vision Record 📹", font=("Segoe UI", 28, "bold"), bg="#1E1E1E", fg="#F5F5F5")
        self.title_label.pack(pady=20)
        
        self.button_frame = Frame(self.main_frame, bg="#1E1E1E")
        self.button_frame.pack(pady=10)

        self.start_button = Button(self.button_frame, text="Start Recording ▶️", command=self.start_recording, bg="#4CAF50", fg="white", font=("Segoe UI", 16), width=18, height=2, relief="flat", padx=10, pady=5, borderwidth=0, activebackground="#45a049", cursor="hand2")
        self.start_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.stop_button = Button(self.button_frame, text="Stop Recording ⏹️", command=self.stop_recording, state="disabled", bg="#f44336", fg="white", font=("Segoe UI", 16), width=18, height=2, relief="flat", padx=10, pady=5, borderwidth=0, activebackground="#d32f2f", cursor="hand2")
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        self.start_button.bind("<Enter>", self.on_hover_enter)
        self.start_button.bind("<Leave>", self.on_hover_leave)
        self.stop_button.bind("<Enter>", self.on_hover_enter)
        self.stop_button.bind("<Leave>", self.on_hover_leave)

        self.file_path = ""
        self.recording_thread = None
        self.stop_event = threading.Event()

    def on_hover_enter(self, event):
        event.widget.config(bg="#FFC107") 

    def on_hover_leave(self, event):
        if event.widget == self.start_button:
            event.widget.config(bg="#4CAF50") 
        elif event.widget == self.stop_button:
            event.widget.config(bg="#f44336") 

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.stop_event.clear()
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.file_path = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi")])
            if not self.file_path:
                messagebox.showerror("Error", "No file path selected.")
                self.recording = False
                self.start_button.config(state="normal")
                self.stop_button.config(state="disabled")
                return

            screen_size = pyautogui.size()
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            self.out = cv2.VideoWriter(self.file_path, fourcc, 20.0, (screen_size.width, screen_size.height))

            self.recording_thread = threading.Thread(target=self.record_screen)
            self.recording_thread.start()

    def record_screen(self):
        while not self.stop_event.is_set():
            img = ImageGrab.grab()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            cursor_pos = pyautogui.position()
            cursor_size = 32
            cursor_color = (0, 255, 0)  
            
            x, y = cursor_pos
            x -= cursor_size // 2
            y -= cursor_size // 2

            if 0 <= x < frame.shape[1] and 0 <= y < frame.shape[0]:
                cv2.circle(frame, (x + cursor_size // 2, y + cursor_size // 2), cursor_size // 2, cursor_color, -1)

            self.out.write(frame)

        self.out.release()
        cv2.destroyAllWindows()
        self.recording = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        messagebox.showinfo("Info", "Recording stopped and saved successfully.")

    def stop_recording(self):
        if self.recording:
            self.stop_event.set()
            self.recording_thread.join()  
            self.out.release()
            cv2.destroyAllWindows()
            self.recording = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            messagebox.showinfo("Info", "Recording stopped and saved successfully.")
        else:
            messagebox.showwarning("Warning", "Recording is not currently running.")

if __name__ == "__main__":
    root = Tk()
    root.geometry("700x350")  
    root.configure(bg="#1E1E1E")  
    app = ScreenRecorder(root)
    root.mainloop()
