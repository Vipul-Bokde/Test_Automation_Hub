Feature: Create new mapping under global file templates

    Background:
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application


    # behave GP\automation_test\behave\features\global_new_mapping.feature --tags=@Create_Template
    @Create_Template                 
    Scenario Outline: Create the new GP templates
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select file templates option under global from the burger menu
        Given I click on new template
        Given I enter new template details
        Then I click on template submit
        When I log out
        Examples:
        |sheet|scenario_id|tc_id|
        # Upload PHSResults File 
        |GP_File_Template_Feature|Create_Template_SC_1|TC1|

    # behave GP\automation_test\behave\features\global_new_mapping.feature --tags=@Send_Template_for_Approval
    @Send_Template_for_Approval                 
    Scenario Outline: Send new GP templates for Apporval
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select file templates option under global from the burger menu
        Then I select file templates name to activate and send for approve
        When I log out
    Examples:
        |sheet|scenario_id|tc_id|
        # Upload PHSResults File 
        |GP_File_Template_Feature|Create_Template_SC_1|TC1|
  

    # behave GP\automation_test\behave\features\global_new_mapping.feature --tags=@Approval_template
    @Approval_template
    Scenario Outline: Approve the template
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select file templates option under global from the burger menu
        Given I click on new template
        Given I enter new template details
        Then I click on template submit
        Then I select file templates name to activate and send for approve
        When I log out
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application as a Manager
        When I select a config to the environment
        Then I enter the application
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select Approvals from burger menu
        When I select client and type from dropdown
        Then Select template and approve
        When I log out
    Examples:
        |sheet|scenario_id|tc_id|
        # Upload PHSResults File 
        |GP_File_Template_Feature|Create_and_Approve_Template_SC_1|TC1|

    # Dev Ticket(GP-806) In-Sprint Automation Ticket(GP-816)
    # Template should be in Active State
    # behave GP\automation_test\behave\features\global_new_mapping.feature --tags=@Send_Template_for_Approval_to_Delete
    @Send_Template_for_Approval_to_Delete                 
    Scenario Outline: Send Delete GP templates for Apporval
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select file templates option under global from the burger menu
        Given I click on new template
        Given I enter new template details
        Then I click on template submit
        Then I select file templates name to activate and send for approve
        When I log out
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application as a Manager
        When I select a config to the environment
        Then I enter the application
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select Approvals from burger menu
        When I select client and type from dropdown
        Then Select template and approve
        When I log out
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select file templates option under global from the burger menu
        Then I select file templates to delete and send for approve
        When I log out
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application as a Manager
        When I select a config to the environment
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select Approvals from burger menu
        When I select client and type from dropdown
        Then Select delete template and approve
        Given I select file templates option under global from the burger menu
        Then I crossverify the deleted template
    Examples:
        |sheet|scenario_id|tc_id|
        # Upload PHSResults File 
        |GP_File_Template_Feature|Create_and_Delete_Template_SC_1|TC1|
   
    # behave GP\automation_test\behave\features\global_new_mapping.feature --tags=@Add_gp_template_mapping
    @Add_gp_template_mapping
    Scenario Outline: Create the GP mapping
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select file templates option under global from the burger menu
        When I Click on GP mappings 
        When I create new mapping
        When Select details for new mapping 
        Then I click on mapping submit button
        When I log out
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_File_Template_Feature|GP_Mapping_SC_1|TC1|
    
    # behave GP\automation_test\behave\features\global_new_mapping.feature --tags=@delete_gp_template_mapping
    @delete_gp_template_mapping
    Scenario Outline: Delete the GP mapping
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select file templates option under global from the burger menu
        When I Click on GP mappings 
        When I select mapping and delete
        Then I verify deleted mapping
        When I log out
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_File_Template_Feature|GP_Mapping_SC_1|TC1|