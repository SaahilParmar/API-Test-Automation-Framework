`# 🧪 API Test Automation Framework

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

---

## 🗂️ Project Structure

api_test_framework/ ├── config/ │   └── config.yaml ├── data/ │   ├── large_payload.json │   └── post_user_payloads.json ├── schemas/ │   ├── create_user_schema.json │   ├── single_user_schema.json │   └── user_list_schema.json ├── tests/ │   └── test_users_api.py ├── utils/ │   └── api_utils.py ├── logs/ ├── reports/ ├── requirements.txt ├── README.md ├── troubleshooting_log.md └── conftest.py

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
│   └── test_users_api.py
├── utils/
│   └── api_utils.py
├── logs/
├── reports/
├── requirements.txt
├── README.md
├── troubleshooting_log.md
└── conftest.py

`
📸 *Screenshot of project structure:*  
`![Project Structure](images/1_project_structure.png)`

---

## ⚙️ Installation & Setup

```bash
# Clone this repo
git clone https://github.com/YOUR-USERNAME/api_test_automation_framework.git
cd api_test_automation_framework

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

📸 Chrome installation step (Linux):
![Chrome Installed](images/2_chrome_install.jpg)


---

🧪 Running Tests

pytest --alluredir=reports/

📸 Virtual environment activated:
![Venv](images/9_venv.jpg)
📸 Requirements installed:
![Requirements](images/10_requirements.jpg)


---

📊 Generate Allure Report

allure generate reports/ -o reports/html --clean
allure open reports/html

📸 Allure report example:
![Allure Report](images/allure_report.png)


---

🚦 Test Categories

Type	Description

✔️ Smoke	Basic GET/POST status checks
📃 Contract	Schema validation with jsonschema
🔁 Data-Driven	POST tests with multiple payloads
🚫 Negative	Invalid input and boundary tests
🧪 Regression	Full test suite



---

🧱 Markers

@pytest.mark.smoke

@pytest.mark.regression


Run specific tests:

pytest -m smoke


---

🛠 Troubleshooting

See troubleshooting_log.md for common errors and fixes (e.g., Chrome driver, Allure, virtualenv).


---

🤝 Contributing

Pull requests are welcome. Please open an issue first to discuss changes.


---

📄 License

This project is licensed under the MIT License.
