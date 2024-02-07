Feature: Test
    Background:
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application

    # behave GP\automation_test\behave\features\view_data.feature
    Scenario Outline: Open GP view data page
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select Viewdata from the burger menu
        When Click on dropdown button and select data type from dropdown 
        Then I see the data record in Viewdata page and click on download button
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_View_Data_Feature|view_data_export_SC_01|TC1|
