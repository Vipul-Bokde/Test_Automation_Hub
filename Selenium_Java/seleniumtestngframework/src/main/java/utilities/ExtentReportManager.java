package utilities;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.reporter.ExtentSparkReporter;
import com.aventstack.extentreports.reporter.configuration.Theme;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.awt.Desktop;
import java.io.File;
import java.io.IOException;
import java.net.URI;

public class ExtentReportManager {
	private static ExtentReports extent;
	private static final Logger logger = LogManager.getLogger(ExtentReportManager.class);
	private static ThreadLocal<ExtentTest> test = new ThreadLocal<>();

	// Initialize ExtentReports with ExtentSparkReporter
	public static ExtentReports initExtentReport() {
		if (extent == null) {
			String reportPath = ConfigReader.getProperty("extent.report.path");
			File file = new File(reportPath);
			File directory = file.getParentFile();
			if (!directory.exists()) {
				directory.mkdirs(); // Create the report directory if it doesn't exist
			}

			// Initialize the Spark Reporter
			ExtentSparkReporter sparkReporter = new ExtentSparkReporter(reportPath);
			sparkReporter.config().setTheme(Theme.DARK);
			sparkReporter.config().setDocumentTitle("Test Automation Report");
			sparkReporter.config().setReportName("Test Results");
			
			// Apply filter to include only failed tests in the report
//			sparkReporter.filter().statusFilter().as(new Status[] {Status.FAIL}).apply();
			

			// Create ExtentReports instance and attach Spark Reporter
			extent = new ExtentReports();
			extent.attachReporter(sparkReporter);
		}
		return extent;
	}

	// Start a test in the report
	public static void startTest(String testName, String testDescription, String groupName) {
		String authorname = ConfigReader.getProperty("test.report.author.name");
		ExtentTest extentTest = extent.createTest(testName, testDescription).assignAuthor(authorname).assignCategory(groupName);
		test.set(extentTest); // Store test in the thread-local variable
	}

	// Log information to the report and the console
	public static void logInfo(String message) {
		if (test.get() != null) {
			test.get().info(message);
		}
		logger.info(message); // Log to the console
	}

	// Log a pass result
	public static void logPass(String message) {
		if (test.get() != null) {
			test.get().pass(message);
		}
		logger.info("PASS: " + message); // Log to the console
	}

	// Log a fail result
	public static void logFail(String message) {
		if (test.get() != null) {
			test.get().fail(message);
		}
		logger.error("FAIL: " + message); // Log to the console
	}
	
	// Automatically log failures based on exception
    public static void logException(Throwable throwable) {
        if (test.get() != null) {
            test.get().fail("Test failed with exception: " + throwable.getMessage());
        }
        logger.error("Test failed with exception: " + throwable.getMessage()); // Log to the console
    }

	// End the test
	public static void endTest() {
		if (extent != null) {
			extent.flush();
		}
	}

	// Generate a clickable report link in the terminal
	public static void generateReportLink() {
		String reportPath = ConfigReader.getProperty("extent.report.path");
		File reportFile = new File(reportPath);
		URI reportUri = reportFile.toURI(); // Convert to URI for proper formatting

		// Logging the clickable link
		logger.info("Test execution completed. Opening the report in browser "
				+ "or View the report at: " + reportUri);
		try {
			Desktop.getDesktop().browse(reportUri);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
}
