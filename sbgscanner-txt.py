import os,sys
import re,colorama
from colorama import Fore, Style
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser

# Init window
window_width = 800
window_height = 600
window = tk.Tk()
window.title('SBG File Scanner')


def load_file_content():
    file_text.delete("1.0", tk.END)
    try:
        with open("sbgfilesdesc.txt", "r") as file:
            content = file.read()
            file_text.insert(tk.END, content)
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found: sbgfilesdesc.txt")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def scan_folder(folder_path):
    file_count = 0
    added_count = 0
    duplicate_count = 0
    scanned_files = set()

    # Count the total number of SBG files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.sbg'):
                file_count += 1

    # Scan and append information to the sbgfilesdesc.txt file
    with open("sbgfilesdesc.txt", "a") as file:
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith('.sbg'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as f:
                        content = f.read()

                        # Search for information in the file using regular expressions
                        name_match = re.search(r"##(.*?)\s*\((.*?)\)", content)
                        category_match = re.search(r"##(.*?)\((.*?)\)", content)
                        duration_match = re.search(r"##(.*?)\n(\d+)\s+minutes", content, re.IGNORECASE)
                        description_match = re.search(r"##(.*?)\n(.*?)\n-SE", content, re.DOTALL)

                        name = name_match.group(1) if name_match else "Unknown"
                        additional_info = name_match.group(2) if name_match else "Unknown"
                        category = category_match.group(1) if category_match else "Unknown"
                        intensity = category_match.group(2) if category_match and len(category_match.groups()) >= 2 else "Unknown"
                        duration = duration_match.group(2) + " minutes" if duration_match else "Unknown"
                        description = description_match.group(2).replace('\n##', ' ').strip() if description_match else "Unknown"

                        # Check if the file has already been scanned
                        if file_name not in scanned_files:
                            # Append information to the sbgfilesdesc.txt file
                            file.write(f"=================== | {file_name} | ===================\n")
                            file.write(f"Name: {name}\n")
                            file.write(f"Additional Info: {additional_info}\n")
                            file.write(f"Category: {category}\n")
                            file.write(f"Intensity: {intensity}\n")
                            file.write(f"Duration: {duration}\n")
                            file.write("\n")
                            file.write("Description:\n")
                            file.write(description)
                            file.write("\n\n")

                            added_count += 1
                            scanned_files.add(file_name)

                            # Display scanning progress
                            progress = round((added_count / file_count) * 100, 2)
                            print(f"[SCAN] Adding files. Added {added_count}/{file_count} [{progress}%]")
                        else:
                            duplicate_count += 1

    # Display scanning results
    message = f"Found {file_count} SBG files. Added {added_count} files to sbgfilesdesc.txt."
    if duplicate_count > 0:
        message += f" Skipped {duplicate_count} duplicate files."
    print("Scanning completed:", message)
    load_file_content()


def start_scanning():
    # Selec path using gui
    folder_path = filedialog.askdirectory()

    if folder_path:
        scan_folder(folder_path)

def show_info():
    messagebox.showinfo("Information", """SBG File Scanner
This open source program scans the selected folder for files with the *.sbg extension, which are generated by the SBAGEN program.

[Version 0.1]
[Open source]

[Authors:]

[Main creator of file - Deto#8444]""")


def load_file_button_clicked():
    file_text.delete("1.0", tk.END)
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            file_text.insert(tk.END, content)

# Initialize the text field
file_text = tk.Text(window)
file_text.pack(side="top", fill="both", expand=True)

# Container for buttons
button_frame = tk.Frame(window)
button_frame.pack(side="bottom", fill="x", padx=10, pady=10)

# Load File button
load_button = tk.Button(button_frame, text="LOAD FILE", command=load_file_content)
load_button.pack(side="left", fill="x", expand=True, padx=10)

# Scan Folder button
scan_button = tk.Button(button_frame, text="SCAN FOLDER", command=start_scanning)
scan_button.pack(side="left", fill="x", expand=True, padx=10)

# Info button
info_button = tk.Button(button_frame, text="INFO", command=show_info)
info_button.pack(side="left", fill="x", expand=True, padx=10)


def open_discord():
    webbrowser.open("https://discord.com/invite/CZEM6mHNdt")

# Discord BTN
discord_button = tk.Button(button_frame, text="My Discord Server", command=open_discord)
discord_button.pack(side="left", fill="x", expand=True, padx=10, pady=10)

# Start main loop
window.geometry(f"{window_width}x{window_height}")
window.mainloop()
