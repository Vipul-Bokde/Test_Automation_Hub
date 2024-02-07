@SMoke_Test_1
Feature: Price Type Editor

    Background:
        Given Initialize testdata for "CREDENTIALS_QA" "SC_3" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application

    # behave GP\automation_test\behave\features\price_type_editor.feature --tags=@Create_price_type
    @Create_price_type 
    Scenario Outline: Create the price type
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select price type editor from burger menu
        When Create new price type
        Then I click on the submit
        Then I verify price type is created
        When I log out
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Price_Type_Feature|Price_Type_SC_1|TC1|

    # behave GP\automation_test\behave\features\price_type_editor.feature --tags=@Logic_Tab_validations
    @Logic_Tab_validations
    Scenario Outline: Logic Tab validations
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select price type editor from burger menu
        Then Open the created price type
        When user add logic for bucket
        When user add logic for formula
        Then user verify disable action for formula and bucket
        Then user verify enable action for formula and bucket
        When user delete the formula and bucket
        Then user verify undo and redo functionality
        When I log out
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Price_Type_Feature|Price_Type_SC_1|TC1|
        
    # behave GP\automation_test\behave\features\price_type_editor.feature --tags=@Import_price_type_file
    @Import_price_type_file 
    Scenario Outline: Import the price type file
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select price type editor from burger menu
        Then Open the created price type
        Then import the price type file
        Then I verify uploaded file
        When I log out
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Price_Type_Feature|Price_Type_SC_1|TC1|

    # behave GP\automation_test\behave\features\price_type_editor.feature --tags=@Update_price_type
    @Update_price_type 
    Scenario Outline: Update the price type editor
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select price type editor from burger menu
        Then Open the created price type
        Then update the price type editor details
        When I log out
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Price_Type_Feature|Price_Type_SC_1|TC1|

    # behave GP\automation_test\behave\features\price_type_editor.feature --tags=@Output_tab_template_upload,@SMoke_Test_1
    @Output_tab_template_upload @SMoke_Test_1
    Scenario Outline: Download the report template file
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select price type editor from burger menu
        Then Open the created price type
        Then Click on output tab under the price type
        Then verify data is present for updated bucket
        Then Upload the report template file
        Then Download the report template file and click on run report button
        Then Export the report template file
        When I log out
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Price_Type_Feature|Price_Type_SC_1|TC1|

    # behave GP\automation_test\behave\features\price_type_editor.feature --tags=@Approve_Price_Type,@Confirm_Revision_History 
    @Approve_Price_Type 
    Scenario Outline: Approve Price Type
        Given Initialize testdata for "CREDENTIALS_QA" "SC_4" and "TC1"
        When I log out
        Given As a user login into the application
        When I login into the application as a Manager
        When I select a config to the environment
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select Approvals from burger menu
        When I select client and type from dropdown
        Then Select a price type and approve
        When I log out
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Price_Type_Feature|Price_Type_SC_1|TC1|

    
    # Dev Ticket(GP-762) In-Sprint Automation Ticket(GP-821)
    # behave GP\automation_test\behave\features\price_type_editor.feature --tags=@Confirm_Revision_History,@SMoke_Test_2
    @Confirm_Revision_History @SMoke_Test_2
    Scenario Outline: Confirm the revision history
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select price type editor from burger menu
        Then Open the created price type
        When I click on revision history tab
        #Then Click on changes tab under the price type
        Then user gets effective start and end date  and comment from changes tab
        Given Initialize testdata for "CREDENTIALS_QA" "SC_4" and "TC1"
        Then Confirm the revision history
        When I log out
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Price_Type_Feature|Price_Type_SC_1|TC1|

    # behave GP\automation_test\behave\features\price_type_editor.feature --tags=@Create_version_2_with_case_2,@SMoke_Test_1
    @Create_version_2_with_case_2 @SMoke_Test_1
    Scenario Outline: Create Version 2 with case 2
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select price type editor from burger menu
        Then Open the created price type
        When I click on edit button
        When I click on revision history tab
        #Then Click on changes tab under the price type
        Then I verify price type is in edit mode with pencil icon
        When I get version 1 effective start date and end date
        Then I select effective start date and end date as end of time for version 2
        When I submit the effective date changes
        Then I get version 2 effective start date and end date
        When I click on logic tab
        Then I submit price type for approval
        Given Initialize testdata for "CREDENTIALS_QA" "SC_3" and "TC1"
        When I log out
        Given As a user login into the application
        When I login into the application as a Manager
        When I select a config to the environment
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select Approvals from burger menu
        When I select client and type from dropdown
        Then Select a price type and approve
        Given Initialize testdata for "CREDENTIALS_QA" "SC_3" and "TC1"
        When I log out
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select price type editor from burger menu
        Then Open the created price type
         When I click on revision history tab
        #Then Click on changes tab under the price type
        Then I verify previous version effective end date is updated
        Then I verify note column is updated
        Given Initialize testdata for "CREDENTIALS_QA" "SC_3" and "TC1"
        Then I verify modified on and modified by should also change
        When I log out
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Price_Type_Feature|Price_Type_SC_1|TC1|

    # behave GP\automation_test\behave\features\price_type_editor.feature --tags=@Create_New_version_3_with_effective_end_as_blank,@SMoke_Test_1
    # Create new versioon by keeping effective end date as blank and same effective start date as version 2
    @Create_New_version_3_with_effective_end_as_blank @SMoke_Test_1
    Scenario Outline: Create New version 3 with effective end as blank
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select price type editor from burger menu
        Then Open the created price type
        When I click on edit button
        When I click on revision history tab
        #Then Click on changes tab under the price type
        Then I verify price type is in edit mode with pencil icon
        Then I get version 2 effective start date and end date
        Then I select effective start date and keep effective end date as blank for version 3
        When I submit the effective date changes
        When I click on logic tab
        Then I submit price type for approval
        Given Initialize testdata for "CREDENTIALS_QA" "SC_3" and "TC1"
        When I log out
        Given As a user login into the application
        When I login into the application as a Manager
        When I select a config to the environment
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select Approvals from burger menu
        When I select client and type from dropdown
        Then Select a price type and approve
        Given Initialize testdata for "CREDENTIALS_QA" "SC_3" and "TC1"
        When I log out
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select price type editor from burger menu
        Then Open the created price type
        When I click on revision history tab
        #Then Click on changes tab under the price type
        When I get version 3 effective start date and end date
        Then I verify version 2 and version 3 effective start and end date is same
        Then I verify version 3 effective end date is updated to end of time
        When I log out
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Price_Type_Feature|Price_Type_SC_1|TC1|