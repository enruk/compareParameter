class parameter:
    def __init__(self,name,value):
        self.name = name 
        self.value = value
        
class parameter_list:
    def __init__(self,TcPOU_file_path):
        self.file_path = TcPOU_file_path
        self.parameters = []
        
    def add_parameters(self,parameter):
        self.parameters.extend(parameter)    
    
    def read_param_from_file(self):
        
        # method is writing all lines with GVL in a parameter list
        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.strip()
                
                if '//' in line:
                    comment = line.split('//', 1)[1].strip()
                    line = line.split('//', 1)[0].strip()
                else:
                    comment = None
                
                if line.startswith("GVL_") and ":" in line and ";" in line:
                    param, value = line.strip(";").split(":")
                    param = param.strip(" \t")  # Entferne Leerzeichen und Tabulatoren von Parametern
                    value = value.strip(" =;")  # Entferne Leerzeichen, Gleichzeichen und Semikolon von Werten
                    parameter_instance = parameter(name=param,value=value)
                    self.parameters.append(parameter_instance)
                    
                    
    def read_local_param_from_file(self,ignored_param):
        
        # method is writing all lines with GVL in a parameter list, except for the "ignored_param"
        with open(self.file_path, 'r') as file:
            parameters_reached = False
            row_counter = 0
            for line in file:
                row_counter = row_counter + 1 # only for debugging needed
                line = line.strip()
                
                # look for the actParameterChanges
                if "MAIN.instProfiler" in line:
                    parameters_reached = True
                
                if parameters_reached:
                    # remove the comment
                    if '//' in line:
                        comment = line.split('//', 1)[1].strip()
                        line = line.split('//', 1)[0].strip()
                    else:
                        comment = None
                        
                    # check if parameter has more then 3 parts, separated by dots
                    if line.startswith("GVL_"):
                        front_string = line.split("=",1)[0]
                        parts = front_string.split(".")
                        
                        if len(parts) > 3 and ":" in line and ";" in line and not any(param in line for param in ignored_param):
                                param, value = line.strip(";").split(":")
                                param = param.strip(" \t")  # Entferne Leerzeichen und Tabulatoren von Parametern
                                value = value.strip(" =;")  # Entferne Leerzeichen, Gleichzeichen und Semikolon von Werten
                                parameter_instance = parameter(name=param,value=value)
                                self.parameters.append(parameter_instance)
                                
