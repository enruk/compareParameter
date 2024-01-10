import tkinter as tk
import gui
from project import project
from compare import comparison
 
                            
if __name__ == "__main__":
    
    root = tk.Tk()
    app = gui.user_interface(root)
    root.mainloop()
    
    # format data_array from gui to project_data[X][Y], X project, Y data (0=name, 1=folder path)
    app.data_array = list(filter(lambda x: x != "", app.data_array))
    project_data = []
    project_data = [app.data_array[i:i+2] for i in range(0, len(app.data_array), 2)]  
    
    # create excel file, get desktop path and some info
    comp = comparison()
    comp.set_target_file_path()
    comp.get_info_for_script()
    print("Information gathered")
    
    # get filter info from GUI
    comp.filters_on = app.filters_on
    comp.filter_index = app.filter_index
    
    # read projects
    project_list = []
    number_of_projects = int(len(project_data))
    for index_in_project_list in range(number_of_projects):
        # create new project
        project_name = project_data[index_in_project_list][0]
        project_folder_path = project_data[index_in_project_list][1]
        column_in_excel = index_in_project_list + 2 #column 1=parameters, therefore first project[0] in column = 2
        new_project = project(project_name,project_folder_path,column_in_excel) 
        
        # get file pathes of standardTemplate and StandardTemplatesChanges
        new_project.get_path_of_templates()
        
        # fill parameter_list with data from templates
        new_project.get_param_from_standardtemplate()
        
        # overwrite parameter from standardtemplateschanges to standardtemplate
        new_project.write_changes_to_standard_template()
        
        # get the local changes
        new_project.get_local_changes(comp.Ignored_folders,comp.ignored_parameters)
        
        # add project to projectlist
        project_list.append(new_project)
    
    # write project list to excel class
    comp.project_list = project_list
    print("Parameter gathered")
    
    # write first project to excel
    comp.write_first_project_to_mainfile()
    
    # add more projects to excel sheet
    if number_of_projects > 1:
        for index_in_project_list in range(1,number_of_projects):
            comp.add_next_project_to_mainfile(index_in_project_list)
            comp.compare_parameters_in_mainfile(index_in_project_list)
            
    # Add 2 columns between A and B and split GVL to make it easier to filter in excel
    comp.format_parameter_column(comp.path_file_comparison)
    comp.format_sheet(comp.path_file_comparison)
    
    print("Parameter Comparion done")
    
    # create excel files for local changes of each project
    for index_in_project_list in range(number_of_projects):
        comp.write_local_changes_to_excel(index_in_project_list)
        
    print("Local Parameter changes collected")

    # set filters if needed
    if comp.filters_on:
        comp.get_filters()
        comp.create_filtered_copy()
        comp.format_sheet(comp.path_file_filtered_comparion)
        
    print("Filtered Parameter Comparion done")
    
    # Tell user script is done
    print("Program Done")
    