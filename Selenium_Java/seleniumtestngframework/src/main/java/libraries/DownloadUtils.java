package libraries;
import utilities.ExtentReportManager;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class DownloadUtils {

	public boolean isFileDownloaded(String downloadPath, String fileName) {
		File file = new File(downloadPath + File.separator + fileName);
		int timeout = 10; // Timeout in seconds
		while (timeout > 0) {
			if (file.exists()) {
				ExtentReportManager.logInfo("File downloaded successfully: " + fileName);
				return true;
			}
			try {
				Thread.sleep(1000); // Check every second
				timeout--;
			} catch (InterruptedException e) {
				ExtentReportManager.logException(e);
				Thread.currentThread().interrupt(); // Restore interrupt status
				return false;
			}
		}
		ExtentReportManager.logFail("File download timed out: " + fileName);
		return false;
	}

	public void clearDownloadDirectory(String downloadPath) {
		try {
			Files.walk(Paths.get(downloadPath)).filter(Files::isRegularFile).forEach(p -> {
				try {
					Files.delete(p);
					ExtentReportManager.logInfo("Deleted file: " + p);
				} catch (IOException e) {
					ExtentReportManager.logException(e);
				}
			});
			ExtentReportManager.logInfo("Cleared download directory: " + downloadPath);
		} catch (IOException e) {
			ExtentReportManager.logException(e);
		}
	}
}
