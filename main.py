import tkinter as tk
import gui
import project
import excel_file       
 
                            
if __name__ == "__main__":
    
    root = tk.Tk()
    app = gui.user_interface(root)
    root.mainloop()
    
    # format data_array from gui to project_data[X][Y], X project, Y data (0=name, 1=folder path)
    app.data_array = list(filter(lambda x: x != "", app.data_array))
    project_data = []
    project_data = [app.data_array[i:i+2] for i in range(0, len(app.data_array), 2)]  
    
    # create excel file, get desktop path and some info
    excel = excel_file("Parameter Comparison")
    excel.set_target_file_path()
    excel.get_info_for_script()
    
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
        new_project.fill_parameter_lists_from_xml()
        
        # ove#rwrite parameter from standardtemplateschanges to standardtemplate
        new_project.write_changes_to_standard_template()
        
        # get the local changes
        new_project.get_local_changes(excel.Ignored_folders,excel.ignored_parameters)
        
        # add project to projectlist
        project_list.append(new_project)
    
    # write project list to excel class
    excel.project_list = project_list
    
    # write first project to excel
    excel.write_first_project_to_excel()
    
    # add more projects to excel sheet
    if number_of_projects > 1:
        for index_in_project_list in range(1,number_of_projects):
            excel.add_next_project_to_excel(index_in_project_list)
            excel.compare_parameters_to_master_parameters(index_in_project_list)
        
    # create excel files for local changes of each project
    for index_in_project_list in range(number_of_projects):
        excel_local_changes = excel(project_list[index_in_project_list].name,project_list)
        excel_local_changes.set_target_file_path()
        excel_local_changes.write_local_changes_to_excel(index_in_project_list)

    # Add 2 columns between A and B and split GVL to make it easier to filter in excel
    excel.format_sheet()
    
    # set filters if needed
    if excel.predefined_filter:
        excel.get_filters()
        excel.set_filters() 
    
    # Tell user script is done
    print("Compare Done")
    