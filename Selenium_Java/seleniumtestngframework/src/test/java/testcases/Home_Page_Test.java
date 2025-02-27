package testcases;

import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

//import libraries.PerformanceUtils;
import pages.FirstPage;
import setup.BaseSetup;
import utilities.PageMethodExecutor;

public class Home_Page_Test extends BaseSetup {

	private FirstPage firstPage;
	private PageMethodExecutor executor;
//	private PerformanceUtils performanceUtils;

	@BeforeMethod(alwaysRun = true)
	public void setupPage() {
		firstPage = new FirstPage(driver);
		executor = new PageMethodExecutor();
//		performanceUtils = new PerformanceUtils(driver, "performance_benchmark 	 HJP[].csv");
	}

	@Test(groups = { "smoke" })
	public void testValidLogin_1() {
//		performanceUtils.capturePerformanceMetrics(driver.getCurrentUrl());
		executor.executePageMethod(firstPage, "validateSearchBox", "sweetName");
//		performanceUtils.capturePerformanceMetrics(driver.getCurrentUrl());
		executor.executePageMethod(firstPage, "clickOnSearchButton");
		executor.executePageMethod(firstPage, "exploresweetNameItem");
	}
}
