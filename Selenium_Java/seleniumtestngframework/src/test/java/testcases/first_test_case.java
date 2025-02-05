package testcases;

import org.testng.Assert;
import org.testng.annotations.Test;
import pages.FirstPage;
import setup.BaseSetup;
import utilities.CSVUtilities;

import java.util.Map;

public class first_test_case extends BaseSetup {

    @Test(groups = {"smoke"})
    public void testValidLogin_1() {
        testLogin("enterUserName");
    }

    @Test(groups = {"smoke"})
    public void testValidLogin_2() {
        testLogin("enterUserName");
    }

    @Test(groups = {"smoke"})
    public void testValidLogin_3() {
        testLogin("enterUserName");
    }

    @Test(groups = {"smoke"})
    public void testValidLogin_4() {
        testLogin("enterUserName");
    }

    @Test(groups = {"smoke"})
    public void testValidLogin_5() {
        testLogin("enterUserName");
    }

    private void testLogin(String usernameKey) {
        try (CSVUtilities csv = new CSVUtilities()) {
            Map<String, String> testData = csv.readData();

            if (testData == null) {
                Assert.fail("Failed to load test data. Check CSV file and setup.");
                return;
            }

            if (!testData.containsKey(usernameKey)) {
                Assert.fail("Key '" + usernameKey + "' not found in test data. Available keys are: " + testData.keySet());
                return;
            }

            String username = testData.get(usernameKey);

            FirstPage loginPage = new FirstPage(driver);
            loginPage.enterUsername(username);

            // Add your assertions or other test logic here.  For example:
            // Assert.assertEquals(driver.getTitle(), "Expected Title");

        } catch (RuntimeException e) {
            System.err.println("Error in test: " + e.getMessage());
            e.printStackTrace();
            Assert.fail("Test failed due to data loading error: " + e.getMessage());
        }
    }
}






































//package testcases;
//
//import org.testng.Assert;
//import org.testng.annotations.Test;
//import pages.FirstPage;
//import setup.BaseSetup;
//import utilities.CSVUtilities; // Make sure this import is correct
//
//import java.util.Map;
//
//public class first_test_case extends BaseSetup {
//
//    @Test(groups = {"smoke"})
//    public void testValidLogin_1() {
//        testLogin("enterUserName"); // Pass the key for the username
//    }
//
//    @Test(groups = {"smoke"})
//    public void testValidLogin_2() {
//        testLogin("enterUserName"); // Pass the key for the username
//    }
//
//    @Test(groups = {"smoke"})
//    public void testValidLogin_3() {
//        testLogin("enterUserName"); // Pass the key for the username
//    }
//
//    @Test(groups = {"smoke"})
//    public void testValidLogin_4() {
//        testLogin("enterUserName"); // Pass the key for the username
//    }
//
//    @Test(groups = {"smoke"})
//    public void testValidLogin_5() {
//        testLogin("enterUserName"); // Pass the key for the username
//    }
//
//    private void testLogin(String usernameKey) {
//        try (CSVUtilities csv = new CSVUtilities()) {
//            Map<String, String> testData = csv.readData();
//
//            if (testData == null) {
//                Assert.fail("Failed to load test data. Check CSV file and setup.");
//                return;
//            }
//
//            // Check if the key exists *before* using it
//            if (!testData.containsKey(usernameKey)) {
//                Assert.fail("Key '" + usernameKey + "' not found in test data. Available keys are: " + testData.keySet());
//                return; // Stop execution if key is missing
//            }
//
//            String username = testData.get(usernameKey); // Safe to get the value now
//
//            FirstPage loginPage = new FirstPage(driver);
//            loginPage.enterUsername(username);
//
//            // Add your assertions or other test logic here.  For example:
//            // Assert.assertEquals(driver.getTitle(), "Expected Title");
//
//        } catch (RuntimeException e) {
//            System.err.println("Error in test: " + e.getMessage());
//            e.printStackTrace();
//            Assert.fail("Test failed due to data loading error: " + e.getMessage());
//        }
//    }
//}