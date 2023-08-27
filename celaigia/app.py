#!/usr/bin/env python3
import os
import re
import tkinter as tk
from tkinter import messagebox, END, SINGLE, Frame, LEFT
import yt_dlp as ydl

from database import Database


def download_audio_from_youtube(url, output_folder, title="audio"):
    os.makedirs(output_folder, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio[ext=mp3]',
        'outtmpl': os.path.join(output_folder, title + '.%(ext)s'),
    }

    with ydl.YoutubeDL(ydl_opts) as ydl_instance:
        ydl_instance.download([url])

def clean_title(title):
    title = title.lower()
    title = re.sub(r'official (music )?video|lyrics?|audio|ft\.?|feat\.?|\[.*?\]|\(.*?\)|\{.*?\}|[-_,.!?;:]', ' ', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title

def search_youtube_sources(query, max_results=10):
    ydl_opts = {
        'format': 'bestaudio[ext=mp3]',
        'quiet': True,
        'verbose': False,
        'extract_flat': True,
        'default_search': 'ytsearch{}'.format(max_results)
    }

    with ydl.YoutubeDL(ydl_opts) as ydl_instance:
        search_results = ydl_instance.extract_info(f"ytsearch{max_results}:{query}", download=False)

        results_dict = {}
        for video in search_results['entries']:
            title = video['title']
            url = video['url']
            results_dict[title] = url

        return results_dict

class CelaigiaApp:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.root.title("Celaigia")

        # Main Search Frame
        self.search_frame = Frame(root)
        self.search_frame.pack(pady=20)

        # Search Query
        self.query_label = tk.Label(self.search_frame, text="Enter search query:")
        self.query_label.pack(side=LEFT, padx=5)

        self.query_entry = tk.Entry(self.search_frame, width=40)
        self.query_entry.pack(side=LEFT, padx=5)

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search)
        self.search_button.pack(side=LEFT, padx=5)

        # Listbox for Results
        self.results_listbox = tk.Listbox(root, height=10, width=50, selectmode=SINGLE, exportselection=False)
        self.results_listbox.bind('<<ListboxSelect>>', self.highlight_selection)
        self.results_listbox.pack(pady=20)

        self.download_button = tk.Button(root, text="Download Selected", command=self.download)
        self.download_button.pack(pady=10)

        # Configuration Frame
        self.config_frame = Frame(root)
        self.config_frame.pack(pady=20, side=LEFT, padx=10)

        # Num Search Results Configuration
        self.num_search_results_label = tk.Label(self.config_frame, text="Num Search Results:")
        self.num_search_results_label.pack(anchor='w')

        self.num_search_results_entry = tk.Entry(self.config_frame, width=20)
        self.num_search_results_entry.pack(pady=5)
        self.num_search_results_entry.insert(0, "2")  # default value

        # Output Folder Configuration
        self.output_folder_label = tk.Label(self.config_frame, text="Output Folder:")
        self.output_folder_label.pack(anchor='w')

        self.output_folder_entry = tk.Entry(self.config_frame, width=20)
        self.output_folder_entry.pack(pady=5)
        self.output_folder_entry.insert(0, "celaigia_downloads")  # default value

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def highlight_selection(self, event):
        self.results_listbox.itemconfig(tk.ACTIVE, {'bg':'green', 'fg':'white'})

    def search(self):
        # Clear previously highlighted items
        for i in self.results_listbox.get(0, tk.END):
            self.results_listbox.itemconfig(self.results_listbox.get(0, tk.END).index(i), bg='white', fg='black')

        self.query = self.query_entry.get()
        try:
            num_search_results = int(self.num_search_results_entry.get())
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid number for Num Search Results.")
            return

        self.titles = []
        self.urls = []

        try:
            results = search_youtube_sources(query, num_search_results)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return

        self.results_listbox.delete(0, END)
        for title, url in results.items():
            self.titles.append(title)
            self.urls.append(url)
            self.results_listbox.insert(tk.END, title)


    def download(self):
        selected_index = list(self.results_listbox.curselection())

        if not selected_index:
            messagebox.showinfo("Info", "No video selected for download.")
            return

        output_folder = self.output_folder_entry.get()

        for i in selected_index:
            url = self.urls[i]
            title = self.titles[i]
            title = clean_title(title)
            download_audio_from_youtube(url, output_folder, title)
            self.db.log_download(title, url, self.query)  # Log the download
        messagebox.showinfo("Info", "Download complete.")

    def on_closing(self):
        self.db.close()  # Close the database connection
        self.root.destroy()  # Destroy the main window

def main():
    root = tk.Tk()
    app = CelaigiaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
