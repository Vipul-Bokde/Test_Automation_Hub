Feature: Create new mapping under global file templates

    Background:
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application

    # behave GP\automation_test\behave\features\reports.feature --tags=@Download_reports
	@Download_reports
    Scenario Outline: Download the credit balance report
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select credit balance report option under reports menu
        Then I verify credit balance report data
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Reports_Feature|Control_and_Reasonability_Report_SC_01|TC1|


    # Before executing this scenario add the credentials of the DB for perfqa and also change the 
    # Env in excel for perfqa
    # behave GP\automation_test\behave\features\reports.feature --tags=@Control_and_Reasonability_Report
	@Control_and_Reasonability_Report
    Scenario Outline: Control and Reasonability Report
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select Control and Reasonability Report option under reports menu
        When I select current date and prior date
        Then I verify prior date is less than current date
        Then I click on submit button
        Then I verify headers and data from excel and DB
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Reports_Feature|Control_and_Reasonability_Report_SC_01|TC1|


    # Before executing this scenario add the credentials of the DB for qa and also change the 
    # Env in excel for qa
    # Before executing this scenario execute gp.runscreen.feature file or a run which
    # have entire workflow from analysis to finalization screen
    # behave GP\automation_test\behave\features\reports.feature --tags=@Calc_Audit_Log_Report
	@Calc_Audit_Log_Report
    Scenario Outline: Calc Audit Log Report
        Given Initialize testdata for "<sheet>" "<scenario_id>" and "<tc_id>"
        Given I select Calc Audit Log Report option under reports menu
        When I select Start date and end date
        Then I click on submit button for cal audit log
        Then I verify headers and data from excel and DB for cal audit log
    Examples:
       |sheet|scenario_id|tc_id|
       |GP_Reports_Feature|Control_and_Reasonability_Report_SC_01|TC1|