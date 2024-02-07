Feature: Join Functionality

    Background:
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application

    # behave GP\automation_test\behave\features\client_joins.feature --tags @Add_Join           
	@Add_Join
    Scenario Outline: Add Join
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select joins option under client from the burger menu
        Given Click on add join
        When Select details for new join 
        Then click on submit for adding new join
        When I log out
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Client_Join_Feature|create_Join_SC_1|TC1|
    
    # behave GP\automation_test\behave\features\client_joins.feature --tags @Edit_Join
    @Edit_Join
    Scenario Outline: Edit joins
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select joins option under client from the burger menu
        Given I Select the created join
        When Edit the details of selected join 
        Then perform click on submit button
        Then I check edited join values
        When I log out
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Client_Join_Feature|edit_Join_SC_1|TC1|

    # behave GP\automation_test\behave\features\client_joins.feature --tags @Disable_join
    @Disable_join
    Scenario: Disable joins
        Given I select joins option under client from the burger menu
        Then I Select the join and click on action
        Then I disable join and verify 
        When I log out
    
    # behave GP\automation_test\behave\features\client_joins.feature --tags @Enable_join
    @Enable_join
    Scenario: Enable joins
        Given I select joins option under client from the burger menu
        Then I Select the join and click on action
        Then I enable join and verify
        When I log out

    # behave GP\automation_test\behave\features\client_joins.feature --tags @Delete_join
    @Delete_join
    Scenario: Delete joins
        Given I select joins option under client from the burger menu
        Then I Select the join and click on action
        Then I delete join and verify 
        When I log out

    # behave GP\automation_test\behave\features\client_joins.feature --tags @Import_join
    @Import_join
    Scenario Outline: Import Join
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select joins option under client from the burger menu
        Then I click on import join and upload join file
        When I log out
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Client_Join_Feature|import_join_SC_1|TC1|

    # behave GP\automation_test\behave\features\client_joins.feature --tags @Export_join
    @Export_join
    Scenario: Export Join
        Given I select joins option under client from the burger menu
        Then I click on Export join and get exported file
        Then I crosscheck exported file and grid data
        When I log out

    # behave GP\automation_test\behave\features\client_joins.feature --tags @Inspect_join
    @Inspect_join
    Scenario Outline: Inspect Join
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select joins option under client from the burger menu
        Then I click on inspect join
        Then I select source and check query
        When I log out
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Client_Join_Feature|inspect_Join_SC_1|TC1|









    