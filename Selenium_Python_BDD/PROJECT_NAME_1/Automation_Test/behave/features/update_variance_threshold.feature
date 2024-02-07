Feature: update variance threshold

    Background:
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application

    # behave GP\automation_test\behave\features\update_variance_threshold.feature
    Scenario Outline: Select price type editor and update variance threshold.
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select price type editor from burger menu
        When I click on Price type and select Rules Tab
        When I update threshold
        Then I click on submit
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Price_Type_Feature|Variance_Threshold_SC_01|TC1|

