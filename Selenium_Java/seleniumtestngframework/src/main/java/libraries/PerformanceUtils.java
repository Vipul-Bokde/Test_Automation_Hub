/*This line from your performance log file represents a single performance measurement taken on your web page. Let's break down each value:

Timestamp: 2025-02-24 18:40:43 - 
This is the date and time when the performance measurement was taken.  
It's in yyyy-MM-dd HH:mm:ss format (Year-Month-Day Hour:Minute:Second).  
This tells you exactly when the metrics were captured.

Page URL: 
https://www.haldirams.com/ - 
This is the URL of the web page for which the performance metrics were captured.  
It's crucial to know which page the data refers to.

Load Time (ms): 5010 - 
This is the total time it took for the page to fully load, measured in milliseconds.  
"Fully loaded" typically means that all resources (HTML, CSS, JavaScript, images, etc.) 
have been downloaded and processed, and the page is ready for user interaction.  
5010 milliseconds is equal to 5.01 seconds.

DOMContentLoaded Time (ms): 3524 - 
This is the time it took for the browser to parse the HTML and construct the 
Document Object Model (DOM).  
The DOM is a representation of the page's structure that 
JavaScript can interact with.  DOMContentLoaded is usually 
a point where the basic page structure is ready, 
even if some resources (like images) might still be loading.  
3524 milliseconds is equal to 3.524 seconds.

Network Requests: 0 - 
This is the number of network requests made by 
the page during the load process.  A network request is when the 
browser asks a server for a resource (HTML file, image, script, etc.).  
In your case, it shows 0 which is suspicious. It is likely that the way 
you are trying to capture the network requests is not working.

Console Errors: 1 - 
This indicates that there was one error logged in the browser's 
console during the page load.  These errors are usually JavaScript errors 
or other problems that might prevent the page from working correctly. 
You should investigate these errors to see if they are affecting performance or functionality.

Console Warnings: 0 - This shows that there were no warnings 
logged in the browser's console.  
Warnings are less severe than errors but can still indicate potential issues.
*/

package libraries;

import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.logging.LogEntries;
import org.openqa.selenium.logging.LogType;

import utilities.ExtentReportManager;

import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class PerformanceUtils {

	private WebDriver driver;
	private FileWriter performanceLog;

	public PerformanceUtils(WebDriver driver, String logFilePath) {
		this.driver = driver;
		try {
			performanceLog = new FileWriter(logFilePath, true); // Append to the log file
			logPerformanceHeader(); // Write header row
		} catch (IOException e) {
			ExtentReportManager.logException(e);
			throw new RuntimeException("Error creating performance log file: " + e.getMessage(), e);
		}
	}

	private void logPerformanceHeader() throws IOException {
		String header = "Timestamp,Page URL,Load Time (ms),DOMContentLoaded Time (ms),Network Requests,Console Errors,Console Warnings\n";
		performanceLog.write(header);
	}

	public void capturePerformanceMetrics(String pageURL) {
		try {
			long loadTime = getLoadTime();
			long domContentLoadedTime = getDOMContentLoadedTime();
			int networkRequests = getNetworkRequests();
			int consoleErrors = getConsoleErrors();
			int consoleWarnings = getConsoleWarnings();

			String timestamp = getCurrentTimestamp();
			String logEntry = String.format("%s,%s,%d,%d,%d,%d,%d\n", timestamp, pageURL, loadTime,
					domContentLoadedTime, networkRequests, consoleErrors, consoleWarnings);
			performanceLog.write(logEntry);
			performanceLog.flush(); // Important: Flush the writer to ensure data is written immediately

			ExtentReportManager.logInfo("Performance metrics captured for: " + pageURL);

		} catch (Exception e) {
			ExtentReportManager.logException(e);
		}
	}

	private long getLoadTime() {
		return (long) ((JavascriptExecutor) driver).executeScript(
				"return window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;");
	}

	private long getDOMContentLoadedTime() {
		return (long) ((JavascriptExecutor) driver).executeScript(
				"return window.performance.timing.domContentLoadedEventEnd - window.performance.timing.navigationStart;");
	}

	private int getNetworkRequests() {
		// You might need a more sophisticated way to get network requests if you need
		// details.
		// This is a very basic example.
		return 0; // Replace with actual logic if needed.
	}

	private int getConsoleErrors() {
		LogEntries entries = driver.manage().logs().get(LogType.BROWSER);
		return (int) entries.getAll().stream().filter(entry -> entry.getLevel().toString().equals("SEVERE")).count();
	}

	private int getConsoleWarnings() {
		LogEntries entries = driver.manage().logs().get(LogType.BROWSER);
		return (int) entries.getAll().stream().filter(entry -> entry.getLevel().toString().equals("WARNING")).count();
	}

	private String getCurrentTimestamp() {
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		return sdf.format(new Date());
	}

	public void closeLogFile() {
		try {
			if (performanceLog != null) {
				performanceLog.close();
			}
		} catch (IOException e) {
			ExtentReportManager.logException(e);
		}
	}
}