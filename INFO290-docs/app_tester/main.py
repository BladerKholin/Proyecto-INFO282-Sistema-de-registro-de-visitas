from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
import time

load_dotenv()

### Options
options = UiAutomator2Options()
options.platform_name = 'Android'
options.device_name = 'emulator-5554'
options.app = os.getenv('APK_PATH')
options.automation_name = 'UiAutomator2'
options.new_command_timeout = 350


### Test cases
from TestCases.TestTextboxMayus.TestTexboxMayus import TestTexboxMayus
tests = [TestTexboxMayus]

### Main
def main():
    
    ### Load environment variables
    WEBDRIVER_REMOTE_URL = os.getenv('WEBDRIVER_REMOTE_URL')
    if WEBDRIVER_REMOTE_URL is None:
        print("WEBDRIVER_REMOTE_URL not found in environment variables")
        return
    
    ### Driver
    print("Starting driver session...")
    driver = webdriver.Remote(WEBDRIVER_REMOTE_URL, options=options)
    print("Driver session started successfully")
    
    for test_case in tests:

        correct = True
        begin_time = time.time()
        test = test_case(driver)
        print("\n------------------------------------------------------")
        print(f"Test name: {test.test_name}")
        print(f"Description: {test.description}")
        print("-----------------------------------------------------")
        
        try: 
            test.setup()
        except Exception as e:
            correct = False
            print(f"Test case setup failed: {test_case.__name__}, Error: {e}")
            print("SKIPPING TEST CASE")
            continue
        
        try: 
            results = test.run()
            test.print_results(results)
        except Exception as e:
            correct = False
            print(f"Test case execution failed: {test_case.__name__}, Error: {e}")
            print("TEST CASE EXECUTION FAILED")

        try: 
            test.teardown()
        except Exception as e:
            correct = False 
            print(f"Test case teardown failed: {test_case.__name__}, Error: {e}")
            print("TEARDOWN FAILED")
        
        test_duration = time.time() - begin_time
        print(f"Test case duration: {test_duration:.2f} seconds || STATUS: {'Execution complete' if correct else 'Execution failed'}")
        print("-----------------------------------------------------\n")


if __name__ == "__main__":
    main()