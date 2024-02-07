Feature: Approvals Functionality
    In this feature are the scenarios related to the approval and reject process.
    Background:
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application
        
    # behave GP\automation_test\behave\features\approvals.feature --tags @Approval
    @Approval
    Scenario Outline: Approve the GP price type, pricing, product
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select Approvals from burger menu
        When I select client and type from dropdown
        Then Select given value and approve
        Examples:
        |sheet|scenario_id|tc_id|
        # Approve GP Price Type 
        |GP_Approval_Feature|Approve_sc_01|TC1|
        # Approve pricing
        |GP_Approval_Feature|Approve_sc_01|TC2|
        # Approve product
        |GP_Approval_Feature|Approve_sc_01|TC3|

        
    # behave GP\automation_test\behave\features\approvals.feature --tags @Rejection
    @Rejection
    Scenario Outline: Reject the GP price type, pricing, product
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        When I select Approvals from burger menu
        When I select client and type from dropdown
        Then Select price type and reject
        Examples:
        |sheet|scenario_id|tc_id|
        # Reject GP Price Type 
        |GP_Approval_Feature|Reject_sc_01|TC1|
        # Reject pricing
        |GP_Approval_Feature|Reject_sc_01|TC2|
        # Reject product
        |GP_Approval_Feature|Reject_sc_01|TC3|
