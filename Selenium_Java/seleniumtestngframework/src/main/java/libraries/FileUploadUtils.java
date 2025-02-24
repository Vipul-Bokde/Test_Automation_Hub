package libraries;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import utilities.ExtentReportManager;

public class FileUploadUtils {
    private LocatorsUtils locators;

    public FileUploadUtils(WebDriver driver) {
        this.locators = new LocatorsUtils(driver);
    }

    public void uploadFile(By locator, String filePath) {
        try {
            WebElement uploadElement = locators.getElement(locator, 10); // Wait for the element
            uploadElement.sendKeys(filePath);
            ExtentReportManager.logInfo("Uploaded file: " + filePath + " using locator: " + locator);
        } catch (Exception e) {
            ExtentReportManager.logException(e);
            throw e; // Re-throw to fail the test
        }
    }

    // Method to upload multiple files (if needed)
    public void uploadMultipleFiles(By locator, String[] filePaths) {
        try {
            WebElement uploadElement = locators.getElement(locator, 10);
            for (String filePath : filePaths) {
                uploadElement.sendKeys(filePath); // sendKeys will append for multiple files
                ExtentReportManager.logInfo("Uploaded file: " + filePath + " using locator: " + locator);
            }
        } catch (Exception e) {
            ExtentReportManager.logException(e);
            throw e;
        }

    }
}