package setup;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.safari.SafariDriver;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import io.github.bonigarcia.wdm.WebDriverManager;
import libraries.BrowserActions;  // Import the BrowserActions class from libraries package
import utilities.ConfigReader;
import utilities.ExtentReportManager;  // Import the ExtentReportManager class

public class BaseSetup {
    protected WebDriver driver;
    private BrowserActions browserActions;  // Declare BrowserActions instance
    private static final Logger logger = LogManager.getLogger(BaseSetup.class);  // Initialize the logger

    @BeforeMethod
    public void setup() {
        // Initialize Extent Report
        ExtentReportManager.initExtentReport();

        logger.info("Starting the test setup...");
        ExtentReportManager.logInfo("Starting the test setup...");
        // Setup the browser based on the configuration (chrome, edge, firefox, safari)
        String browser = ConfigReader.getProperty("browser");
        String url = ConfigReader.getProperty("base.url");
        ExtentReportManager.startTest("Smoke Suite", "Test Execution Started");
        ExtentReportManager.logInfo("Selected browser: " + browser);
        logger.info("Selected browser: " + browser);

        switch (browser.toLowerCase()) {
            case "chrome":
                WebDriverManager.chromedriver().setup();
                driver = new ChromeDriver();
                break;
            case "edge":
                WebDriverManager.edgedriver().setup();
                driver = new EdgeDriver();
                break;
            case "firefox":
                WebDriverManager.firefoxdriver().setup();
                driver = new FirefoxDriver();
                break;
            case "safari":
                driver = new SafariDriver();
                break;
            default:
                logger.error("Browser not supported: " + browser);
                throw new IllegalArgumentException("Browser not supported: " + browser);
        }

        driver.manage().window().maximize();
        driver.get(url);  // Replace with your test URL
        ExtentReportManager.logInfo("Browser opened successfully.");
        ExtentReportManager.logInfo(url + "opened successfully.");
        
        // Initialize BrowserActions with the WebDriver
        browserActions = new BrowserActions(driver);
    }

    @AfterMethod
    public void teardown() {
        logger.info("Tearing down the test...");
        if (driver != null) {
            // Use the quitBrowser method from BrowserActions in libraries package
            browserActions.quitBrowser();
            logger.info("Browser closed.");
            ExtentReportManager.logInfo("Browser closed successfully.");
        }
        
        // End the test in the Extent Report
        ExtentReportManager.endTest();

        // Generate the report link in the terminal
        ExtentReportManager.generateReportLink();
    }
}
