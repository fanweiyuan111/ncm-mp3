import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pydub import AudioSegment
import ncmdump
import threading
import time

def convert_ncm_to_mp3(ncm_file, mp3_file, progress_var):
    decrypted_wav_file = 'decrypted.wav'
    try:
        # Simulate a long-running task
        for i in range(10):
            time.sleep(0.1)  # Simulate work
            progress_var.set(i * 10)
            root.update_idletasks()

        ncmdump.decrypt(ncm_file, decrypted_wav_file)
        audio = AudioSegment.from_wav(decrypted_wav_file)
        audio.export(mp3_file, format='mp3')
        os.remove(decrypted_wav_file)
        progress_var.set(100)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def start_conversion():
    ncm_file = ncm_file_var.get()
    mp3_file = mp3_file_var.get()
    if not ncm_file or not mp3_file:
        messagebox.showwarning("Warning", "Please select both input NCM file and output MP3 file path.")
        return

    # Disable the start button to prevent multiple clicks
    convert_button.config(state=tk.DISABLED)
    progress_var.set(0)
    progress_bar.start()

    def run_conversion():
        success = convert_ncm_to_mp3(ncm_file, mp3_file, progress_var)
        progress_bar.stop()
        convert_button.config(state=tk.NORMAL)
        if success:
            messagebox.showinfo("Success", "Conversion completed successfully.")
        else:
            messagebox.showerror("Error", "Conversion failed. Check the logs for details.")

    # Run the conversion in a separate thread to keep the GUI responsive
    threading.Thread(target=run_conversion).start()

# GUI setup
root = tk.Tk()
root.title("NCM to MP3 Converter")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ncm_file_var = tk.StringVar()
mp3_file_var = tk.StringVar()
progress_var = tk.IntVar()

ttk.Label(frame, text="NCM File:").grid(row=0, column=0, sticky=tk.W)
ttk.Entry(frame, textvariable=ncm_file_var, width=50).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(frame, text="Browse", command=select_ncm_file).grid(row=0, column=2, padx=5, pady=5)

ttk.Label(frame, text="Output MP3 File:").grid(row=1, column=0, sticky=tk.W)
ttk.Entry(frame, textvariable=mp3_file_var, width=50).grid(row=1, column=1, padx=5, pady=5)
ttk.Button(frame, text="Browse", command=select_output_file).grid(row=1, column=2, padx=5, pady=5)

ttk.Button(frame, text="Convert", command=start_conversion).grid(row=2, column=1, pady=10)

# Progress bar
ttk.Label(frame, text="Progress:").grid(row=3, column=0, sticky=tk.W, pady=5)
progress_bar = ttk.Progressbar(frame, length=300, mode='determinate', variable=progress_var)
progress_bar.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

root.mainloop()
