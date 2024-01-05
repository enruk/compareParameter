class parameter:
    def __init__(self,name,value):
        self.name = name 
        self.value = value
        
class parameter_list:
    def __init__(self,TcPOU_file_path):
        self.file_path = TcPOU_file_path
        self.parameters = []
        
    def read_list_from_xml(self):
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