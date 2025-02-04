package setup;

import java.util.Arrays;
import java.lang.reflect.Method;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.edge.EdgeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.safari.SafariDriver;
import org.testng.ITestContext;
import org.testng.ITestResult;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import io.github.bonigarcia.wdm.WebDriverManager;
import libraries.BrowserActions;
import utilities.ConfigReader;
import utilities.ExtentReportManager;

public class BaseSetup {
	protected WebDriver driver;
	private BrowserActions browserActions;
	private static final Logger logger = LogManager.getLogger(BaseSetup.class);

	@BeforeMethod(alwaysRun = true)
	public void setup(ITestContext context, Method method) {
		try {
			ExtentReportManager.initExtentReport();
			logger.info("Starting the test setup...");

			// Read browser name from config file
			String browser = ConfigReader.getProperty("browser");
			String url = ConfigReader.getProperty("base.url");

			// Get suite, test method name & test description
			String suiteName = context.getSuite().getName();
			String testMethodName = method.getName(); // ✅ Fetching actual test method name
			String[] groups = context.getIncludedGroups();
			String groupNames = (groups.length > 0) ? Arrays.toString(groups) : "No Groups Defined";

			/*
			 * long threadId = Thread.currentThread().getId();
			 * logger.info("Executing test on thread: " + threadId);
			 * ExtentReportManager.logInfo("Test running on thread: " + threadId);
			 */

			// Explicitly log the suite name and method name
			String fullTestName = suiteName + " - " + testMethodName;
			ExtentReportManager.startTest(fullTestName, "Test Execution Started For " + testMethodName, groupNames);

//			ExtentReportManager.startTest(suiteName, "Test Execution Started For " + testMethodName, groupNames);
			// Log browser info and other setup details
			ExtentReportManager.logInfo("Selected browser: " + browser);
			logger.info("Selected browser: " + browser);

			// Check if running inside GitHub Actions
			boolean isCI = System.getenv("GITHUB_ACTIONS") != null;

			switch (browser.toLowerCase()) {
			case "chrome":
				WebDriverManager.chromedriver().setup();
				ChromeOptions chromeOptions = new ChromeOptions();
				if (isCI) {
					chromeOptions.addArguments("--headless", "--disable-gpu", "--window-size=1920,1080");
				}
				driver = new ChromeDriver(chromeOptions);
				break;
			case "edge":
				WebDriverManager.edgedriver().setup();
				EdgeOptions edgeOptions = new EdgeOptions();
				if (isCI) {
					edgeOptions.addArguments("--headless", "--disable-gpu", "--window-size=1920,1080");
				}
				driver = new EdgeDriver(edgeOptions);
				break;
			case "firefox":
				WebDriverManager.firefoxdriver().setup();
				FirefoxOptions firefoxOptions = new FirefoxOptions();
				if (isCI) {
					firefoxOptions.addArguments("--headless", "--disable-gpu", "--window-size=1920,1080");
				}
				driver = new FirefoxDriver(firefoxOptions);
				break;
			case "safari":
				if (isCI) {
					logger.error("Safari is not supported in GitHub Actions.");
					throw new UnsupportedOperationException("Safari is not supported in CI.");
				}
				driver = new SafariDriver();
				break;
			default:
				logger.error("Browser not supported: " + browser);
				throw new IllegalArgumentException("Browser not supported: " + browser);
			}

			driver.manage().window().maximize();
			driver.get(url);
			ExtentReportManager.logInfo("Browser opened successfully.");
			ExtentReportManager.logInfo(url + " opened successfully.");

			// Initialize BrowserActions
			browserActions = new BrowserActions(driver);
		} catch (Exception e) {
			logger.error("Error in setup: " + e.getMessage(), e);
			throw e; // Rethrow to fail the test
		}
	}

	@AfterMethod(alwaysRun = true)
	public void teardown(ITestResult result) {
		String testName = result.getName();
		String resultMessage = "";

		// Log the test method name again in UPPERCASE
		logTestMethodName(testName);

		// Handle test result logging
		if (result.getStatus() == ITestResult.SUCCESS) {
			resultMessage = testName + " passed successfully.";
			ExtentReportManager.logPass(resultMessage);
		} else if (result.getStatus() == ITestResult.FAILURE) {
			resultMessage = "Test failed with exception: " + result.getThrowable().getMessage();
			ExtentReportManager.logException(result.getThrowable());
		} else if (result.getStatus() == ITestResult.SKIP) {
			resultMessage = testName + " was skipped.";
			ExtentReportManager.logInfo(resultMessage);
		}

		// Common teardown steps
		ExtentReportManager.endTest();

		// ✅ Prevent NullPointerException for `browserActions`
		if (browserActions != null) {
			browserActions.quitBrowser();
		} else {
			logger.warn("BrowserActions is null, skipping browser quit.");
		}

		logger.info(resultMessage);
		ExtentReportManager.logInfo("Browser closed successfully.");
		ExtentReportManager.generateReportLink();
	}

	// Utility method to log test method name in UPPERCASE
	private void logTestMethodName(String testName) {
		if (testName != null) {
			String upperCaseTestName = testName.toUpperCase();
			logger.info("Executing Test: " + upperCaseTestName);
			ExtentReportManager.logInfo("Executing Test: " + upperCaseTestName);
		} else {
			logger.warn("Test method name is null, skipping log.");
		}
	}
}
