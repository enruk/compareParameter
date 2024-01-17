# compareXML

##DESCRIPTION
compare standardtemplate.xml of different PLCs to be able to compare parameters in different projects

######### ------------------- VERSION ------------------- #########
1.0 - initial version                               18.12.2023      HT
1.1 - implement local changes and filters           17.01.2024      HT

######### ------------------- HOWTO ------------------- #########

    ######### -------PREPARATION
    1. You need all PLC you want to compare somewhere saved local
    2. you can adjust the two xml-files (more info down below)
        - stuff_to_ignore.xml
        - filters.xml
    3. All your projects need to have the following structur, otherwise the programme will not work

        OverheadSystems
            ...
            Project
            ProjectSpecials
                PRG_StandardTemplate.TcPOU
                PRG_StandardTemplatesChanges.TcPOU
            ...
    


    ######### ------- USE THIS SCRIPT
    1. run the main.exe, a command prompt should open and after a while the application window
    2. use the application window
        - add and remove project as much as you want with the buttons, but dont add more project rows than you need
        - set a name for every project
        - set for every the path to the project folder, more info to the project folder down below
        - set a filter if you want, you dont have to
    3. Press run
    4. when the script is done, the command prompt will show "Compare Done"
        - On your desktop you should find a new folder called "Parameter Comparison"
        - in that you will find multiple excel files
            - "Parameter Comparison.xlsx"
            - "Fitlered Parameter Comparison.xlsx" - if you have selected a filter
            - for each project one .xlsx for local changes
        - in the Comparion files different values in the projects should be marked with red color
    6. Close the excel sheets before running the script again


    ######### ------- Select the correct project folder
    You need to choose the folder that contains the "OverheadSystems"-folder
    
    Your PLC     <---- select that folder
        .vs
        _Boot
        _Config
        OverheadSystems
            ...
            Project
            ProjectSpecials
            ...
        XMLs


    ######### ------- XML-files:

    stuff_to_ignore.xml:
        - add objects here that are in your Your_PLC\OverheadSystems\Project-folder that dont have programm you want to search for local changes

    filters.xml:
        - add devices on each filter that you want to include in the filter
        - the filter "always" will always be included in every filter