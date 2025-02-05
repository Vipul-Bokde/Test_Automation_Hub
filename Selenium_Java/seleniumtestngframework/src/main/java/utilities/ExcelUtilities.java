package utilities;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

public class ExcelUtilities {

    private static final String ENCRYPTED_FILE_PATH = ConfigReader.getProperty("outputPath"); // Encrypted file path
    private static final String TEMP_FILE_PATH = ConfigReader.getProperty("tempPath"); // Decrypted file path
    private static final String SECRET_KEY = System.getenv("SECRET_TEST_DATA_KEY"); // Get secret key from environment variable

    private Workbook workbook;
    private Sheet sheet;

    public ExcelUtilities(String sheetName) {
        try {
            decryptFile(ENCRYPTED_FILE_PATH, TEMP_FILE_PATH); // Decrypt the file at runtime
            workbook = new XSSFWorkbook(new File(TEMP_FILE_PATH));
            sheet = workbook.getSheet(sheetName);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void decryptFile(String inputPath, String outputPath) throws Exception {
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
            Row headerRow = rowIterator.next(); // Assuming first row as header
            Row valueRow = rowIterator.next(); // Assuming second row as values

            Iterator<Cell> headerCells = headerRow.cellIterator();
            Iterator<Cell> valueCells = valueRow.cellIterator();

            while (headerCells.hasNext() && valueCells.hasNext()) {
                String header = headerCells.next().getStringCellValue();
                String value = valueCells.next().getStringCellValue();
                dataMap.put(header, value);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return dataMap;
    }

    public void writeData(String key, String value) {
        try {
            boolean keyExists = false;
            for (Row row : sheet) {
                Cell firstCell = row.getCell(0);
                if (firstCell != null && firstCell.getStringCellValue().equalsIgnoreCase(key)) {
                    row.getCell(1).setCellValue(value);
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

            // Write changes to temp file and then re-encrypt
            FileOutputStream outputStream = new FileOutputStream(TEMP_FILE_PATH);
            workbook.write(outputStream);
            outputStream.close();

            encryptFile(TEMP_FILE_PATH, ENCRYPTED_FILE_PATH); // Re-encrypt after writing
        } catch (Exception e) {
            e.printStackTrace();
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

    public void closeWorkbook() {
        try {
            if (workbook != null) {
                workbook.close();
            }
            new File(TEMP_FILE_PATH).delete(); // Delete temp file to prevent errors
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}


/*
 * package utilities;
 * 
 * import org.apache.poi.ss.usermodel.*; import
 * org.apache.poi.xssf.usermodel.XSSFWorkbook; import java.io.File; import
 * java.io.FileOutputStream; import java.util.HashMap; import
 * java.util.Iterator; import java.util.Map;
 * 
 * public class ExcelUtilities {
 * 
 * private static final String EXCEL_FILE_PATH =
 * "src\\main\\java\\testdata\\TestData.xlsx"; // Direct file path
 * 
 * private Workbook workbook; private Sheet sheet;
 * 
 * public ExcelUtilities(String sheetName) { try { workbook = new
 * XSSFWorkbook(new File(EXCEL_FILE_PATH)); sheet =
 * workbook.getSheet(sheetName); } catch (Exception e) { e.printStackTrace(); }
 * }
 * 
 * public Map<String, String> readData() { Map<String, String> dataMap = new
 * HashMap<>(); try { Iterator<Row> rowIterator = sheet.iterator(); Row
 * headerRow = rowIterator.next(); // Assuming first row as header Row valueRow
 * = rowIterator.next(); // Assuming second row as values
 * 
 * Iterator<Cell> headerCells = headerRow.cellIterator(); Iterator<Cell>
 * valueCells = valueRow.cellIterator();
 * 
 * while (headerCells.hasNext() && valueCells.hasNext()) { String header =
 * headerCells.next().getStringCellValue(); String value =
 * valueCells.next().getStringCellValue(); dataMap.put(header, value); } } catch
 * (Exception e) { e.printStackTrace(); } return dataMap; }
 * 
 * public void writeData(String key, String value) { try { boolean keyExists =
 * false; for (Row row : sheet) { Cell firstCell = row.getCell(0); if (firstCell
 * != null && firstCell.getStringCellValue().equalsIgnoreCase(key)) {
 * row.getCell(1).setCellValue(value); keyExists = true; break; } }
 * 
 * if (!keyExists) { int rowNum = sheet.getLastRowNum() + 1; Row row =
 * sheet.createRow(rowNum); row.createCell(0).setCellValue(key);
 * row.createCell(1).setCellValue(value); }
 * 
 * FileOutputStream outputStream = new FileOutputStream(EXCEL_FILE_PATH);
 * workbook.write(outputStream); outputStream.close(); } catch (Exception e) {
 * e.printStackTrace(); } }
 * 
 * public void closeWorkbook() { try { if (workbook != null) { workbook.close();
 * } } catch (Exception e) { e.printStackTrace(); } } }
 */