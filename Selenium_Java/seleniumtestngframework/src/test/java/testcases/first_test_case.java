package testcases;
import org.testng.annotations.Test;
import pages.firstpage;
import setup.BaseSetup;

public class first_test_case extends BaseSetup {

    @Test
    public void testValidLogin() {
        firstpage loginPage = new firstpage(driver);
        loginPage.enterUsername("testuser");
    }
}
