import tkinter as tk
from tkinter import ttk, filedialog
from logic import fetch_playlist, download_videos

class YoutubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Playlist Downloader")
        self.root.geometry("1000x800")
        self.root.configure(bg="#1e1e1e")

        self.playlist_videos = []

        # Custom style for ttk widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', background="#1e1e1e", foreground="#ffffff", font=('Helvetica', 12))
        self.style.configure('TEntry', fieldbackground="#333333", foreground="#ffffff", font=('Helvetica', 12), borderwidth=2, relief="groove", padding=8, bordercolor="#444444") # More padding
        self.style.configure('TButton', background="#444444", foreground="#ffffff", font=('Helvetica', 12), borderwidth=3, relief="groove", padding=12, bordercolor="#444444", borderradius=10) # More padding and borderradius
        self.style.map('TButton', background=[('active', '#666666')])
        self.style.configure('TFrame', background="#1e1e1e")

        # URL Entry
        self.url_label = ttk.Label(root, text="Enter YouTube Playlist URL:")
        self.url_label.pack(pady=5)
        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.pack(pady=5)

        # Filepath Selection
        self.filepath_label = ttk.Label(root, text="Select Save Location:")
        self.filepath_label.pack(pady=5)
        self.filepath_entry = ttk.Entry(root, width=50)
        self.filepath_entry.pack(pady=5)
        self.browse_button = ttk.Button(root, text="Browse", command=self.browse_filepath)
        self.browse_button.pack(pady=5)

        # Fetch Playlist Button
        self.fetch_button = ttk.Button(root, text="Fetch Playlist", command=self.fetch_playlist)
        self.fetch_button.pack(pady=5)

        # Playlist Items Listbox with Scrollbar
        self.playlist_label = ttk.Label(root, text="Playlist Items:")
        self.playlist_label.pack(pady=5)

        self.listbox_frame = ttk.Frame(root)
        self.listbox_frame.pack(pady=5)

        self.scrollbar = ttk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL)
        self.playlist_listbox = tk.Listbox(self.listbox_frame, selectmode=tk.MULTIPLE, width=150, height=30,
                                           yscrollcommand=self.scrollbar.set, bg="#333333", fg="#ffffff",
                                           font=('Helvetica', 12), borderwidth=0, relief="flat", highlightthickness=0)
        self.scrollbar.config(command=self.playlist_listbox.yview)

        self.playlist_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Select & Deselect Buttons
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(pady=5)

        self.select_all_button = ttk.Button(self.button_frame, text="Select All", command=self.select_all)
        self.select_all_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.deselect_all_button = ttk.Button(self.button_frame, text="Deselect All", command=self.deselect_all)
        self.deselect_all_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Download Button
        self.download_button = ttk.Button(root, text="Download Selected", command=self.download_selected)
        self.download_button.pack(pady=10)

        # Status Label
        self.status_label = ttk.Label(root, text="", foreground="#00ff00", background="#1e1e1e", font=('Helvetica', 12))
        self.status_label.pack(pady=10)

    def browse_filepath(self):
        """Open a dialog to select the save directory."""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.filepath_entry.delete(0, tk.END)
            self.filepath_entry.insert(0, folder_selected)

    def fetch_playlist(self):
        """Fetch and display the playlist."""
        url = self.url_entry.get().strip()
        self.playlist_listbox.delete(0, tk.END)
        self.playlist_videos = fetch_playlist(url)

        for title, _ in self.playlist_videos:
            self.playlist_listbox.insert(tk.END, title)

    def select_all(self):
        self.playlist_listbox.selection_set(0, tk.END)

    def deselect_all(self):
        self.playlist_listbox.selection_clear(0, tk.END)

    def download_selected(self):
        selected_indices = self.playlist_listbox.curselection()
        selected_videos = [self.playlist_videos[i] for i in selected_indices]
        save_path = self.filepath_entry.get().strip()

        download_videos(selected_videos, save_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloaderApp(root)
    root.mainloop()