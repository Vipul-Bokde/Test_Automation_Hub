package testcases;

import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;
import pages.FirstPage;
import setup.BaseSetup;
import utilities.PageMethodExecutor;

public class Home_Page_Test extends BaseSetup {

	private FirstPage firstPage;
	private PageMethodExecutor executor;

	@BeforeMethod(alwaysRun = true)
	public void setupPage() {
		firstPage = new FirstPage(driver);
		executor = new PageMethodExecutor();
	}

	@Test(groups = { "smoke" })
	public void testValidLogin_1() {
		executor.executePageMethod(firstPage, "validateSearchBox", "searchBox");
		executor.executePageMethod(firstPage, "clickOnSearchButton");
		executor.executePageMethod(firstPage, "validateSearchBox", "sweetName");
		executor.executePageMethod(firstPage, "clickOnSearchButton");
	}
}
