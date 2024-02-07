Feature: Product 
        In this feature is related to the upload the product files in 
        upload page.

    Background:
        Given Initialize testdata for "GP_Product_Feature" "Product_validate_SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application

    # behave GP\automation_test\behave\features\product.feature
    # close all Test_Data_Sheet and Product Upload files.
    @Upload_Product_and_validate
    Scenario Outline: Upload_Product_and_validate
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select Upload from burger menu
        When I upload product file and get ndc11 value
        When I log out
        Given As a user login into the application
        When I login into the application as a Manager
        When I select a config to the environment
        Then I enter the application
        When I Approve Product
        When I goes to changes tab 
        When I validate changes tab
    Examples:
        |sheet|scenario_id|tc_id|
        |GP_Product_Feature|Product_validate_SC_1|TC1|

        
        

