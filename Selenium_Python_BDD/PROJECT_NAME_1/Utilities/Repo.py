import os
# from asyncio.log import logger
from GP.utilities.logs_util import logger

parent_dir = os.getcwd()
logger.info("Your working directory is:"+parent_dir)

project_path = os.path.realpath("")
logger.info("project_path"+project_path)

ui_test_path = os.path.join(parent_dir, "ui_test")
logger.info("ui_test_path"+ui_test_path)

GP_path = os.path.join(project_path, "GP")
logger.info("GP_path"+GP_path)

automation_test_path = os.path.join(GP_path, "automation_test")

uploadfiles_path_1 = os.path.join(automation_test_path, "uploadfiles")

file1 = os.path.join(uploadfiles_path_1, "File1.csv")

testData_Folder_Path = os.path.join(GP_path, "TestData")

testDataSheet_GP = os.path.join(testData_Folder_Path, "GP_TestDataSheet.xls")

testData_path = os.path.join(GP_path, "TestData")

uploadfiles_path = os.path.join(testData_path, "UploadFiles")

downloadfiles_path = os.path.join(testData_path, "DownloadFiles")

Env_folder_path = os.path.join(project_path, "ENV")

QA_env = os.path.join(Env_folder_path, "QA")
UAT_env = os.path.join(Env_folder_path, "UAT")

QA_GP = os.path.join(QA_env, "GP")
UAT_GP = os.path.join(UAT_env, "GP")

QA_GP_Client = os.path.join(QA_GP, "Client")
UAT_GP_Client = os.path.join(UAT_GP, "Client")
