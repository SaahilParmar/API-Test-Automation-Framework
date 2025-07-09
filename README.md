# 🧪 API Test Automation Framework

A professional API testing framework built using **Python**, **Pytest**, and **Allure** for reporting.  
This framework is designed to test RESTful APIs using data-driven and contract-based testing approaches.  
Target API: [ReqRes Public API](https://reqres.in/)

---

## ✅ Features

- Modular and scalable folder structure
- Configurable environments (e.g. dev, staging)
- JSON Schema validation (contract testing)
- Data-driven POST testing
- Boundary and negative test cases
- Retry logic and timeouts
- Allure report integration
- Pytest markers and logging
- Compatible with CI/CD (via GitHub Actions)
- Isolated virtual environment in `.venv`

---

## 🗂️ Project Structure

```
api_test_framework/
├── config/
│   └── config.yaml
├── data/
│   ├── large_payload.json
│   └── post_user_payloads.json
├── schemas/
│   ├── create_user_schema.json
│   ├── single_user_schema.json
│   └── user_list_schema.json
├── tests/
│   ├── test_user_retrieval.py      # GET operations & user listing
│   ├── test_user_creation.py       # POST operations & user creation
│   ├── test_error_scenarios.py     # 404, invalid requests, edge cases
│   ├── test_api_validation.py      # Schema validation & headers
├── utils/
│   └── api_utils.py
├── logs/
├── reports/
├── requirements.txt
├── pytest.ini                     # Test configuration & markers
├── test_runner.sh                 # Test execution script
├── setup.sh                      # Automated setup script
├── README.md
├── troubleshooting_log.md
└── conftest.py
```

📸 *Screenshot of project structure:*  
![Project_Structure]()


---

## ⚙️ Installation & Setup

### Quick Setup (Recommended)
```bash
# Clone this repo
git clone https://github.com/YOUR-USERNAME/api_test_automation_framework.git
cd api_test_automation_framework

# Run the setup script (creates venv and installs dependencies)
./setup.sh
```

### Manual Setup
```bash
# Clone this repo
git clone https://github.com/YOUR-USERNAME/api_test_automation_framework.git
cd api_test_automation_framework

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

📸 Chrome installation step (Linux):
![Chrome Installed](images/2_chrome_install.jpg)


---

---

## 🚀 Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/API-Test-Automation-Framework.git
   cd API-Test-Automation-Framework
   ```

2. Run the setup script (creates `.venv` and installs dependencies):
   ```bash
   ./setup.sh
   ```

3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate     # On Windows
   ```

4. Run the tests:
   ```bash
   pytest tests/ -v          # Run all tests
   pytest tests/ -m smoke    # Run smoke tests only
   ```

⚠️ Important: Always use the `.venv` virtual environment. This is the standard environment used by our CI/CD workflow and ensures consistent test execution across all environments.

## 🛠️ Development Setup

1. Ensure you're using the correct virtual environment:
   ```bash
   # You should see (.venv) in your prompt
   # If not, activate it:
   source .venv/bin/activate
   ```

2. Verify your setup:
   ```bash
   python --version  # Should match version in .github/workflows/ci.yml
   pip list         # Should match requirements.txt
   ```

3. Install new dependencies:
   ```bash
   pip install new-package
   pip freeze > requirements.txt  # Update requirements
   ```
