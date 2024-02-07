
# System Overview
The test automation framework has been created to facilitate the design, and the execution of the automated tests for Integrichain’s projects; it allows performing automated tests in different levels.

## Prerequisites

1. Install Python 3.7 or higher
1. Install pyenv(https://github.com/pyenv/pyenv#installation)

## Configuration

For the correct automation of the current projects these steps must be followed:

1. pip install selenium
2. pip install allure-behave
3. Configure the virtual environment ( it is recommended to use pipenv for this)
4. We prepared a requirement file: Execute the `pip install -r requirements.txt` command on the root to install the dependencies
5. Execute the tests using Python behave commands


# How to run the tests locally

To run these tests locally with Docker. After cloning the repository, go to the `ui_test` folder and install the dependencies from the `requirements.txt` file.

Get into the infrastructure folder and run the script `dockerExecution.sh`
```
$ ./dockerExecution.sh
```

There are two main global variables that need to be set as following:
```
$ export LOAD_BALANCER_NAME=http://localhost:4444
$ export BROWSER_NAME=CHROME
```
The BROWSER_NAME variable can be CHROME, FIREFOX or EDGE.

Also, before running the tests it is important set other global variables, since it is necessary to get certain required information through the `Sparc API`. The variables are as follows:
- `ENV_NAME`: refers to the environment where you want to run the tests, for example `dev`, `dev3`, `dev4` or `uat`.
- `SPARC_USER_NAME` and `SPARC_PASSWORD`: username and password to login.
- `SPARC_SERVICE_NAME` and `SPARC_CLIENT_NAME`: name of the service and client to use, as it appears in the user interface.

Example:
```
$ export ENV_NAME=dev4
$ export SPARC_USER_NAME=lu******
$ export SPARC_PASSWORD=l******
$ export SPARC_SERVICE_NAME=Medicaid
$ export SPARC_CLIENT_NAME='Dermira Inc.'
```

Now, to run the test it is necessary to be located in the `ui_test` directory and execute `Python behave` commands: 
```
$ behave directory/file.feature
```
Example:
```
$ behave Medicaid/automation_test/behaves/features/invoice.feature
```

Or you can use the bash script to run the test and call the allure reports service:

The first argument is the feature to be run, and the second one is the project where the feature belongs, in lower case.

Examples:
```
$ bash run.sh login_steps.feature medicaid

$ bash run.sh gen_login.feature ubr
```
Or you can execute the feature directly
```
$ behave  -f allure_behave.formatter:AllureFormatter -o AllureReport medicaid/automation_test/behave/features/login_steps.feature
 
$ python send_allure_report.py localhost icyte-sparc-medicaid /AllureReport
```

**Note:** If you want to run a specific test, all scenarios have `tags` that you can see in the `feature` file before each one. To use them, they are listed after the commands shown above.

Examples:
```
$ behave Medicaid/automation_test/behaves/features/invoice.feature --tags=create_invoice
```
or to execute with the allure report
```
$ behave  -f allure_behave.formatter:AllureFormatter -o AllureReport medicaid/automation_test/behave/features/invoice.feature --tags=create_invoice
```

# How to run the tests remotely (Jenkins)

To run these tests remotely using Jenkins, follow the steps:

1. Go to the [icyte-sparc](https://devjenkins.integrichain.net/job/icyte-sparc/) project.
2. Search for the current branch you are working on, for example [release/3.18.0.0](https://devjenkins.integrichain.net/job/icyte-sparc/job/release%252F3.18.0.0/).
3. Click `Build with Parameters` option, and provide the following information:
- `UI_TESTING` or `edge Testing` depending on which browser is going to run the tests.
- In `feature` fill out the feature name, for example `login_test` or `*` for running all features.
- In `SELENIUM_ENV` fill out the environment where you want to run the tests, for example `dev`, `dev3`, `dev4` or `uat`.
- Any other field could be left intact (empty or null).
4. Click `Build` and the job will start its execution.