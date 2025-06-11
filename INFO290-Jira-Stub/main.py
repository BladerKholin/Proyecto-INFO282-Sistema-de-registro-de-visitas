from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
import time
import traceback
from jira_integration import JiraIntegration

load_dotenv()

### Options
options = UiAutomator2Options()
options.platform_name = 'Android'
options.device_name = os.getenv('DEVICE_NAME', 'emulator-5554')  # Configurable device name
options.app = os.getenv('APK_PATH')
options.automation_name = 'UiAutomator2'
options.new_command_timeout = int(os.getenv('COMMAND_TIMEOUT', '350'))  # Configurable timeout
options.no_reset = os.getenv('NO_RESET', 'false').lower() == 'true'  # Configurable reset behavior
options.full_reset = os.getenv('FULL_RESET', 'false').lower() == 'true'  # Configurable full reset


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
    
    # Initialize Jira integration
    jira = JiraIntegration()
    
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
        
        # Clear any previous test data
        test.clear_test_data()
        screenshot_path = None
        
        try: 
            test.setup()
        except Exception as e:
            correct = False
            error_msg = f"Test case setup failed: {test_case.__name__}, Error: {e}"
            print(error_msg)
            print("SKIPPING TEST CASE")
            
            # Capture screenshot on setup failure
            screenshot_path = test.take_screenshot("setup_failure")
            
            # Create Jira issue for setup failure
            if jira.enabled:
                test_data = test.get_test_data()
                test_data['failure_stage'] = 'setup'
                test_data['error_type'] = type(e).__name__
                
                jira.create_test_failure_issue(
                    test_name=test.test_name,
                    test_description=test.description,
                    error_details=f"Setup Error: {str(e)}\n\nStacktrace:\n{traceback.format_exc()}",
                    test_data=test_data,
                    screenshot_path=screenshot_path
                )
            
            continue
        
        try: 
            results = test.run()
            test.print_results(results)
        except Exception as e:
            correct = False
            error_msg = f"Test case execution failed: {test_case.__name__}, Error: {e}"
            print(error_msg)
            print("TEST CASE EXECUTION FAILED")
            
            # Capture screenshot on execution failure
            screenshot_path = test.take_screenshot("execution_failure")
            
            # Create Jira issue for execution failure
            if jira.enabled:
                test_data = test.get_test_data()
                test_data['failure_stage'] = 'execution'
                test_data['error_type'] = type(e).__name__
                
                jira.create_test_failure_issue(
                    test_name=test.test_name,
                    test_description=test.description,
                    error_details=f"Execution Error: {str(e)}\n\nStacktrace:\n{traceback.format_exc()}",
                    test_data=test_data,
                    screenshot_path=screenshot_path
                )

        try: 
            test.teardown()
        except Exception as e:
            correct = False 
            error_msg = f"Test case teardown failed: {test_case.__name__}, Error: {e}"
            print(error_msg)
            print("TEARDOWN FAILED")
            
            # Capture screenshot on teardown failure
            screenshot_path = test.take_screenshot("teardown_failure")
            
            # Create Jira issue for teardown failure
            if jira.enabled:
                test_data = test.get_test_data()
                test_data['failure_stage'] = 'teardown'
                test_data['error_type'] = type(e).__name__
                
                jira.create_test_failure_issue(
                    test_name=test.test_name,
                    test_description=test.description,
                    error_details=f"Teardown Error: {str(e)}\n\nStacktrace:\n{traceback.format_exc()}",
                    test_data=test_data,
                    screenshot_path=screenshot_path
                )
        
        test_duration = time.time() - begin_time
        print(f"Test case duration: {test_duration:.2f} seconds || STATUS: {'Execution complete' if correct else 'Execution failed'}")
        print("-----------------------------------------------------\n")
    
    # Close driver session
    try:
        driver.quit()
        print("Driver session closed successfully")
    except Exception as e:
        print(f"Error closing driver session: {str(e)}")


if __name__ == "__main__":
    main()