package libraries;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import utilities.ExtentReportManager;

import java.util.ArrayList;
import java.util.List;

public class TableUtils {
    private LocatorsUtils locators;

    public TableUtils(WebDriver driver) {
        this.locators = new LocatorsUtils(driver);
    }

    public String getCellValue(By tableLocator, int row, int col) {
        WebElement cell = locators.getElement(By.xpath(String.format("%s//tr[%d]/td[%d]", tableLocator, row, col)), 10);
        String value = cell.getText();
        ExtentReportManager.logInfo("Cell value at row " + row + ", column " + col + ": " + value);
        return value;
    }

    public List<String> getRowData(By tableLocator, int row) {
        List<String> rowData = new ArrayList<>();
        List<WebElement> cells = locators.getElements(By.xpath(String.format("%s//tr[%d]/td", tableLocator, row)), 10);
        for (WebElement cell : cells) {
            rowData.add(cell.getText());
        }
        ExtentReportManager.logInfo("Row data at row " + row + ": " + rowData);
        return rowData;
    }

    public List<String> getColumnData(By tableLocator, int col) {
        List<String> columnData = new ArrayList<>();
        List<WebElement> cells = locators.getElements(By.xpath(String.format("%s//tr/td[%d]", tableLocator, col)), 10);
        for (WebElement cell : cells) {
            columnData.add(cell.getText());
        }
        ExtentReportManager.logInfo("Column data at column " + col + ": " + columnData);
        return columnData;
    }

    public boolean isValuePresentInTable(By tableLocator, String value) {
        List<WebElement> cells = locators.getElements(By.xpath(String.format("%s//td", tableLocator)), 10);
        for (WebElement cell : cells) {
            if (cell.getText().contains(value)) {
                ExtentReportManager.logInfo("Value '" + value + "' found in table.");
                return true;
            }
        }
        ExtentReportManager.logInfo("Value '" + value + "' not found in table.");
        return false;
    }
}