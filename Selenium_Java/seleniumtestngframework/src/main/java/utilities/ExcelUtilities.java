package utilities;
import org.apache.poi.ss.usermodel.*;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

public class ExcelUtilities implements AutoCloseable {

    private static final String ENCRYPTED_FILE_PATH = ConfigReader.getProperty("outputPath_2");
    private static final String TEMP_FILE_PATH = ConfigReader.getProperty("tempPath_2");
    private static final String SECRET_KEY = System.getenv("SECRET_TEST_DATA_KEY");

    private Workbook workbook;
    private Sheet sheet;
    private String sheetName; // Store the sheet name

    public ExcelUtilities(String sheetName) {
        this.sheetName = sheetName; // Initialize sheet name
        try {
            decryptFile(ENCRYPTED_FILE_PATH, TEMP_FILE_PATH);
            try (FileInputStream fis = new FileInputStream(TEMP_FILE_PATH)) { // Use try-with-resources
                workbook = WorkbookFactory.create(fis); // Use WorkbookFactory
                sheet = workbook.getSheet(sheetName);
                if (sheet == null) {
                    sheet = workbook.createSheet(sheetName); // Create if it doesn't exist
                    // Add a header row if the sheet is new:
                    Row headerRow = sheet.createRow(0);
                    // You'll need to decide what your header columns should be.  For example:
                    headerRow.createCell(0).setCellValue("Key");
                    headerRow.createCell(1).setCellValue("Value");
                }
            }
        } catch (Exception e) {
            throw new RuntimeException("Error initializing ExcelUtilities: " + e.getMessage(), e);
        }
    }


    private void decryptFile(String inputPath, String outputPath) throws Exception {
        if (SECRET_KEY == null || SECRET_KEY.isEmpty()) {
            throw new RuntimeException("SECRET_TEST_DATA_KEY environment variable is not set.");
        }
        byte[] encryptedData = Files.readAllBytes(Paths.get(inputPath));
        byte[] decryptedData = decrypt(encryptedData);
        Files.write(Paths.get(outputPath), decryptedData);
    }

    private byte[] decrypt(byte[] encryptedData) throws Exception {
        Cipher cipher = Cipher.getInstance("AES");
        SecretKeySpec keySpec = new SecretKeySpec(SECRET_KEY.getBytes(), "AES");
        cipher.init(Cipher.DECRYPT_MODE, keySpec);
        return cipher.doFinal(encryptedData);
    }

    public Map<String, String> readData() {
        Map<String, String> dataMap = new HashMap<>();
        try {
            Iterator<Row> rowIterator = sheet.iterator();
            if (rowIterator.hasNext()) { // Skip header row if present
                rowIterator.next();
            }

            while (rowIterator.hasNext()) {
                Row row = rowIterator.next();
                Cell keyCell = row.getCell(0); // Assuming key is in the first column
                Cell valueCell = row.getCell(1); // Assuming value is in the second column

                String key = getCellValue(keyCell);
                String value = getCellValue(valueCell);

                if (key != null && !key.isEmpty()) { // Check for null or empty key
                    dataMap.put(key, value);
                }
            }
        } catch (Exception e) {
            throw new RuntimeException("Error reading Excel data: " + e.getMessage(), e);
        }
        return dataMap;
    }

    private String getCellValue(Cell cell) {
        if (cell == null) return null;

        switch (cell.getCellType()) {
            case STRING:
                return cell.getStringCellValue();
            case NUMERIC:
                return String.valueOf(cell.getNumericCellValue());
            case BOOLEAN:
                return String.valueOf(cell.getBooleanCellValue());
            case FORMULA:
                try {
                    return String.valueOf(cell.getNumericCellValue()); // Try numeric first
                } catch (IllegalStateException e) {
                    return cell.getCellFormula(); // If not numeric, get formula
                }
            case BLANK: // Handle blank cells
                return "";
            default:
                return null;
        }
    }



    public void writeData(String key, String value) {
        try {
            boolean keyExists = false;
            for (Row row : sheet) {
                Cell firstCell = row.getCell(0);
                if (firstCell != null && getCellValue(firstCell).equalsIgnoreCase(key)) {
                    Cell cell = row.getCell(1);
                    if (cell == null) {
                        cell = row.createCell(1);
                    }
                    cell.setCellValue(value);
                    keyExists = true;
                    break;
                }
            }

            if (!keyExists) {
                int rowNum = sheet.getLastRowNum() + 1;
                Row row = sheet.createRow(rowNum);
                row.createCell(0).setCellValue(key);
                row.createCell(1).setCellValue(value);
            }

            try (FileOutputStream outputStream = new FileOutputStream(TEMP_FILE_PATH)) { // Try-with-resources
                workbook.write(outputStream);
            }

            encryptFile(TEMP_FILE_PATH, ENCRYPTED_FILE_PATH);
        } catch (Exception e) {
            throw new RuntimeException("Error writing to Excel file: " + e.getMessage(), e);
        }
    }

    private void encryptFile(String inputPath, String outputPath) throws Exception {
        byte[] fileData = Files.readAllBytes(Paths.get(inputPath));
        byte[] encryptedData = encrypt(fileData);
        Files.write(Paths.get(outputPath), encryptedData);
    }

    private byte[] encrypt(byte[] data) throws Exception {
        Cipher cipher = Cipher.getInstance("AES");
        SecretKeySpec keySpec = new SecretKeySpec(SECRET_KEY.getBytes(), "AES");
        cipher.init(Cipher.ENCRYPT_MODE, keySpec);
        return cipher.doFinal(data);
    }

    @Override
    public void close() {
        try {
            if (workbook != null) {
                workbook.close();
            }
            new File(TEMP_FILE_PATH).delete();
        } catch (Exception e) {
            throw new RuntimeException("Error closing Excel workbook: " + e.getMessage(), e);
        }
    }
}