Feature: Price Type Delete

    Background:
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application

    # behave GP\automation_test\behave\features\price_type_delete.feature    
    @delete_price_type
    Scenario Outline: Select price type editor and delete price type .
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select price type editor from burger menu
        When I select Price type and click on checkbox
        Then I Delete Price Type
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Price_Type_Feature|Price_Type_Delete_SC_1|TC1|

