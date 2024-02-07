Feature: GP Read Only Smoke TestSuite
    Background:
        Given Initialize testdata for "GP_Read_Only_Smoke_TestSuite" "SC_ROSTS_01" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application

    # behave GP\automation_test\behave\features\GP_Read_Only_Smoke_TestSuite.feature --tags=@GP_Read_Only_Smoke_TestSuite
    @GP_Read_Only_Smoke_TestSuite
    Scenario Outline: GP Read Only Smoke TestSuite
        # GP Read Only Smoke TestSuite
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When user is on landing screen data overview
        Then I verify client name and overview screen all available buttons
            |Button_Name |
            |Upload      |
            |Validate    |
        When I navigate to the run screen
        Then I verify run screen all available buttons
            |Run_Screen_Buttons|
            |New Run           |
            |Close Run(s)      |
            |Delete Run(s)     |  
            |Compare           |
        When I navigate to data dictionary screen
        Then I verify data dictionary screen all available buttons
            |Data_Dictionary_Buttons|
            |New Table              |
            |Delete Table(s)        |
        When user navigate to view data screen
        Then I verify view data screen all available buttons
        When I navigate to Price type editor screen
        Then I verify Price type editor screen all available buttons
            |Price_Type_Editor      |
            |New Price Type         |
            |Delete Price Type(s)   |
            |Compare                |
        When user navigate to Rebate transfer screen
        Then user verify Rebate transfer screen all available buttons
        When I navigate to Approvals screen
        Then I verify Approvals screen all available buttons and available dropdown
            |Approvals              |
            |Approve                |
            |Reject                 |
        When I navigate to Uploads screen
        Then I verify Uploads screen all available buttons
            |Uploads              |
            |Delete File(s)       |
            |Upload File          |
        When I navigate to client join screen
        Then I verify client joins screen all available buttons
            |Client ->Joins       |
            |Inspect Joins        |
            |Import Joins         |
            |Export Joins         |
            |Add Join             |
            |Actions              |
        When I navigate to client pricing screen
        Then I verify client pricing screen all available buttons
            |Client ->Pricing       |
            |Delete Price(s)        |
            |New Pricing            |
        When I navigate to client product screen
        Then I verify client product screen all available buttons
            |Client ->Product       |
            |Delete Product(s)      |
            |New Product            |
        When I navigate to Global price type screen
        Then I verify Global price type screen all available buttons
            |Global ->PriceTypes     |
            |New Price Type          |
        When I navigate to Global file template screen
        Then I verify file template screen all available buttons
            |Global ->File Template -> Templates|
            |New Template                       |
            |Delete Template                    |
        When I navigate to Global file template GP mapping screen
        Then I verify Global file template GP mapping screen all available buttons
            |Global ->File Template -> GPMappings|
            |New Mapping                         |
            |Delete Mapping(s)                   |
    Examples:
        |sheet                      |scenario_id   |tc_id|
        |GP_Read_Only_Smoke_TestSuite|SC_ROSTS_01   |TC1  |