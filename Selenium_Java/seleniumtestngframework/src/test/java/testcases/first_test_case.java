package testcases;
import org.testng.annotations.Test;
import pages.FirstPage;
import setup.BaseSetup;

public class first_test_case extends BaseSetup {

    @Test
    public void testValidLogin() {
        FirstPage loginPage = new FirstPage(driver);
        loginPage.enterUsername("testuser");
    }
}
