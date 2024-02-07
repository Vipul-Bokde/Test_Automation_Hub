Feature: Create new mapping under global file templates

    Background:
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application

    # behave GP\automation_test\behave\features\data_dictionary.feature --tags @create_table
    @create_table
    Scenario Outline: Create new table in data dictionary
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select data dictionary option under client from the burger menu
        Given Click on new table and create a new table
        When Select details for new table 
        Then click on submit
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Data_Dictionary_Feature|Create_table_SC_1|TC1|

    # behave GP\automation_test\behave\features\data_dictionary.feature --tags @create_new_column
    @create_new_column
    Scenario Outline: Create new column in data dictionary
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select data dictionary option under client from the burger menu
        Given Select any table row
        When Click on new column and select details
        Then click on submit button
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Data_Dictionary_Feature|Create_column_SC_1|TC1|

    # behave GP\automation_test\behave\features\data_dictionary.feature --tags @delete_column  
    @delete_column   
    Scenario Outline: Delete column in data dictionary
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select data dictionary option under client from the burger menu
        Given Select table row to delete column
        When Select column to delete
        Then Click on column delete
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Data_Dictionary_Feature|Delete_column_SC_1|TC1|

    # behave GP\automation_test\behave\features\data_dictionary.feature --tags @delete_table 
    @delete_table
    Scenario Outline: Delete new table in data dictionary
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select data dictionary option under client from the burger menu
        When Select added table row
        Then Click on delete
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Data_Dictionary_Feature|Delete_table_SC_1|TC1|


    
    

      