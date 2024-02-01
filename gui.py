import tkinter as tk 
from tkinter import filedialog, ttk
import threading
import main


entries_width_small = 30
entries_width_big = 60
button_width_big = 30
button_width_small = 15


class inputrow:
    
    def __init__(self, root, targetrow, labelname):
        
        self.root = root
        self.targetrow = targetrow
        self.labelname = labelname
    
        # Row X+1        
        self.project_name_entry = tk.Entry(self.root, width = entries_width_small)
        self.project_name_entry.grid(row=self.targetrow, column=0, padx=10, pady=10,sticky= "w")
        self.project_name_entry.config(width=entries_width_small)
        
        self.folder_path_button = tk.Button(self.root, text="Choose PLC Projekt Folder", command=self.choose_folder, width = button_width_big)
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
        
        # porject info
        self.entry_widgets = []
        self.data_array_projects = []
        self.local_changes_On = False
        self.summary_differences_On = False
        
        # filter info
        self.filters_on = False
        self.filter_index = 0
        self.options = ["No Filter","Induction", "Dynamic Buffer", "Order Buffer", "Matrix Presorter", "Packing", "Crossover"]
        
        # root info
        self.root = root
        self.root.title("Compare Parameters of PLCs")
        self.root.columnconfigure(0, minsize=250)
        self.root.columnconfigure(1, minsize=150)
        self.root.columnconfigure(2, minsize=400)

        self.fixed_width = 900
        self.initial_height = 200
        self.root.geometry(f"{self.fixed_width}x{self.initial_height}")
        self.root.minsize(900, 200)  
        self.root.resizable(width=False, height=True)
        
        
        # Row 0
        infotext = "Compare of Parameters"
        self.short_info = tk.Label(root, text=infotext, justify="left",font=("Helvetica", 14, "bold"))
        self.short_info.grid(row=0, column=0,columnspan=3, padx=10, pady=10,sticky= "w")
        
        self.checkbox_local_changes_var = tk.BooleanVar()
        self.checkbox_local_changes = tk.Checkbutton(root, text="Get local changes of all PLCs", variable=self.checkbox_local_changes_var)
        self.checkbox_local_changes.grid(row=0, column=1, padx=10, pady=10,sticky="w")
        
        self.checkbox_differences_var = tk.BooleanVar()
        self.checkbox_differences = tk.Checkbutton(root, text="Create a summary of the found differences", variable=self.checkbox_differences_var)
        self.checkbox_differences.grid(row=0, column=2, padx=10, pady=10,sticky="w")
        
        # Row 1
        self.add_button = tk.Button(root, text="Add Project", command=self.add_new_project_row, width = button_width_small)
        self.add_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.delete_button = tk.Button(root, text="Remove Project", command=self.delete_row, width = button_width_small)
        self.delete_button.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.run_button = tk.Button(root, text="Run", command=self.run_programm, width = button_width_small)
        self.run_button.grid(row=1, column=2, padx=10, pady=10,sticky="e")
        
        self.dropdown_var = tk.StringVar(root)
        self.dropdown = ttk.Combobox(root, textvariable=self.dropdown_var, values=self.options)
        self.dropdown.set("Choose a Filter") 
        self.dropdown.grid(row=1, column=2, padx=20, pady=10,sticky= "w")
        
        # Row 2
        self.header_project_name = tk.Label(root, text="Projectname")
        self.header_project_name.grid(row=2, column=0, padx=10, pady=10,sticky= "w")
        
        self.header_project_folder = tk.Label(root, text="Projectfolder")
        self.header_project_folder.grid(row=2, column=2, padx=10, pady=10,sticky= "w")
        
        self.row_widgets = []
        
        self.add_new_project_row()


    def add_new_project_row(self):
        
        new_row = self.add_row()
        
        new_project_row = inputrow(self.root,new_row,"Folderpath PLC Project")
        self.row_widgets.append(new_project_row)
        self.entry_widgets.append(new_project_row.project_name_entry)
        self.entry_widgets.append(new_project_row.folder_path_entry)
        
        self.new_height = self.root.winfo_height() + 50 
        self.root.geometry(f"{self.fixed_width}x{self.new_height}")


    def delete_row(self):
        rows = self.root.grid_size()[1]
        if rows > 4:
            #delete in gui
            for column in range(self.root.grid_size()[0]):
                slaves = self.root.grid_slaves(row=rows-1, column=column)
                if slaves:
                    widget = slaves[0]
                    widget.destroy()
            self.root.grid_rowconfigure(rows-1, weight=0)
            self.root.grid_columnconfigure(column, weight=0)
            
            self.new_height = self.root.winfo_height() - 50 
            self.root.geometry(f"{self.fixed_width}x{self.new_height}")
            
            #delete in widget array
            self.entry_widgets = self.entry_widgets[:-2]


    def add_row(self):
        row_count = self.root.grid_size()[1]
        self.root.grid_rowconfigure(row_count, weight=1)
        return row_count        


    def run_programm(self):
        
        # get project info
        for entry in self.entry_widgets:
            entry_string = entry.get()
            self.data_array_projects.append(entry_string)
        self.local_changes_On = self.checkbox_local_changes_var.get()
        self.summary_differences_On = self.checkbox_differences_var.get()
        
        # get filter info
        selected_filter = self.dropdown_var.get()
        if selected_filter == "No Filter":
            self.filters_on = False
            self.filter_index = 0
        elif selected_filter == "Induction":
            self.filters_on = True
            self.filter_index = 1
        elif selected_filter == "Dynamic Buffer":
            self.filters_on = True
            self.filter_index = 2
        elif selected_filter == "Order Buffer":
            self.filters_on = True
            self.filter_index = 3
        elif selected_filter == "Matrix Presorter":
            self.filters_on = True
            self.filter_index = 4
        elif selected_filter == "Packing":
            self.filters_on = True
            self.filter_index = 5
        elif selected_filter == "Crossover":
            self.filters_on = True
            self.filter_index = 6
        
        self.root.destroy()


