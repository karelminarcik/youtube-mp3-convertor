import os
import tempfile
from pytube import YouTube
from moviepy.editor import *
from tkinter import *
from tkinter import filedialog, messagebox

# Function to download YouTube video and convert to MP3
def download_and_convert_to_mp3(url):
    try:
        # Create a YouTube object with the video URL
        yt = YouTube(url)

        # Filter streams to get the ones with progressive video and in mp4 format
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()

        # Generate temporary file path
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, 'temp.mp4')

        # Download the video
        video_stream.download(output_path=temp_dir, filename='temp.mp4')

        # Convert audio to MP3
        clip = AudioFileClip(temp_file_path)

        # Generating unique filename if file already exists
        mp3_filename = file_name_entry.get() + '.mp3'
        counter = 1
        while os.path.exists(mp3_filename):
            mp3_filename = f"{file_name_entry.get()}_{counter}.mp3"
            counter += 1

        # Save MP3 file to chosen directory
        mp3_file_path = os.path.join(output_directory.get(), mp3_filename)
        clip.write_audiofile(mp3_file_path)
        clip.close()

        messagebox.showinfo("Success", f"Conversion successful! MP3 file saved as '{mp3_file_path}'")

        # Clear entry fields
        clear_entries()
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def browse_directory():
    selected_directory = filedialog.askdirectory()
    output_directory.set(selected_directory)

def clear_entries():
    url_entry.delete(0, END)
    file_name_entry.delete(0, END)
    output_directory_entry.delete(0, END)

tk = Tk()
tk.geometry("440x290")  # Adjusted window size to accommodate the margin
tk.title("YouTube to MP3 Converter")

# Set background color to black
tk.configure(bg="black")

# Adding padding/margin around the perimeter of the window
tk.grid_rowconfigure(0, pad=10)
tk.grid_rowconfigure(5, pad=10)
tk.grid_columnconfigure(0, pad=20)
tk.grid_columnconfigure(2, pad=20)

general_label = Label(text="YouTube to MP3 Converter", fg="white", bg="black",font=("Arial", 12, "bold"),)
general_label.grid(row=1, column=1)

url_label = Label(text="Enter the YouTube URL: ", fg="white", bg="black")
url_label.grid(row=2, column=0)

url_entry = Entry(width=30)
url_entry.grid(row=2, column=1, pady=5)

file_name_label = Label(text="Name of the file", fg="white", bg="black")
file_name_label.grid(row=3, column=0)

file_name_entry = Entry(width=30)
file_name_entry.grid(row=3, column=1, pady=5)

output_directory_label = Label(text="Save MP3 to: ", fg="white", bg="black")
output_directory_label.grid(row=4, column=0)

output_directory = StringVar()
output_directory_entry = Entry(width=30, textvariable=output_directory)
output_directory_entry.grid(row=4, column=1, pady=5)

browse_button = Button(text="Browse", command=browse_directory, fg="white", bg="grey")
browse_button.grid(row=4, column=2, padx=5)

convert_button = Button(text="Convert", command=lambda: download_and_convert_to_mp3(url_entry.get()), fg="white", bg="blue",padx=10,
    pady=5,font=("Arial", 12, "bold"), bd=3)  # Set font weight to bold)
convert_button.grid(row=5, column=1, pady=10)


tk.mainloop()
