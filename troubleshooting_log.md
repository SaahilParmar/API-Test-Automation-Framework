# 🛠️ Troubleshooting Log

---

This log captures real errors and solutions encountered while setting up and running the **API Test Automation Framework**.

---

## 1️⃣ Virtual Environment Activation Errors

**Error:**

source: No such file or directory

✅ **Solution:**
- Make sure you created your virtual environment:
  ```bash
  python3 -m venv venv

Then activate:

source venv/bin/activate



---

2️⃣ pytest: unrecognized arguments

Error:

pytest: error: unrecognized arguments: --browser --headless

✅ Cause:

Those arguments belong to UI testing, not API tests.


✅ Solution:

Remove UI flags:

pytest --alluredir=reports/



---

3️⃣ Chrome Binary Not Found

Error:

selenium.common.exceptions.WebDriverException: Message: unknown error: cannot find Chrome binary

✅ Solution:

Install Chrome:

sudo apt update
sudo apt install -y google-chrome-stable



---

4️⃣ Large Files Exceed GitHub Size Limit

Error:

File google-chrome-stable_current_amd64.deb is 112.57 MB; this exceeds GitHub's file size limit of 100.00 MB

✅ Solution:

Don’t push installers into your repo.

Instead, include instructions in your README to install Chrome locally.



---

5️⃣ Git Push Failed: No Upstream

Error:

fatal: The current branch main has no upstream branch.

✅ Solution:

Run:

git push --set-upstream origin main



---

6️⃣ JSON Schema Validation Errors

Error Example:

jsonschema.exceptions.ValidationError: 'Michael' is not of type 'integer'

✅ Solution:

Double-check your schema files (e.g. user_list_schema.json) and ensure data types match your API responses.



---

7️⃣ Allure CLI Not Found

Error:

bash: allure: command not found

✅ Solution:

Install Allure CLI:

sudo apt install -y allure

Or download from: Allure Commandline Download



---

8️⃣ Import Errors for webdriver_manager

Error:

ImportError: cannot import name 'ChromeType' from 'webdriver_manager.core.utils'

✅ Solution:

For this API project, Selenium isn’t used.

Remove unused Selenium-related code.



---

9️⃣ Unknown ChromeDriver Exit Code

Error:

chromedriver unexpectedly exited. Status code was: 127

✅ Cause:

Chrome wasn’t installed or accessible.


✅ Solution:

Ensure Chrome is installed and matches your driver version.



---

✅ Tips

Always activate your virtual environment before installing packages.

Keep your requirements.txt updated.

Check the official ReqRes documentation for API endpoints and sample responses.



---

✅ This file will be updated as new issues arise.

Happy testing! 🚀
