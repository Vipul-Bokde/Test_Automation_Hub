package utilities;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.reporter.ExtentSparkReporter;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import java.io.File;
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
            sparkReporter.config().setDocumentTitle("Test Automation Report");
            sparkReporter.config().setReportName("Test Results");

            // Create ExtentReports instance and attach Spark Reporter
            extent = new ExtentReports();
            extent.attachReporter(sparkReporter);
        }
        return extent;
    }

    // Start a test in the report
    public static void startTest(String testName, String testDescription) {
        ExtentTest extentTest = extent.createTest(testName, testDescription);
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
        logger.info("Test execution completed. View the report at: " + reportUri);
    }
}
