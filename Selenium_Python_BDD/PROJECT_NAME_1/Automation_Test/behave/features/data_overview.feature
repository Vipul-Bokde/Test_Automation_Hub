Feature: Data Overview
        In this feature is related to the upload the different files in 
        data overview page.

    Background:
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application
        
    # behave GP\automation_test\behave\features\data_overview.feature --tags @upload
    # File Type should be different based on file selection.
    # If user want upload differnt file then change the file type and add file to the xl sheet.  
    @upload                
    Scenario Outline: Upload file in data overview page
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given click on upload button on overview page
        When select file type, template and refresh option and click on Submit
        When user should navigate to upload screen then I see the file that was uploaded
        Then I take data from uploaded file 
        When I navigate to view data screen
        Then I crosscheck data 
    Examples:
        |sheet|scenario_id|tc_id|
        # Upload PHSResults File 
        |GP_Data_Overview_Feature|File_Upload_SC_1|TC1|
        # Upload Contract
        |GP_Data_Overview_Feature|File_Upload_SC_1|TC2|
        # Upload Trx Type
        |GP_Data_Overview_Feature|File_Upload_SC_1|TC3|
        # Contract Term
        |GP_Data_Overview_Feature|File_Upload_SC_1|TC4|
        # Contract Term Product
        |GP_Data_Overview_Feature|File_Upload_SC_1|TC5|

    # behave GP\automation_test\behave\features\data_overview.feature --tags @transaction_upload
    @transaction_upload                
    Scenario Outline: Transaction file Upload in data overview page
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given click on upload button on overview page
        When select file type, template and refresh option and click on Submit
        When user should navigate to upload screen then I see the file that was uploaded
        Then I take data from uploaded file 
        Then I click on uploaded source and period value from overview screen
        Then I verify view data and database count for that source and period
        Then I crosscheck data 
    Examples:
        |sheet|scenario_id|tc_id|
        # Chargeback
        |GP_Data_Overview_Feature|trx_File_Upload_SC_1|TC1|
        # Direct Sales
        |GP_Data_Overview_Feature|trx_File_Upload_SC_1|TC2|
        # Rebate
        |GP_Data_Overview_Feature|trx_File_Upload_SC_1|TC3|
        # Tricare
        |GP_Data_Overview_Feature|trx_File_Upload_SC_1|TC4|


    # behave GP\automation_test\behave\features\data_overview.feature --tags @validation
    @validation
    Scenario Outline: Validation Process
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I click on validate button on overview screen
        When I select validation data source 
        When I select validation period 
        Then I click on validate button and wait till validation completes
        Then I Check validation Results status
    Examples:
       |sheet|scenario_id|tc_id|
       # To validate Error Select start and end date.
       |GP_Data_Overview_Feature|Error_Msg_SC_1|TC1|
       # To validate Error Select at least 1 validation source.
       |GP_Data_Overview_Feature|Error_Msg_SC_1|TC2|
       # To validate Error End date must be greater than start date.
       |GP_Data_Overview_Feature|Error_Msg_SC_1|TC3|
       # To validate Data with correct dataset
       |GP_Data_Overview_Feature|Validation_SC_2|TC1|
    
    # behave GP\automation_test\behave\features\data_overview.feature --tags @validation_cancel
    @validation_cancel
    Scenario Outline: Validation cancel Process
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I click on validate button on overview screen
        When I select validation data source 
        When I select validation period
        Then I click on cancel button
    Examples:
       |sheet|scenario_id|tc_id|
       # To check cancel button functionality     
       |GP_Data_Overview_Feature|Validation_Cancel_SC_3|TC1|

    # behave GP\automation_test\behave\features\data_overview.feature --tags @validation_results
    @validation_results
     Scenario: Checking Validation Results
        Given Check validation results exist or not
        When I check "Missing ContractTerms" validation 
        Then I download "Create Records for ContractTerm" file
        When I check "Missing ContractTermProducts" validation 
        Then I download "Create Records for ContractTermProduct" file
        When I log out