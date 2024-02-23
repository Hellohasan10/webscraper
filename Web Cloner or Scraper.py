import tkinter as tk
from tkinter import Toplevel, messagebox, filedialog, Label, Entry, Button, Radiobutton, StringVar, ttk
import requests
from bs4 import BeautifulSoup
import threading 

# Define colors and styles
bg_color = "#333333"
text_color = "#FFFFFF"
button_color = "#1C1C1C"
entry_bg_color = "#474747"
entry_fg_color = "#FFFFFF"
frame_padding = 20

def sanitize_filename(filename):
    return ''.join(char for char in filename if char.isalnum() or char in (' ', '.', '_')).rstrip()

def scrape_website(url, save_as_text, loading_screen):
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        text_content = soup.get_text() if save_as_text else soup.prettify()

        file_extension = 'txt' if save_as_text else 'html'
        filename = f"website.{file_extension}"
        with open(filename, "w", encoding='utf-8') as file:
            file.write(text_content)

        loading_screen.destroy()
        show_save_file_screen(filename)

    except Exception as e:
        loading_screen.destroy()
        messagebox.showerror("Error", f"An error occurred: {e}")

def show_loading_screen(url, save_as_text):
    loading_screen = Toplevel(root, bg=bg_color)
    loading_screen.title("Loading")
    loading_screen.geometry("300x150")
    Label(loading_screen, text="Getting into the URL...", bg=bg_color, fg=text_color, font=("Helvetica", 12)).pack(pady=50)
    loading_screen.grab_set()
    threading.Thread(target=scrape_website, args=(url, save_as_text, loading_screen), daemon=True).start()

def show_save_file_screen(filename):
    save_screen = Toplevel(root, bg=bg_color)
    save_screen.title("Save File")
    save_screen.geometry("300x150")

    Label(save_screen, text="The scraping is complete!", bg=bg_color, fg=text_color, font=("Helvetica", 12)).pack(pady=20)
    file_entry = Entry(save_screen, width=50, bg=entry_bg_color, fg=entry_fg_color)
    file_entry.insert(0, filename)
    file_entry.pack(pady=10)

    Button(save_screen, text="Save As...", bg=button_color, fg=text_color, command=lambda: save_file(filename, file_entry.get(), save_screen)).pack(pady=10)

def save_file(original_filename, new_filename, save_screen):
    file = filedialog.asksaveasfilename(defaultextension=".*",
                                        initialfile=new_filename,
                                        filetypes=[("HTML Files", "*.html"), ("Text Files", "*.txt"), ("All Files", "*.*")])
    if file:
        with open(original_filename, 'r', encoding='utf-8') as f:
            file_content = f.read()
        with open(file, 'w', encoding='utf-8') as f:
            f.write(file_content)
        save_screen.destroy()
        messagebox.showinfo("Success", "File saved successfully!")

def start_scraping():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL to scrape.")
        return
    save_as_text = output_format_var.get() == "TEXT"
    show_loading_screen(url, save_as_text)

root = tk.Tk()
root.title("Website Cloner")
root.configure(bg=bg_color)
root.geometry("400x200")

Label(root, text="Website Cloner", bg=bg_color, fg=text_color, font=("Helvetica", 18)).pack(pady=10)
Label(root, text="Enter URL to get its HTML", bg=bg_color, fg=text_color).pack()

url_entry = Entry(root, width=50, bg=entry_bg_color, fg=entry_fg_color)
url_entry.pack(pady=10)

output_format_var = StringVar(value="HTML")
Radiobutton(root, text="HTML", variable=output_format_var, value="HTML", bg=bg_color, fg=text_color, selectcolor=button_color).pack(side=tk.LEFT, padx=10)
Radiobutton(root, text="TEXT", variable=output_format_var, value="TEXT", bg=bg_color, fg=text_color, selectcolor=button_color).pack(side=tk.LEFT)

Button(root, text="Start Scraping", bg=button_color, fg=text_color, command=start_scraping).pack(pady=10)

root.mainloop()