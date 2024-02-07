
export LOAD_BALANCER_NAME=http://localhost:4444
export BROWSER_NAME='chrome'
#export LOAD_BALANCER_NAME=https://test-selenium-grid.integrichain.net/grid/console
export WORKING_DIR='AllureReport'
echo 'Deleting previous report results...'
if [ -d "$WORKING_DIR" ]; then rm -Rf $WORKING_DIR; fi
echo 'Running SELENIUM  Scenario...'
if [ "$2" = 'medicaid' ]; then export STEP="Medicaid/automation_test/behave/features/$1"
elif [ "$2" = 'ubr' ]; then export STEP="UBR/automation_test/behave/features/$1"; fi
behave  -f allure_behave.formatter:AllureFormatter -o AllureReport $STEP
echo 'Sending Results'
export BUILD_URL='LOCALHOST'
echo $BUILD_URL
export PROJECT_ID="icyte-sparc-$2"
export TRAIL_SLASH="/"
python  send_allure_report.py $BUILD_URL $PROJECT_ID "/"$WORKING_DIR
echo 'DONE...'
echo 'Deleting  report results...'
if [ -d "$WORKING_DIR" ]; then rm -Rf $WORKING_DIR; fi
