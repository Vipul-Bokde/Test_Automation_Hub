Feature: Upload Screen

    Background:
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application

    @Upload_Product_and_validate
    Scenario Outline: Upload_File_and_validate
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select Upload File from burger menu
        When I upload file
        Then I Verify File status
    Examples:
        |sheet|scenario_id|tc_id|
        # |GP_Uploads_Screen|Upload_validate_SC_1|TC1|
        |GP_Uploads_Screen|Upload_validate_SC_1|TC2|
