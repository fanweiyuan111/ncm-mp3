import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pydub import AudioSegment
import ncmdump

def convert_ncm_to_mp3(ncm_file, mp3_file):
    decrypted_wav_file = 'decrypted.wav'
    try:
        ncmdump.decrypt(ncm_file, decrypted_wav_file)
        audio = AudioSegment.from_wav(decrypted_wav_file)
        audio.export(mp3_file, format='mp3')
        os.remove(decrypted_wav_file)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def select_ncm_file():
    file_path = filedialog.askopenfilename(filetypes=[("NCM Files", "*.ncm")])
    if file_path:
        ncm_file_var.set(file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
    if file_path:
        mp3_file_var.set(file_path)

def start_conversion():
    ncm_file = ncm_file_var.get()
    mp3_file = mp3_file_var.get()
    if not ncm_file or not mp3_file:
        messagebox.showwarning("Warning", "Please select both input NCM file and output MP3 file path.")
        return

    if convert_ncm_to_mp3(ncm_file, mp3_file):
        messagebox.showinfo("Success", "Conversion completed successfully.")
    else:
        messagebox.showerror("Error", "Conversion failed. Check the logs for details.")

# GUI setup
root = tk.Tk()
root.title("NCM to MP3 Converter")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ncm_file_var = tk.StringVar()
mp3_file_var = tk.StringVar()

ttk.Label(frame, text="NCM File:").grid(row=0, column=0, sticky=tk.W)
ttk.Entry(frame, textvariable=ncm_file_var, width=50).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(frame, text="Browse", command=select_ncm_file).grid(row=0, column=2, padx=5, pady=5)

ttk.Label(frame, text="Output MP3 File:").grid(row=1, column=0, sticky=tk.W)
ttk.Entry(frame, textvariable=mp3_file_var, width=50).grid(row=1, column=1, padx=5, pady=5)
ttk.Button(frame, text="Browse", command=select_output_file).grid(row=1, column=2, padx=5, pady=5)

ttk.Button(frame, text="Convert", command=start_conversion).grid(row=2, column=1, pady=10)

root.mainloop()
