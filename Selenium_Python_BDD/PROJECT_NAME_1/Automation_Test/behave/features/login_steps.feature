Feature: GP Login
  # behave GP\automation_test\behave\features\login_steps.feature 
  Scenario: login
        Given Initialize testdata for "CREDENTIALS_QA" "SC_1" and "TC1"
        Given As a user login into the application
        When I login into the application
        When I select a config to the environment
        Then I enter the application


