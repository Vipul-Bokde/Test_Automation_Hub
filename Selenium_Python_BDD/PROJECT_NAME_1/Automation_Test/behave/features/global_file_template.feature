Feature: Create new file template and its functionalities under global file templates

    Background:
        Given Initialize testdata for "CREDENTIALS_QA" "SC_6" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application

    # behave GP\automation_test\behave\features\global_file_template.feature --tags=@Validate_File_Template_Screen_Functionality
    @Validate_File_Template_Screen_Functionality               
    Scenario Outline: Create the new GP File template and validate its entire functionalities
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I upload file template using overview screen and validate its status
        Given I validate file template screen buttons
        When  I validate new fields screen and perform deletion of added field
        When  I validate manage test files elements
        When  I validate and edit advanced option elements 
        When  I click on submit for approval
        Then  I validate X icon availability for active or pending status
        When  I log out
        Given Initialize testdata for "CREDENTIALS_QA" "SC_2" and "TC1"
        Given As a user login into the application
        When  I login into the application as a Manager
        When  I select a config to the environment
        Then  I enter the application
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When  I select Approvals from burger menu
        When  I select client and type from dropdown
        Then  Select template name for approval and approve
        When  I log out
        Examples:
        |sheet|scenario_id|tc_id|
        # Upload PHSResults File 
        |GP_Global_File_Template|Create_File_Temp_SC_1|TC1|

    # behave GP\automation_test\behave\features\global_file_template.feature --tags=@Validate_template_history
    @Validate_template_history                
    Scenario Outline: Validate template history and its columns informations 
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Then I validate template history values
        Examples:
        |sheet|scenario_id|tc_id|
        # Upload PHSResults File 
        |GP_Global_File_Template|Create_File_Temp_SC_1|TC1|




        