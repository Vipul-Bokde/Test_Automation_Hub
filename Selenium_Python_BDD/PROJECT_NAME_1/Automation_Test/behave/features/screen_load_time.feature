Feature: Screen Laod Time

    # behave GP\automation_test\behave\features\screen_load_time.feature --tags=@screen_load_time
    @screen_load_time
    Scenario Outline: title: Navigate through screens
        Given Initialize testdata for "CREDENTIALS_QA" "SC_2" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on the select run
        When I navigate to run screen
        When I select to price type and go to summary tab
        When I click on Detail tab
        When I select Bucket Tab
        Then I Confirm user Can Switch Between Buckets
        When I select override Tab
        When I click on Approval Tab    
        When I click on Finalization Tab
        Given I select file templates option under global from the burger menu
        Then I click on file templates
        Then I click on GP mappings
        Then I navigate to global price type
        Then I navigate to all screens under client
        Then I navigate to all screens under users
        Then I navigate to clients
        Given I select data dictionary option under client from the burger menu
        Then I click on data dictionary table
        Given I select Viewdata from the burger menu
        When I navigate through all resources of view data screen
        When I select price type editor from burger menu
        Then I navigate to all tabs under price type editor
        When I select price rebate transfter from hamburger menu
        When I select Approvals from burger menu
        Then I navigate to Uploads Screen
        Then I navigate to run tracker
        When I log out
    Examples: 
        |sheet|scenario_id|tc_id|
        |Screen_Load_Time|Screen_load_SC_01|TC1|

   