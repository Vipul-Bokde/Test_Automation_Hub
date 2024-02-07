Feature: GP COnfigurations Screen

    Background:
        Given Initialize testdata for "CREDENTIALS_QA" "SC_5" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application
    
    # behave GP\automation_test\behave\features\gp_configurations.feature --tags=@GP_Config_Screen
    @GP_Config_Screen                 
    Scenario Outline: Validate GP Configurations Screen
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select GP Configurations option under client from the burger menu
        When  I validate GP Configurations Screen Columns
        When  I click on add config and create new GP Configuration
        Then  I delete existing values of newly created gp config, check statuses and modify it by adding new values
        When  I upload a rebate file from upload screen
        Then  I verify view data and database of uploaded file for that source and period
        Examples:
        |sheet|scenario_id|tc_id| 
        |GP_Configurations|Create_And_Add_Config_SC_1|TC1|

    # behave GP\automation_test\behave\features\gp_configurations.feature --tags=@Transaction_reversal_job
    @Transaction_reversal_job                 
    Scenario Outline: Validate Transaction Reversal Job Tracker Screen
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Then  I validate transaction reversal job
        Examples:
        |sheet|scenario_id|tc_id| 
        |GP_Configurations|Create_And_Add_Config_SC_1|TC1|

    




    