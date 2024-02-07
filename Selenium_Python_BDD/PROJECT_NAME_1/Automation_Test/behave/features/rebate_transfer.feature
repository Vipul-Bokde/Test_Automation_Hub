Feature: Rebate Transfer Feature

    Background:
        Given Initialize testdata for "CREDENTIALS_QA" "SC_2" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application

    # behave GP\automation_test\behave\features\rebate_transfer.feature --tags=@Rebate_Transfer
    @Rebate_Transfer 
    Scenario Outline: Transfter the rebate
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select price rebate transfter from hamburger menu
        When Click on transfer button
        Then Add the period Date 
        Then Click on a submit button
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Rebate_Transfer_Feature|rebate_transfer_SC_01|TC1|

    # behave GP\automation_test\behave\features\rebate_transfer.feature --tags=@Rebate_Transfer_Export
    @Rebate_Transfer_Export
    Scenario: Rebate Export Option
        When I select price rebate transfter from hamburger menu
        Given I click on Export of File
        Then I validate export of grid in Rebate transfer screen
       
    # behave GP\automation_test\behave\features\rebate_transfer.feature --tags=@Rebate_Transfer_Validation
    # Before Executing this Scenario add the DB credentials In database_connection.py file from
    # Utilies folder.
    @Rebate_Transfer_Validation
    Scenario Outline:Rebate Transfer Validation
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select price rebate transfter from hamburger menu
        When I filter the status column for unsettled invoice
        Then I verify the status column for unsettled invoice
        Then I get data for Dollar Amount column
        When I verify Dollar Amount and get data for column Internal ID and rebate source I click on transfer button in rebate transfer page
        Then I Add the period Date
        Then Click on a submit button
        Then I verify the rebate transfer is successfully done on rebate transfer page
        When I select view data from hamburger menu
        When I select combobox dropdown
        Then I check data is available for filtered settlement number
        Then I filter the settlement number and period month
        Then I verify settlement number period month and rebate source is same as selected in rebate transfer page
        Then I verify records of UI and DB are equal for selected settlement number
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Rebate_Transfer_Feature|rebate_transfer_SC_02|TC1|