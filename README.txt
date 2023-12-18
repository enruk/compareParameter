# compareXML

##DESCRIPTION
compare standardtemplate.xml of different PLCs to be able to compare parameters in the different projects

## VERSION
1.0 - 18.12.2023

## HOWTO

PREPARATION
1. Open all PLC you want to compare with TwinCAT, navigate to the StandardTemplate(PRG) and StandardTemplatesChanges(PRG) and export them as .xml
    - make sure the variable in the GVL is called "GVL_StandardTemplate"
    - right click on the PRG and click on "Export PLCopenXML"
    - choose a location


USE THIS SCRIPT
1. navigate to the dist folder and run the main.exe, a command prompt should open and after a while the application window
2. use the application window
    - set a name for every project
    - set for every project the location of the standardtemplate.xml and standardtemplateschanges.xml by using the button "Choose XML-File"
    - add more project by clicking the button Add project
    - dont put in more the 5 projects
3. Press run
4. when the script is done, the command prompt will show "Compare Done" and will disappear
5. Open the Excel sheet "Compare_Standardtemplates.xlsx"
6. Different values should be marked with red color
7. Close the excel sheet before running the script again

