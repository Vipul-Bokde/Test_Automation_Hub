package testcases;
import org.testng.annotations.Test;
import pages.FirstPage;
import setup.BaseSetup;

public class first_test_case extends BaseSetup {
	

	@Test(groups = {"smoke"})
    public void testValidLogin_1() {
        FirstPage loginPage = new FirstPage(driver);
        loginPage.enterUsername("testuser");
    }
	
	@Test(groups = {"smoke"})
    public void testValidLogin_2() {
        FirstPage loginPage = new FirstPage(driver);
        loginPage.enterUsername("testuser");
    }
	

	@Test(groups = {"sanity"})
    public void testValidLogin_3() {
        FirstPage loginPage = new FirstPage(driver);
        loginPage.enterUsername("testuser");
    }
	
	@Test(groups = {"sanity"})
    public void testValidLogin_4() {
        FirstPage loginPage = new FirstPage(driver);
        loginPage.enterUsername("testuser");
    }
}
