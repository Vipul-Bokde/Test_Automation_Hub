// libraries.DropdownAndRadioButtonHandler.java
package libraries;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.Select;

import utilities.ExtentReportManager;

import java.util.List;

public class DropdownAndRadioButtonUtils {

	private WebDriver driver;

	public DropdownAndRadioButtonUtils(WebDriver driver) {
		this.driver = driver;
	}

	// --- Dropdown Handling ---

	public void selectByVisibleText(By locator, String visibleText) {
		try {
			WebElement dropdownElement = driver.findElement(locator);
			Select select = new Select(dropdownElement);
			select.selectByVisibleText(visibleText);
			ExtentReportManager.logInfo("Selected '" + visibleText + "' from dropdown: " + locator);
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

	public void selectByIndex(By locator, int index) {
		try {
			WebElement dropdownElement = driver.findElement(locator);
			Select select = new Select(dropdownElement);
			select.selectByIndex(index);
			ExtentReportManager.logInfo("Selected index '" + index + "' from dropdown: " + locator);
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

	public void selectByValue(By locator, String value) {
		try {
			WebElement dropdownElement = driver.findElement(locator);
			Select select = new Select(dropdownElement);
			select.selectByValue(value);
			ExtentReportManager.logInfo("Selected value '" + value + "' from dropdown: " + locator);
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

	public String getFirstSelectedOption(By locator) {
		try {
			WebElement dropdownElement = driver.findElement(locator);
			Select select = new Select(dropdownElement);
			String selectedOption = select.getFirstSelectedOption().getText();
			ExtentReportManager.logInfo("First selected option: " + selectedOption);
			return selectedOption;
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

	public List<WebElement> getAllOptions(By locator) {
		try {
			WebElement dropdownElement = driver.findElement(locator);
			Select select = new Select(dropdownElement);
			List<WebElement> options = select.getOptions();
			ExtentReportManager.logInfo("Retrieved all options from dropdown: " + locator);
			return options;
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

	public boolean isMultipleSelect(By locator) {
		try {
			WebElement dropdownElement = driver.findElement(locator);
			Select select = new Select(dropdownElement);
			boolean isMultiple = select.isMultiple();
			ExtentReportManager.logInfo("Dropdown allows multiple selections: " + isMultiple);
			return isMultiple;
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

	// --- Radio Button Handling ---

	public void selectRadioButton(By locator) {
		try {
			WebElement radioButton = driver.findElement(locator);
			radioButton.click();
			ExtentReportManager.logInfo("Selected radio button: " + locator);
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

	public boolean isRadioButtonSelected(By locator) {
		try {
			WebElement radioButton = driver.findElement(locator);
			boolean isSelected = radioButton.isSelected();
			ExtentReportManager.logInfo("Radio button is selected: " + isSelected);
			return isSelected;
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

	// --- Checkbox Handling ---
	public void selectCheckbox(By locator) {
		try {
			WebElement checkbox = driver.findElement(locator);
			if (!checkbox.isSelected()) {
				checkbox.click();
			}
			ExtentReportManager.logInfo("Selected checkbox: " + locator);
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

	public void deselectCheckbox(By locator) {
		try {
			WebElement checkbox = driver.findElement(locator);
			if (checkbox.isSelected()) {
				checkbox.click();
			}
			ExtentReportManager.logInfo("Deselected checkbox: " + locator);
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

	public boolean isCheckboxSelected(By locator) {
		try {
			WebElement checkbox = driver.findElement(locator);
			boolean isSelected = checkbox.isSelected();
			ExtentReportManager.logInfo("Checkbox is selected: " + isSelected);
			return isSelected;
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

}