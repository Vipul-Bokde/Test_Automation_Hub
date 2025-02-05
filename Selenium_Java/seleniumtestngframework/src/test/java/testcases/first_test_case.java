package testcases;

import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;
import pages.FirstPage;
import setup.BaseSetup;
import utilities.ExcelUtilities;
import java.util.Map;

public class first_test_case extends BaseSetup {
    private Map<String, String> testData;

    @BeforeClass
    public void setUpTestData() {
    	ExcelUtilities excel = new ExcelUtilities("HomePage"); // Load "HomePage" sheet
        testData = excel.readData();
        excel.closeWorkbook();
    }

    @Test(groups = {"smoke"})
    public void testValidLogin_1() {
        FirstPage loginPage = new FirstPage(driver);
        loginPage.enterUsername(testData.get("enterUserName"));
    }

    @Test(groups = {"smoke"})
    public void testValidLogin_2() {
        FirstPage loginPage = new FirstPage(driver);
        loginPage.enterUsername(testData.get("enterUserName"));
    }

    @Test(groups = {"sanity"})
    public void testValidLogin_3() {
        FirstPage loginPage = new FirstPage(driver);
        loginPage.enterUsername(testData.get("enterUserName"));
    }

    @Test(groups = {"sanity"})
    public void testValidLogin_4() {
        FirstPage loginPage = new FirstPage(driver);
        loginPage.enterUsername(testData.get("enterUserName"));
    }
}
