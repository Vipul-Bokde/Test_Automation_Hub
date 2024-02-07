Feature: GP DRS Bundle Definition Screen

    Background:
        Given Initialize testdata for "CREDENTIALS_QA" "SC_6" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application

    # behave GP\automation_test\behave\features\gp_drs_bundle.feature --tags=@GP_Bundle_create_and_validate_db
    @GP_Bundle_create_and_validate_db                 
    Scenario Outline: Create and Validate Bundle Definition 
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select Bundle Definition Editor option under DRS from the burger menu
        When  I validate Bundle Definition Screen Columns
        Then  I create and validate new bundle definition on bundle definition page
        When  I validate bundle definition name in database
        When  I log out
        Examples:
        |sheet|scenario_id|tc_id| 
        |GP_DRS_Bundle|Create_And_Add_Bundle_SC_1|TC1|

    # behave GP\automation_test\behave\features\gp_drs_bundle.feature --tags=@GP_Bundle_Definition_tab
    @GP_Bundle_Definition_tab               
    Scenario Outline: Navigate to definition tab and validates its elements
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select Bundle Definition Editor option under DRS from the burger menu
        Then  I click on a bundle
        When  I entered bundle defnition tab and validate its elements
        When  I log out
        Examples:
        |sheet|scenario_id|tc_id| 
        |GP_DRS_Bundle|Create_And_Add_Bundle_SC_1|TC1|


    # behave GP\automation_test\behave\features\gp_drs_bundle.feature --tags=@GP_Bundle_Contract_tab
    @GP_Bundle_Contract_tab               
    Scenario Outline: Navigate to contract and contract terms tab and validates its elements
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select Bundle Definition Editor option under DRS from the burger menu
        Then  I click on a bundle
        When  I navigate and click on contract tab
        When  I entered contract tab and validate its elements
        When  I navigate contract terms tab and validate its elements
        When  I validate contract number in database
        When  I validate contract_term name in database
        When  I log out
        Examples:
        |sheet|scenario_id|tc_id| 
        |GP_DRS_Bundle|Create_And_Add_Bundle_SC_1|TC1|

    # behave GP\automation_test\behave\features\gp_drs_bundle.feature --tags=@GP_Bundle_Contract_tab_Creation_Deletion
    @GP_Bundle_Contract_tab_Creation_Deletion               
    Scenario Outline: Navigate to contract tab and validates its elements including creation and deletion
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select Bundle Definition Editor option under DRS from the burger menu
        Then  I click on a bundle
        When  I navigate and click on contract tab
        When  I entered contract tab and validate its columns
        When  I entered contract_term tab and validate its columns
        When  I remove contract terms from contract tab
        When  I remove contract from contract tab
        When  I log out
        Examples:
        |sheet|scenario_id|tc_id| 
        |GP_DRS_Bundle|Create_And_Add_Bundle_SC_1|TC1|

    # behave GP\automation_test\behave\features\gp_drs_bundle.feature --tags=@GP_Bundle_Def_deletion
    @GP_Bundle_Def_deletion                 
    Scenario Outline: Delete Bundle Definition 
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select Bundle Definition Editor option under DRS from the burger menu
        Then  I delete bundle definition from bundle definition page
        When  I log out
        Examples:
        |sheet|scenario_id|tc_id| 
        |GP_DRS_Bundle|Create_And_Add_Bundle_SC_1|TC1|

    # behave GP\automation_test\behave\features\drs_automation.feature --tags=@DRS_Bundle_Customer_Product
    @DRS_Bundle_Customer_Product
    Scenario Outline: Customers and Products tab in Bundle Definition Editor
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select Bundle Definition Editor option under DRS from the burger menu
        Then  I click on a bundle
        Then I go to Customers tab
        Then I verify the headers of dropdowns
        Then I select the dropdown menu for Customer Grouping
        Then I select the dropdown menu for Customer Selection
        Then I click on save    
        Then I go to Products tab
        Then I verify the headers in products tab
        Then I click on Add Products Group
        Then I click on Cancel
        Then I click on Add Products Group
        Then I enter the valid Product Group name
        Then I click on submit button in products group tab
        Then I remove the product group
        Then I click on Add Products Group
        Then I enter the valid Product Group name
        Then I click on submit button in products group tab
        Then I edit the product group name using pencil icon
        Then I click on submit button in products group tab
        Then I select the option from Product selection dropdown
        Then I click on save
        When I click on Add Product
        Then I click on submit button in products list tab
        Then I click on save
        Then I click on Remove Product
        Then I click on save
        When  I log out        
        Examples:
        |sheet|scenario_id|tc_id|
        |GP_DRS_Bundle|Create_And_Add_Bundle_SC_1|TC1|

    # behave GP\automation_test\behave\features\gp_drs_bundle.feature --tags=@GP_Bundle_DataBucket_tab
    @GP_Bundle_DataBucket_tab               
    Scenario Outline: Navigate to databucket tab and validates its elements
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select Bundle Definition Editor option under DRS from the burger menu
        Then  I click on a bundle
        When  I navigate and click on data_bucket tab
        When  I navigate data bucket tab and validate its elements
        When  I log out
        Examples:
        |sheet|scenario_id|tc_id| 
        |GP_DRS_Bundle|Create_And_Add_Bundle_SC_1|TC1|

    # behave GP\automation_test\behave\features\gp_drs_bundle.feature --tags=@GP_Bundle_DataBucket_Creation_Deletion
    @GP_Bundle_DataBucket_Creation_Deletion               
    Scenario Outline: Navigate to databucket tab and validates its elements with creation and deletion
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select Bundle Definition Editor option under DRS from the burger menu
        Then  I click on a bundle
        When  I navigate and click on data_bucket tab
        When  I navigate data bucket tab and validate its elements
        When  I remove specific data bucket from data bucket tab
        When  I log out
        Examples:
        |sheet|scenario_id|tc_id| 
        |GP_DRS_Bundle|Create_And_Add_Bundle_SC_1|TC1|

    # behave GP\automation_test\behave\features\gp_drs_bundle.feature --tags=@GP_Bundle_Revision_History_Tab
    @GP_Bundle_Revision_History_Tab               
    Scenario Outline: Navigate to revision history tab and validates its elements
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select Bundle Definition Editor option under DRS from the burger menu
        Then  I click on a bundle
        When  I navigate and click on revision history tab
        When  I validate revision history tab columns
        When  I validate revision history data
        When  I log out
        Examples:
        |sheet|scenario_id|tc_id| 
        |GP_DRS_Bundle|Create_And_Add_Bundle_SC_1|TC1|

    # behave GP\automation_test\behave\features\gp_drs_bundle.feature --tags=@GP_DRS_BUNDLE_E2E_SCENARIO
    @GP_DRS_BUNDLE_E2E_SCENARIO            
    Scenario Outline: E2E Flow for Bundle Defintion creation and approval
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select Bundle Definition Editor option under DRS from the burger menu
        Then  I create and validate new bundle definition on bundle definition page
        Then  I click on a bundle
        When  I entered bundle defnition tab and validate its elements
        When  I navigate and click on contract tab
        When  I entered contract tab and validate its elements
        When  I navigate contract terms tab and validate its elements
        Then  I go to Customers tab
        Then  I select the dropdown menu for Customer Grouping
        Then  I select the dropdown menu for Customer Selection
        Then  I click on save 
        Then  I go to Products tab
        Then  I click on Add Products Group
        Then  I enter the valid Product Group name
        Then  I click on submit button in products group tab
        Then  I edit the product group name using pencil icon
        Then  I click on submit button in products group tab
        Then  I select the option from Product selection dropdown
        Then  I click on save
        When  I click on Add Product
        Then  I click on submit button in products list tab
        Then  I click on save
        When  I navigate and click on data_bucket tab
        When  I navigate data bucket tab and validate its elements
        # NOTE - HERE PLEASE ADD STEPS FOR PRICE TYPE TAB I.E USER STORY - GP-2129
        When  I navigate and click on revision history tab
        When  I validate revision history tab columns
        When  I validate revision history data
        Then  I submit bundle for approval
        When  I log out
        Given Initialize testdata for "CREDENTIALS_QA" "SC_2" and "TC1"
        Given As a user login into the application
        When  I login into the application as a Manager
        When  I select a config to the environment
        Then  I enter the application
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When  I select Approvals from burger menu
        When  I select client and type from dropdown
        Then  I select bundle name for approval and approve
        When  I log out
        Given Initialize testdata for "CREDENTIALS_QA" "SC_6" and "TC1"
        Given As a user login into the application
        When  I login into the application
        When  I select a config to the environment
        Then  I enter the application
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select Bundle Definition Editor option under DRS from the burger menu
        Then  I validate bundle status after approval
        Examples:
        |sheet|scenario_id|tc_id| 
        |GP_DRS_Bundle|Create_And_Add_Bundle_SC_1|TC1|