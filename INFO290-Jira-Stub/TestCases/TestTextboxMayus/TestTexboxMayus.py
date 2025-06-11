import random
import string
import time
from ..TestCaseInterface import TestCaseInterface, wait_and_find
from appium.webdriver.common.appiumby import AppiumBy


class TestTexboxMayus(TestCaseInterface):
    def __init__(self, driver):
        super().__init__(driver)  # Initialize parent class
        self.test_name = "Textbox Uppercase Test"
        self.description = "Tests if textbox converts input text to uppercase"
        
        # Test data
        self.num_iterations = 10
        self.test_strings = []
        
        # Generate random test strings
        for _ in range(self.num_iterations):
            random_string = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 20)))
            self.test_strings.append({
                'input': random_string,
                'expected': random_string.upper()
            })
        
        # Capture test configuration data
        self.capture_test_data('num_iterations', self.num_iterations)
        self.capture_test_data('test_strings', self.test_strings)

    def setup(self):
        """Navigate to the test screen and prepare test environment"""
        try:
            # Add more logging for better debugging
            print("Starting test setup...")
            
            # Try finding "Formularios" with multiple strategies

            # print("Looking for 'Formularios' button...")
            time.sleep(1)
            formularios_button = wait_and_find(self.driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Formularios")')
            formularios_button.click()
            # print("Clicked on 'Formularios'")

            # Take a screenshot to verify current state
            # self.driver.save_screenshot("after_formularios_click.png")
            time.sleep(1.5)  # Slightly longer wait to ensure page transitions
            
            # Find and click on "Prueba texto" element
            # print("Looking for 'Prueba texto' button...")
            prueba_texto_button =  wait_and_find(self.driver,AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Prueba texto")')
            prueba_texto_button.click()
            # print("Clicked on 'Prueba texto'")
            # self.driver.save_screenshot("after_prueba_texto_click.png")
            time.sleep(1)
            
            # Find and click on "Rellenar" button
            # print("Looking for 'Rellenar' button...")
            rellenar_button =  wait_and_find(self.driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Rellenar")')
            rellenar_button.click()
            # print("Clicked on 'Rellenar'")
            # self.driver.save_screenshot("after_rellenar_click.png")
            time.sleep(1)
              # Accept camera permissions if prompted
            try:
                allow_button = wait_and_find(self.driver,AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.android.permissioncontroller:id/permission_allow_foreground_only_button")')
                allow_button.click()
                print("Camera permission accepted")
                time.sleep(0.5)
            except:
                print("Camera permission dialog not found or already granted")
            
            # Capture setup completion
            self.capture_test_data('setup_completed', True)
            self.capture_test_data('setup_timestamp', time.time())
            
            return True
            
        except Exception as e:
            # Capture failure data
            self.capture_test_data('setup_completed', False)
            self.capture_test_data('setup_error', str(e))
            
            # Save screenshot on failure for debugging
            print(f"Error in setup: {e.args[0]}")
            self.take_screenshot("setup_failure")
            print("Current page source:")
            print(self.driver.page_source)
            raise e
    def run(self):
        """Execute the test - input text and verify uppercase conversion"""
        current_input = None
        current_iteration = 0
        
        try:
            results = []
            
            # Find the input field
            input_field = wait_and_find(self.driver, AppiumBy.CLASS_NAME, "android.widget.EditText")
            self.capture_test_data('input_field_found', True)

            for test_case in self.test_strings:
                current_iteration += 1
                current_input = test_case['input']
                
                # Capture current test iteration data
                self.capture_test_data('current_iteration', current_iteration)
                self.capture_test_data('current_input', current_input)
                self.capture_test_data('expected_output', test_case['expected'])

                # Clear field            
                input_field.clear()
                input_field.click()
                
                for char in test_case['input']:
                    if char.isupper():
                        # Uppercase letter - press shift + key
                        self.driver.press_keycode(59)
                        self.driver.press_keycode(29 + (ord(char) - ord('A')))
                        self.driver.press_keycode(59)  # Release shift
                    elif char.islower():
                        # Lowercase letter - press key alone
                        self.driver.press_keycode(29 + (ord(char.upper()) - ord('A')))
                
                
                # Get the actual text from the field
                actual_text = input_field.get_attribute("text")
                self.capture_test_data('actual_output', actual_text)
                
                # Verify if the text was converted to uppercase
                is_success = actual_text == test_case['expected']
                
                results.append({
                    'id': len(results) + 1,
                    'input': test_case['input'],
                    'expected': test_case['expected'],
                    'actual': actual_text,
                    'success': is_success
                })
            input_field.clear()
            return results
            
        except Exception as e:
            # Capture failure data with current test information
            self.capture_test_data('execution_failed', True)
            self.capture_test_data('failed_at_input', current_input)
            self.capture_test_data('failed_at_iteration', current_iteration)
            print(f"! - DATA: {current_input if current_input else 'No input data'}")
            raise e  
    def teardown(self):
        """Clean up after the test - return to the home screen"""
        try:
            # Click on the back button to return to home screen
            back_button =  wait_and_find(self.driver, AppiumBy.XPATH, "//com.horcrux.svg.PathView")
            back_button.click()
            time.sleep(1)
            # Clickear el boton de "Si" para confirmar el regreso a la pantalla de inicio
            wait_and_find(self.driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Si")').click()
            
            # Capture successful teardown
            self.capture_test_data('teardown_completed', True)
            self.capture_test_data('teardown_timestamp', time.time())
            
            return True
            
        except Exception as e:
            # Capture failure data
            self.capture_test_data('teardown_completed', False)
            self.capture_test_data('teardown_error', str(e))
            print(f"Error in teardown: {e.args[0]}")
            raise e
        
    def get_name(self):
        """Return the name of the test case"""
        return self.test_name
        
    def get_description(self):
        """Return the description of the test case"""
        return self.description