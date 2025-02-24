package libraries;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import utilities.ExtentReportManager;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.List;
import org.openqa.selenium.NoSuchElementException;

public class CalendarUtils {

    private WebDriver driver;
    private LocatorsUtils locators;

    public CalendarUtils(WebDriver driver) {
        this.driver = driver;
        this.locators = new LocatorsUtils(driver);
    }

    public void setDate(By dateFieldLocator, String date) {
        locators.sendKeys(dateFieldLocator, date);
        ExtentReportManager.logInfo("Set date to: " + date);
    }

    public void selectDateFromGrid(By calendarLocator, String date, String dateFormat) throws ParseException {
        SimpleDateFormat sdf = new SimpleDateFormat(dateFormat);
        String formattedDate = sdf.format(sdf.parse(date));
        String dateLocator = String.format("//table[%s]//td[text()='%s']", calendarLocator, formattedDate); // Example XPath
        locators.getElement(By.xpath(dateLocator), 10).click();
        ExtentReportManager.logInfo("Selected date: " + date);
    }

    public void selectDateFromGrid(By calendarLocator, int day, int month, int year) {
        // Logic to navigate to the correct month and year (if needed)

        List<WebElement> dates = locators.getElements(By.xpath(String.format("//table[%s]//td", calendarLocator)), 10);
        for (WebElement date : dates) {
            try { //added try catch block to handle exception if date is not a number
                if (Integer.parseInt(date.getText()) == day) {
                    date.click();
                    ExtentReportManager.logInfo("Selected date: " + day + "/" + month + "/" + year);
                    return;
                }
            } catch (NumberFormatException e) {
                // Ignore if the element is not a number (e.g., header cells)
            }
        }
        ExtentReportManager.logFail("Date not found: " + day + "/" + month + "/" + year);
        throw new NoSuchElementException("Date not found: " + day + "/" + month + "/" + year);
    }

     @SuppressWarnings("deprecation")
	public void selectDateFromGridDynamic(By calendarLocator, String date) {

        String[] dateParts = date.split("/"); // Split the date into day, month, and year

        int day = Integer.parseInt(dateParts[0]);
        int month = Integer.parseInt(dateParts[1]);
        int year = Integer.parseInt(dateParts[2]);

        List<WebElement> monthDropdown = locators.getElements(By.xpath("//select[@class='month']"),10);
        for(WebElement element:monthDropdown){
            if(Integer.parseInt(element.getAttribute("value"))==month-1){
                element.click();
                break;
            }
        }

        List<WebElement> yearDropdown = locators.getElements(By.xpath("//select[@class='year']"),10);
        for(WebElement element:yearDropdown){
            if(Integer.parseInt(element.getAttribute("value"))==year){
                element.click();
                break;
            }
        }

        List<WebElement> dates = locators.getElements(By.xpath(String.format("//table[%s]//td", calendarLocator)), 10);
        for (WebElement dateElement : dates) {
            try { //added try catch block to handle exception if date is not a number
                if (Integer.parseInt(dateElement.getText()) == day) {
                    dateElement.click();
                    ExtentReportManager.logInfo("Selected date: " + day + "/" + month + "/" + year);
                    return;
                }
            } catch (NumberFormatException e) {
                // Ignore if the element is not a number (e.g., header cells)
            }
        }
        ExtentReportManager.logFail("Date not found: " + day + "/" + month + "/" + year);
        throw new NoSuchElementException("Date not found: " + day + "/" + month + "/" + year);
    }
}