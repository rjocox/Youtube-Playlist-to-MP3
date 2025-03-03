import tkinter as tk
from ui import YoutubeDownloaderApp

def main():
    root = tk.Tk()
    root.iconbitmap("youtube.ico")
    app = YoutubeDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()