Feature: Run Creation Feature

    Background:
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application

    # *****Run Creation*****
    # The run created here is taken as input for the whole run screen
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Run_Creation_New_Run
    @Run_Creation_New_Run
    Scenario Outline: Run Creation - New Run
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I click on new run
        When I enter new run details
        Then I submit new run
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_01|TC1|

   # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Confirm_All_Results_Ready_with_all_popups_for_all_standard_price_types
    # For the created run check results ready for all price type and verify confirmation popups
    @Confirm_All_Results_Ready_with_all_popups_for_all_standard_price_types
    Scenario Outline: Confirm All Results Ready - with all popups handling for all standard price types
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        Then I verify result ready for price type and all popups
        When I get analysis price type stage count
        When I filter run name
        Then I verify analysis price type stage count with run overview screen count
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_01|TC1|

    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Run_Creation_Execute_All
    # Click on execute all and verify confirmtion popups
    @Run_Creation_Execute_All
    Scenario Outline: Run Creation - Execute_All
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        Then I see version column is displayed
        Then I click on execute all
        Then I verify execute all confirmation popups
        Then I verify result ready for price type and all popups
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_01|TC1|

    # *****Summary Tab*****
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Run_Creation_Summary_Tab_Operations
    # Summary Tab operations and verifications of downloaded files
    @Run_Creation_Summary_Tab_Operations
    Scenario Outline: Run Creation - Summary Tab Operations
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        When I select price type
        Then I verify rollback button is disabled in summary tab
        When Perform operations on Summary Tab and verify downloaded file
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_01|TC1|

    # *****Detail Tab*****
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@After_Run_Creation_Detail_Tab_Operations
    #To run this Scenario->All Price Type Should be is Result Ready Stage & variance Should have records (Based on Run_Creation_Execute_All Scenario) 
    @After_Run_Creation_Detail_Tab_Operations
    Scenario Outline: Run Creation - Detail Tab Operations
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        When I select price type
        When I click on Detail tab
        When I select NDC9, bucket & Add Comment and edit the comment , and delete the comment
        When I select NDC9, bucket & Add Comment and verify added comment and verify data is valid as per selection
        When I click on a bucket
        Then I verify lower grid has close panel,new tab and export option
        Then I verify lower grid close panel working properly
        When I click on Variance & Add comment, Export and verify downloaded file
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_01|TC1|

    
    # *****Detail Tab/Lower Grid*****
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@After_Run_Creation_Detail_Tab_Lower_Grid_Operations
    #To run this Scenario->All Price Type Should be is Result Ready Stage(Based on Run_Creation_Execute_All Scenario) 
    @After_Run_Creation_Detail_Tab_Lower_Grid_Operations
    Scenario Outline: Run Creation - Detail Tab Operations
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        When I select price type
        When I click on Detail tab
        When I select NDC9, bucket
        When I click on a bucket
        When I click on Export button on lower grid tab
        When I click on new tab button on lower grid tab
        Then I verify new tab is having export functionality
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_01|TC1|

    # *****Bucket Tab*****
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Run_Creation_Bucket_Confirm_Can_Switch_Between_Buckets
    # switching between tabs can take more time base on data.
    @Run_Creation_Bucket_Confirm_Can_Switch_Between_Buckets
    Scenario Outline: Run Creation - Confirm Can Switch Between Buckets
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        When I select price type
        #When I select result ready price type and click on it
        When I select Bucket Tab
        Then I Confirm user Can Switch Between Buckets
        Then I Confirm Bucket Filter/Sort
        When I select any bucket and click on request NDC9 report
        When I select source and NDC9 and submit the request
        When I click on summary tab and click on attachments button
        Then I verify report is generated in attachments popup
        When I select Bucket Tab
        Then I Confirm Bucket Export and verify downloaded file
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_01|TC1|

    # *****Bucket Tab Exclude Include Scenario*****
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Run_Creation_Bucket_Include_Exclude
    # Exclude Include Scenario for any bucket
    # Run Name: 2022_Q3_CMS_VA (If this run does not exists then use a run with buckets tab having data)
    @Run_Creation_Bucket_Include_Exclude
    Scenario Outline: Run Creation - Bucket Include Exclude
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        When I select price type
        #When I select result ready price type and click on it
        When I select Bucket Tab
        Then I exclude record and verify record excluded
        When I click on Analysis Tab
        Then I verify result ready for selected price type and all popups
        When I select price type
        When I select Bucket Tab
        Then I include record and verify record included
        When I click on Analysis Tab
        Then I verify result ready for selected price type and all popups
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_include_exclude_scenario|TC1|

    # *****Bucket Tab Exclude Scenario*****
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Run_Creation_Bucket_Exclude_And_Verify_Comments_In_Exported_Report
    # Exclude Scenario for any bucket
    # Run Name: 2022_Q3_CMS_VA (If this run does not exists then use a run with buckets tab having data)
    @Run_Creation_Bucket_Exclude_And_Verify_Comments_In_Exported_Report
    Scenario Outline: Run Creation - Bucket Exclude and Vedrify Comments in Exported file
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        When I select price type
        #When I select result ready price type and click on it
        When I select Bucket Tab
        Then I exclude record and verify record excluded
        Then I click on export button and verify comments from exported file
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_include_exclude_scenario|TC1|

    # *****Override tab*****
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Run_Creation_Override_Confirm_Add_New_Override
    #Add new overrride
    @Run_Creation_Override_Confirm_Add_New_Override 
    Scenario Outline: Run Creation - Confirm Add New Override  
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>" 
        When I click on select run
        When I select run name
        Then I verify result ready for price type and all popups
        When I select price type
        #When I select result ready price type and click on it
        When I select override Tab
        Then I add new override details
        Then I verify red triangle on override tab
        When I click on Analysis Tab
        Then I verify result ready for price type and all popups
        When I select price type
        Then I verify dollar and unit amounts
        When I select override Tab
        Then I verify after re-execution red triangle should be removed
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_01|TC1|

    # repeatative feature need to remove and add these 3 steps into add/edit/delete override features once override works properly
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Run_Creation_Override_Confirm_Summary_Asks_to_Re-Execute_After_Override
    # @Run_Creation_Override_Confirm_Summary_Asks_to_Re-Execute_After_Override
    # Scenario: Run Creation - Confirm Summary Asks to Re-Execute After Override
    #     When I click on select run
    #     When I select run name
    #     Then I Confirm Summary Asks to re execute

    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Run_Creation_Override_Edit_Override
    # Edit existing override
    @Run_Creation_Override_Edit_Override
    Scenario Outline: Run Creation - Confirm Edit Override
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        Then I verify result ready for price type and all popups
        When I select price type
        #When I select result ready price type and click on it
        When I select override Tab
        When I select override and click on edit override
        Then I edit override details
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_01|TC1|

    # # behave GP\automation_test\behave\features\gp_run_creation.feature --tags @Run_Creation_Override_Confirm_Summary_Asks_to_Re-Execute_After_Edit_Override
    # @Run_Creation_Override_Confirm_Summary_Asks_to_Re-Execute_After_Edit_Override
    # Scenario: Run Creation - Confirm Summary Asks to Re-Execute After Edit Override
    #     When I click on select run
    #     When I select run name
    #     Then I Confirm Summary Asks to re execute

    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Run_Creation_Override_Remove_Override
    # Delete added override
    @Run_Creation_Override_Remove_Override
    Scenario Outline: Run Creation - Confirm Remove Override   
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        Then I verify result ready for price type and all popups
        When I select price type
        #When I select result ready price type and click on it
        When I select override Tab
        Then I select override and delete Overide
        Then I verify count on override button should be removed
        Then I click on Export
        Then I verify downloaded file
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_01|TC1|

    # # behave GP\automation_test\behave\features\gp_run_creation.feature --tags @Run_Creation_Override_Confirm_Summary_Asks_to_Re-Execute_After_Remove_Override
    # @Run_Creation_Override_Confirm_Summary_Asks_to_Re-Execute_After_Remove_Override
    # Scenario: Run Creation - Confirm Summary Asks to Re-Execute After Remove Override
    #     When I click on select run
    #     When I select run name
    #     Then I Confirm Summary Asks to re execute
       
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Click_on_Data_Summary_and_Approve
    # Approve Data summary price type due to which submitted by and submitted on columns get updated
    @Click_on_Data_Summary_and_Approve
    Scenario Outline: Run Creation - Click on Data Summary and Approve
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        Then I verify result ready for price type and all popups
        When Click on Data Summary and Approve
        When I get analysis and approval price type stage count for data summary when sent for approval
        When I filter run name
        Then I verify analysis and approval price type stage count with run overview screen count for data summary when sent for approval
        When I click on Approval Tab
        Then I verify stage as pending approval for data summary
        Then I verify submitted by and submitted on column for data summary
        When I log out
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_01|TC1|

    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Click_on_Data_Summary_and_Complete_Workflow_from_PendingApproval_To_Finalization
    # Data Summary Complete Workflow from Pending Approvl to Finalization
    @Click_on_Data_Summary_and_Complete_Workflow_from_PendingApproval_To_Finalization
    Scenario Outline: Run Creation - Data Summary Complete Workflow from PendingApproval To Finalization
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I log out
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application as a Manager
        When I select a config to the environment
        Then I enter the application
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        When I click on Approval Tab
        When I select price type
        When I click on Approve
        When I log out
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        When I click on Finalization Tab
        Then I verify version in stage cannot be changed and execution of price type is also not possible
        When I select price type
        Then I click Final Delivered
        Then I verify version in stage cannot be changed and execution of price type is also not possible
        When I log out
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_02|TC1|
    
    # *****Approval Screen PriceType Approve & Rollback for amp price type*****
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Summary_screen_price_type_Approve
    #After approve price type amp and rollback for amp then submitted by,submitted on ,rollback by, rollback on is affected
    @Summary_screen_price_type_Approve
    Scenario Outline: Price Type Approval
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        When I select price type
        When I click on Approve
        When I click on Approval Tab
        When I filter price type
        When I click on execute button
        Then I verify confirmation popup and click on yes button
        Then I verify message popup only price type in queue or analysis may be run and click on ok button
        Then I verify stage as pending approval for selected price type
        Then I verify submitted by and submitted on column for selected price type
        When I select price type
        When I click on Approve
        Then I verify message popup manager cannot approve both approvals
        When I click on Approval Tab
        When I filter price type
        When I click the disable button
        When I click on Analysis Tab
        Then I verify stage as disabled and execution status as disabled for this run
        When I click the enable button
        Then I verify result ready for price type and all popups
        When I select price type
        When I click on Approve
        When I click on Approval Tab
        When I select price type
        Then I click on Rollback
        When I click on Analysis Tab
        Then I verify rollback by and rollback on column for selected price type
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_01|TC1|


    # *****Approval Screen(Override Scenarios)*****
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Run_Creation_Override_Confirm_Add_New_Override_Approval_Screen
    #Add new overrride in analysis screen . Then approve the PT (amp). Then add/edit/delete override in approval screen
    # which shows errors messages.
    @Run_Creation_Override_Confirm_Add_New_Override_Approval_Screen
    Scenario Outline: Run Creation - Confirm Add New Override Approval Screen
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>" 
        When I click on select run
        When I select run name
        Then I verify result ready for price type and all popups
        When I select price type
        #When I select result ready price type and click on it
        When I select override Tab
        Then I add new override details
        When I click on Analysis Tab
        Then I verify result ready for price type and all popups
        When I select price type
        When I click on Approve
        When I click on Approval Tab
        When I select price type
        When I select override Tab
        Then I add new override details
        Then I verify popup Only Price Types in queued or analysis may be overridden
        When I select override and click on edit override
        Then I edit override details
        Then I verify message Only Price Types in queued or analysis may have their overrides altered
        Then I select override and delete Overide
        Then I verify message Only Price Types in queued or analysis may have their overrides altered
        When I click on Approval Tab
        When I select price type
        Then I click on Rollback
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_01|TC1|

    # *****Approval Screen PriceType Submitt & Approval screen price type approved***** 
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Approval_screen
    @Approval_screen
    Scenario Outline: Approval Screen
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        When I select price type
        When I click on Approve
        When I click on Approval Tab
        Then I verify stage as pending approval for selected price type
        Then I verify submitted by and submitted on column for selected price type
        When I select price type
        When Perform operations on Summary Tab
        When I click on Detail tab
        When I select NDC9, bucket & Add Comment and verify added comment and verify data is valid as per selection
        When I select Bucket Tab
        Then I Confirm Bucket Filter/Sort
        When I log out
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application as a Manager
        When I select a config to the environment
        Then I enter the application
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        When I click on Approval Tab
        When I select price type
        When I click on Approve
        When I click on Finalization Tab
        Then I verify stage as approved for selected price type
        Then I verify approved by and approved on column for selected price type
        When I log out
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_01|TC1|

    # *****Finalization Screen PriceType Finalization Rollback*****
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Finalization_screen_rollback
    @Finalization_screen_rollback
    Scenario Outline: Finalization Screen
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        When I click on Finalization Tab
        Then I verify execute button is disabled in finalization tab
        When I select price type
        When Perform operations on Summary Tab
        Then I click on Rollback
        When I click on Approval Tab
        Then I verify rollback by and rollback on column for selected price type for approval stage
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_01|TC1|

    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Finalization_screen_Delivered
    @Finalization_screen_Delivered
    Scenario Outline: Finalization Screen
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I log out
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application as a Manager
        When I select a config to the environment
        Then I enter the application
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name
        When I click on Approval Tab
        When I select price type
        When I click on Approve
        When I click on Finalization Tab
        Then I verify stage as approved for selected price type
        Then I verify approved by and approved on column for selected price type
        When I select price type
        Then I click Final Delivered
        When I click on Finalization Tab
        Then I verify stage as delivered for selected price type
        Then I verify delivered by and delivered on column for selected price type
        When I select price type
        Then I verify buttons mark as delivered and rollback are disabled
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_01|TC1|

    # *****Close Run (With Price type as Data Summary and AMP) and verify Status changed to closed*****
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Close_Run_Verify_Closed_Status
    # for this scenario all above scenarios need to executed.
    @Close_Run_Verify_Closed_Status
    Scenario Outline: Run Screen - Close Run and Verify Closed Status
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I filter run name
        When I click on checkbox and close run
        Then I verify run name is having closed status
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_SC_01|TC1|

    # *****Assessment Run Creation*****
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Run_Creation_New_Run_with_assessment_run
    @Run_Creation_New_Run_with_assessment_run
    Scenario Outline: Run Creation - New Run with Assessment Run
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I click on new run
        When I enter new run Details with Assessment Run
        Then I submit new run
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_ass_SC_01|TC1|

    # *****Assessment Run Price type Setting Popup*****
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Assessment_run_Price_Type_Setting_Popup
    # Go to price type editor and take only those price type which is having status as active.
    @Assessment_run_Price_Type_Setting_Popup
    Scenario Outline: Run Creation - New Run with Assessment Run
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I filter assessment run name
        When I filter price type
        When I verify pencil icon is displayed and click on pencil icon
        Then I verify label under price type setting popup
        When I select price type editor from burger menu
        Then Open the created price type
        When I click on revision history tab
        When I get the version count
        When I click on select run
        When I filter assessment run name
        When I filter price type
        When I verify pencil icon is displayed and click on pencil icon
        Then I verify user can see all versions of that price type
        When I select the latest price type and click on save button
        Then I verify result ready for selected price type and all popups
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_ass_SC_01|TC1|
        
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Run_Creation_Ensure_Assessment_Only_Run_Executes
    @Run_Creation_Ensure_Assessment_Only_Run_Executes
    Scenario Outline: Run Creation - Ensure Assessment Only Run Executes
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select assessment only run name
        Then I disable bp (BPA) price type
        Then I click on execute all
        When I log out
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_ass_SC_01|TC1|

    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Run_Creation_Ensure_Assessment_Only_Run_Cannot_Be_Approved
    @Run_Creation_Ensure_Assessment_Only_Run_Cannot_Be_Approved
    Scenario Outline: Run Creation - Ensure Assessment Only Run Cannot Be Approved
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select assessment only run name
        When I select result ready price type and click on it
        Then I check Assessment run can not be approved
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_ass_SC_01|TC1|
    
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Run_Creation_Delete_Run
    @Run_Creation_Delete_Run
    Scenario Outline: Run Creation - Run_Creation_Delete_Run
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        Then I select delete run name and delete
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_delete_SC_01|TC1|

    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Deletion_Of_Run_Already_Exists
    # If the name already in use or run already exists does not occur the only create new run and verify new run and created on date
    @Deletion_Of_Run_Already_Exists
    Scenario Outline: Run Delation - Deletion_Of_Run_Already_Exists
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I click on new run
        When I enter new run details
        Then I submit new run
        Then if I see name already exists or run already exists in new run popup page I delete the existing run and create new run
        Then I verify new run and created on date
        Then I delete run
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_delete_SC_02|TC1|
       |GP_Run_Feature|run_delete_SC_02|TC2|
       |GP_Run_Feature|run_delete_SC_02|TC3|
       
    # *****Closed Run and Restatement*****
    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Run_Creation_Take_Closed_Run_and_Create_Restatement
    # In Test Data Sheet add a run name which is having status closed.
    @Run_Creation_Take_Closed_Run_and_Create_Restatement
    Scenario Outline: Run Creation - Take Closed Run and Create Restatement
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        When I select run name with closed status
        Then I click on create restatement
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_restatement_SC_01|TC1|

    # behave GP\automation_test\behave\features\gp_run_creation.feature --tags=@Run_Creation_Ensure_Restatement_Execution
    @Run_Creation_Ensure_Restatement_Execution
    Scenario Outline: Run Creation - Ensure Restatement Execution
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I click on select run
        Then I ensure restatement execution
        When I click on select run
        When I select run name with closed status filter
        When I get price type and version from closed run
        When I click on select run
        When I select re-statement run name
        When I filter price type for restatement
        Then I verify re-statement newly created run should show same tagged version as original one
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Run_Feature|run_restatement_SC_01|TC1|