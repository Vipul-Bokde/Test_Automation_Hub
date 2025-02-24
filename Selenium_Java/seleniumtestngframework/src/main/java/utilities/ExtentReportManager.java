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

	public static ExtentReports initExtentReport() {
		if (extent == null) {
			String reportPath = ConfigReader.getProperty("extent.report.path");
			File reportFile = new File(reportPath);
			File directory = reportFile.getParentFile();
			if (!directory.exists()) {
				directory.mkdirs();
			}

			ExtentSparkReporter sparkReporter = new ExtentSparkReporter(reportPath);
			sparkReporter.config().setTheme(Theme.DARK);
			sparkReporter.config().setDocumentTitle("Test Automation Report");
			sparkReporter.config().setReportName("Test Results");

			// Optional: Filter for failed tests only (uncomment if needed)
			// sparkReporter.filter().statusFilter().as(new Status[] { Status.FAIL
			// }).apply();

			extent = new ExtentReports();
			extent.attachReporter(sparkReporter);
		}
		return extent;
	}

	public static void startTest(String testName, String testDescription, String groupName) {
		String authorname = ConfigReader.getProperty("test.report.author.name");
		ExtentTest extentTest = extent.createTest(testName, testDescription).assignAuthor(authorname)
				.assignCategory(groupName);
		test.set(extentTest);
	}

	public static void logInfo(String message) {
		if (test.get() != null) {
			test.get().info(message);
		}
		logger.info(message);
	}

	public static void logPass(String message) {
		if (test.get() != null) {
			test.get().pass(message);
		}
		logger.info("PASS: " + message);
	}

	public static void logFail(String message) {
		if (test.get() != null) {
			test.get().fail(message);
		}
		logger.error("FAIL: " + message);
	}

	public static void logException(Throwable throwable) {
		if (test.get() != null) {
			test.get().fail(throwable);
		}
		logger.error("Test failed with exception: ", throwable);
	}

	public static void endTest() {
		if (extent != null) {
			extent.flush();
		}
	}

	public static void generateReportLink() {
		String reportPath = ConfigReader.getProperty("extent.report.path");
		File reportFile = new File(reportPath);
		URI reportUri = reportFile.toURI();

		logger.info("Test execution completed. Opening the report in browser or View the report at: " + reportUri);
		try {
			Desktop.getDesktop().browse(reportUri);
		} catch (IOException e) {
			logger.error("Error opening report in browser: " + e.getMessage(), e); // Log the exception
		}
	}
}