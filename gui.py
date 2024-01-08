import tkinter as tk 
from tkinter import filedialog

entries_width_small = 30;
entries_width_big = 60;


class projectrow:
    
    def __init__(self, root, targetrow):
        
        self.targetrow = targetrow
        self.root = root
    
        # Row X
        self.project_label = tk.Label(root, text="Projekt:")
        self.project_label.grid(row=self.targetrow, column=0, padx=10, pady=10,sticky= "w")
        
        self.project_entry = tk.Entry(root)
        self.project_entry.grid(row=self.targetrow, column=1, padx=10, pady=10,sticky= "w")
        self.project_entry.config(width=entries_width_small)


class inputrow:
    
    def __init__(self, root, targetrow, labelname):
        
        self.root = root
        self.targetrow = targetrow
        self.labelname = labelname
    
        # Row X+1        
        self.project_name_entry = tk.Entry(root)
        self.project_name_entry.grid(row=self.targetrow, column=0, padx=10, pady=10,sticky= "w")
        self.project_name_entry.config(width=entries_width_small)
        
        self.folder_path_button = tk.Button(root, text="Choose PLC Projekt Folder", command=self.choose_folder)
        self.folder_path_button.grid(row=self.targetrow, column=1, padx=10, pady=10,sticky= "w")
        
        self.folder_path_variable = tk.StringVar()
        self.folder_path_entry = tk.Entry(self.root,textvariable=self.folder_path_variable,state='readonly',width=entries_width_big)
        self.folder_path_entry.grid(row=self.targetrow, column=2, padx=10, pady=10,sticky= "w")
        
    def choose_folder(self):
        folder_path = filedialog.askdirectory(title="Choose PLC Project Folder")
        if folder_path:
            self.folder_path_variable.set(folder_path)       


class user_interface:
    
    def __init__(self, root):
        
        self.entry_widgets = []
        
        self.root = root
        self.root.title("Compare XML Files")
        self.root.columnconfigure(0, minsize=350)
        self.root.columnconfigure(1, minsize=150)
        self.root.columnconfigure(2, minsize=500)

        self.fixed_width = 900
        self.initial_height = 200
        self.root.geometry(f"{self.fixed_width}x{self.initial_height}")
        
        # Row 0
        self.short_info = tk.Label(root, text="Helptext")
        self.short_info.grid(row=0, column=0, padx=10, pady=10,sticky= "w")
        
        self.add_button = tk.Button(root, text="Add Project", command=self.add_new_project)
        self.add_button.grid(row=0, column=1, pady=10)

        self.run_button = tk.Button(root, text="Run", command=self.close_window)
        self.run_button.grid(row=0, column=2, pady=10,sticky="e")
        
        # Row 1
        self.header_project_name = tk.Label(root, text="Projectname")
        self.header_project_name.grid(row=1, column=0, padx=10, pady=10,sticky= "w")
        
        self.header_project_folder = tk.Label(root, text="Projectfolder")
        self.header_project_folder.grid(row=1, column=1, padx=10, pady=10,sticky= "w")
        
        self.row_widgets = []
        
        self.add_new_project()
        
        self.fixed_width = 900
        self.initial_height = 150
        self.root.geometry(f"{self.fixed_width}x{self.initial_height}")
    

    def add_new_project(self):
        
        new_row = self.add_row()
        
        new_project_row = inputrow(self.root,new_row+1,"Folderpath PLC Project")
        self.row_widgets.append(new_project_row)
        self.entry_widgets.append(new_project_row.project_name_entry)
        self.entry_widgets.append(new_project_row.folder_path_entry)
        
        self.new_height = self.root.winfo_height() + 80 
        self.root.geometry(f"{self.fixed_width}x{self.new_height}")


    def add_row(self):
        row_count = self.root.grid_size()[1]
        self.root.grid_rowconfigure(row_count, weight=1)
        return row_count

    def close_window(self):
        self.data_array = []
        for entry in self.entry_widgets:
            entry_string = entry.get()
            self.data_array.append(entry_string)
        
        self.root.destroy()


