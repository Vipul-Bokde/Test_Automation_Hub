Feature: Smoke Test
    Background:
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application

    # behave GP\automation_test\behave\features\Smoke_Test_Suite.feature --tags=@Smoke_Test
    @Smoke_Test
    Scenario Outline: Smoke Test
        # Given Check for Validation errors
        Given click on upload button on overview page
        When select FileType from dropdown and click on Submit for the given "<TC_ID>" 
        When user should be navigate to upload screen then I see the product file that was uploaded
        Then I take data from uploaded file 
        When I navigate back to view data screen
        Then I crosscheck the data 
        When I click on the select run
        When I click on new run
        When I enter new run detail
        Then I submit the new run
        When I select the run name
        Then I click on execute all
        Then I confirm that all results are ready  
        Then I disable bp (BPA) price type 
        When Click on Data Summary and Approve
        When I select the price type 
        When I Perform operations on Summary Tab
        When I click on Detail tab
        When I select the NDC9, bucket & Add Comment
        When I click on the Variance & Add comment, Export
        When I select Bucket Tab
        Then I Confirm user Can Switch Between Buckets
        Then I Confirm the Bucket Export
        When I select override Tab
        Then I add new override detail
        When I select the override and click on edit override
        Then I edit the override details
        Then I select the override and delete Overide
        When I click on Summary Tab
        When I click on Approve
        When I click on Approval Tab
        When I select the price type
        Then I click on the Rollback 
        When I click on select run
        When I select the run name
        When I select the price type
        When I click on Approve
        When I click on Approval Tab
        When I select the price type
        When Perform operations on Summary Tab
        When I click on Detail tab
        When I select the NDC9, bucket & Add Comment
        When I select Bucket Tab
        Then I Confirm user Can Switch Between Buckets
        When I log out
        When I login with the different User
        When I click on select run
        When I select the run name
        When I click on Approval Tab
        When I select the price type
        When I click on Approve
        When I click on Finalization Tab
        When I select the price type
        When I Perform the operations on Summary Tab
        Then I click on the Rollback
        When I click on Approval Tab
        When I select the price type
        When I click on Approve
        When I click on Finalization Tab
        When I select the price type
        Then I click the Final Delivered
        When I log out
        When I login with the original User
        When I click on select run
        When I select the run name with closed status
        Then I click on the create restatement
        When I click on select run
        Then I ensure the restatement execution
        When I click on select run
        When I click on new run
        When I enter new run Details for Assessment Run
        Then I submit the new run
        When I select the assessment only run name
        Then I disable bp (BPA) price type 
        Then I click on execute all
        When I select the result ready price type and click on it
        Then I check that Assessment run can not be approved
        When I click on select run
        Then I select the delete run name and delete
        When I log out
    Examples:
        |TC_ID|
        # Direct Sales   
        |TC1|