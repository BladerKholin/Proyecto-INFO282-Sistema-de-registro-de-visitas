import requests
import base64
import json
import os
from datetime import datetime
import traceback

class JiraIntegration:
    def __init__(self):
        """Initialize Jira integration with environment variables"""
        self.jira_url = os.getenv('JIRA_URL')  # e.g., 'https://yourcompany.atlassian.net'
        self.jira_username = os.getenv('JIRA_USERNAME')  # Your email
        self.jira_api_token = os.getenv('JIRA_API_TOKEN')  # API Token from Jira
        self.jira_project_key = os.getenv('JIRA_PROJECT_KEY')  # e.g., 'TEST'
        self.issue_type = os.getenv('JIRA_ISSUE_TYPE', 'Bug')  # Default to Bug
        
        # Validate required configuration
        if not all([self.jira_url, self.jira_username, self.jira_api_token, self.jira_project_key]):
            print("Warning: Jira integration not fully configured. Check environment variables:")
            print("- JIRA_URL")
            print("- JIRA_USERNAME") 
            print("- JIRA_API_TOKEN")
            print("- JIRA_PROJECT_KEY")
            self.enabled = False
        else:
            self.enabled = True
            
        # Create auth header
        if self.enabled:
            credentials = f"{self.jira_username}:{self.jira_api_token}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            self.headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/json'
            }

    def create_test_failure_issue(self, test_name, test_description, error_details, test_data=None, screenshot_path=None):
        """
        Create a Jira issue for a test failure
        
        Args:
            test_name: Name of the failed test
            test_description: Description of the test
            error_details: Exception details and stacktrace
            test_data: Dictionary with test data at the time of failure
            screenshot_path: Path to screenshot file (optional)
        """
        if not self.enabled:
            print("Jira integration not enabled. Skipping issue creation.")
            return None
            
        try:
            # Generate issue summary and description
            summary = f"[Automated Test Failure] {test_name}"
            
            description = self._generate_issue_description(
                test_name, test_description, error_details, test_data
            )
            
            # Create the issue
            issue_data = {
                "fields": {
                    "project": {"key": self.jira_project_key},
                    "summary": summary,
                    "description": description,
                    "issuetype": {"name": self.issue_type},
                    "priority": {"name": "Medium"},
                    "labels": ["automated-test", "test-failure", "appium"]
                }
            }
            
            # Add custom fields if needed (uncomment and modify as needed)
            # issue_data["fields"]["customfield_xxxxx"] = "Test Automation"
            
            response = requests.post(
                f"{self.jira_url}/rest/api/3/issue",
                headers=self.headers,
                data=json.dumps(issue_data)
            )
            
            if response.status_code == 201:
                issue_key = response.json()['key']
                print(f"✅ Jira issue created successfully: {issue_key}")
                
                # Attach screenshot if provided
                if screenshot_path and os.path.exists(screenshot_path):
                    self._attach_screenshot(issue_key, screenshot_path)
                
                return issue_key
            else:
                print(f"❌ Failed to create Jira issue. Status: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating Jira issue: {str(e)}")
            traceback.print_exc()
            return None

    def _generate_issue_description(self, test_name, test_description, error_details, test_data):
        """Generate a detailed issue description"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        description = f"""
h2. Test Failure Summary
*Test Name:* {test_name}
*Test Description:* {test_description}
*Failure Time:* {timestamp}
*Environment:* Android Emulator (emulator-5554)

h2. Error Details
{{code:java}}
{error_details}
{{code}}

h2. Test Data at Time of Failure
"""
        
        if test_data:
            description += "{{code:json}}\n"
            description += json.dumps(test_data, indent=2, default=str)
            description += "\n{{code}}\n"
        else:
            description += "No test data captured\n"
            
        description += """
h2. Environment Information
* Platform: Android
* Device: emulator-5554
* Automation Framework: Appium + Selenium
* Test Type: UI Automation

h2. Reproduction Steps
1. Run the automated test suite
2. Execute the failing test case
3. Observe the failure

h2. Expected vs Actual
Review the test data above for expected vs actual results.

---
_This issue was created automatically by the test automation framework._
"""
        return description

    def _attach_screenshot(self, issue_key, screenshot_path):
        """Attach a screenshot to the Jira issue"""
        try:
            with open(screenshot_path, 'rb') as file:
                files = {'file': file}
                headers_no_content = {k: v for k, v in self.headers.items() if k != 'Content-Type'}
                
                response = requests.post(
                    f"{self.jira_url}/rest/api/3/issue/{issue_key}/attachments",
                    headers=headers_no_content,
                    files=files
                )
                
                if response.status_code == 200:
                    print(f"✅ Screenshot attached to issue {issue_key}")
                else:
                    print(f"❌ Failed to attach screenshot. Status: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Error attaching screenshot: {str(e)}")

    def add_comment_to_issue(self, issue_key, comment):
        """Add a comment to an existing Jira issue"""
        if not self.enabled:
            return None
            
        try:
            comment_data = {
                "body": comment
            }
            
            response = requests.post(
                f"{self.jira_url}/rest/api/3/issue/{issue_key}/comment",
                headers=self.headers,
                data=json.dumps(comment_data)
            )
            
            if response.status_code == 201:
                print(f"✅ Comment added to issue {issue_key}")
                return True
            else:
                print(f"❌ Failed to add comment. Status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error adding comment: {str(e)}")
            return False

    def transition_issue(self, issue_key, transition_name):
        """Transition an issue to a different status (e.g., 'In Progress', 'Resolved')"""
        if not self.enabled:
            return None
            
        try:
            # Get available transitions
            response = requests.get(
                f"{self.jira_url}/rest/api/3/issue/{issue_key}/transitions",
                headers=self.headers
            )
            
            if response.status_code == 200:
                transitions = response.json()['transitions']
                transition_id = None
                
                for transition in transitions:
                    if transition['name'].lower() == transition_name.lower():
                        transition_id = transition['id']
                        break
                
                if transition_id:
                    transition_data = {
                        "transition": {"id": transition_id}
                    }
                    
                    response = requests.post(
                        f"{self.jira_url}/rest/api/3/issue/{issue_key}/transitions",
                        headers=self.headers,
                        data=json.dumps(transition_data)
                    )
                    
                    if response.status_code == 204:
                        print(f"✅ Issue {issue_key} transitioned to {transition_name}")
                        return True
                    else:
                        print(f"❌ Failed to transition issue. Status: {response.status_code}")
                        return False
                else:
                    print(f"❌ Transition '{transition_name}' not available for issue {issue_key}")
                    return False
            else:
                print(f"❌ Failed to get transitions. Status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error transitioning issue: {str(e)}")
            return False
