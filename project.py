import os
from parameter import parameter_list                    

class project:
    def __init__(self,name,folder_path_project,column_in_excel):
        self.name = name
        
        self.path_to_PLC_folder = folder_path_project
        self.path_to_project_special_folder = ""
        self.path_to_project_folder= ""
        self.file_path_standard_template = ""
        self.file_path_standard_templates_changes = ""
        
        self.standard_template = parameter_list
        self.standard_templates_changes = parameter_list
        self.local_parameter_changes = parameter_list
        self.column_in_excel = column_in_excel
        
        
    def get_path_of_templates(self):
        
        self.path_to_project_special_folder = self.path_to_PLC_folder + "/OverheadSystems/ProjectSpecials" 
        
        name_standardtemplate = "PRG_StandardTemplate.TcPOU"
        name_standardtemplateschanges = "PRG_StandardTemplatesChanges.TcPOU"
         
        files = os.listdir(self.path_to_project_special_folder)
                
        if name_standardtemplate in files and name_standardtemplateschanges in files:
            self.file_path_standard_template = self.path_to_project_special_folder + "/" +name_standardtemplate
            self.file_path_standard_templates_changes = self.path_to_project_special_folder + "/" +name_standardtemplateschanges
        else:
            print(f"For the projekt '{self.name}' it was not possible to find the PRG_StandardTemplate.TcPOU and / or the PRG_StandardTemplatesChanges.TcPOU")
    
    
    def get_param_from_standardtemplate(self):
        self.standard_template = parameter_list(self.file_path_standard_template)
        self.standard_template.read_param_from_file()
        
        self.standard_templates_changes = parameter_list(self.file_path_standard_templates_changes)
        self.standard_templates_changes.read_param_from_file()
    
    
    def write_changes_to_standard_template(self):
        for parameter_changes in self.standard_templates_changes.parameters:
            counter = 0
            for parameter_standard in self.standard_template.parameters:
                if parameter_standard.name == parameter_changes.name:
                    self.standard_template.parameters[counter].value = parameter_changes.value
                    break
                counter = counter + 1 
    
    
    def get_local_changes(self,ignored_folders,ignored_param):
        
        self.local_parameter_changes = parameter_list("dummy_path")
        
        # go to project folder and get all folders of the PLC programm
        self.path_to_project_folder = self.path_to_PLC_folder + "/OverheadSystems/Project"
        content_project_folder = os.listdir(self.path_to_project_folder)
        clean_project_folder = [folder for folder in content_project_folder if folder not in ignored_folders]
        
        # go in every sub folders and get all programs in each sub folder
        for sub_folder in clean_project_folder:
            temp_sub_folder_path = self.path_to_project_folder + "/" + sub_folder
            content_program_folder = os.listdir(temp_sub_folder_path)
            clean_program_folder = [element for element in content_program_folder if element != "DUTs"]
            
            # go throw all programs, create a temporaly list of local changes
            for program in clean_program_folder:
                program_path = temp_sub_folder_path + "/" + program
                temp_parameter_list = parameter_list(program_path)
                temp_parameter_list.read_local_param_from_file(ignored_param)
                
                # copy all temporary changes to the main list for local changes
                self.local_parameter_changes.parameters.extend(temp_parameter_list.parameters)
                temp_parameter_list.parameters.clear()