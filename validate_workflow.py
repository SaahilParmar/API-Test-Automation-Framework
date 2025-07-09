#!/usr/bin/env python3

import yaml
import sys
import os


def validate_workflow():
    workflow_file = ".github/workflows/ci.yml"

    if not os.path.exists(workflow_file):
        print(f"❌ Workflow file not found: {workflow_file}")
        return False

    try:
        with open(workflow_file, 'r') as file:
            workflow = yaml.safe_load(file)

        print("✅ YAML syntax is valid")
        print(f"📋 Workflow name: {workflow.get('name', 'Unknown')}")
        print(f"🔧 Number of jobs: {len(workflow.get('jobs', {}))}")

        # Check required sections
        required_sections = ['on', 'jobs']
        for section in required_sections:
            if section in workflow:
                print(f"✅ Required section '{section}' found")
            else:
                print(f"❌ Required section '{section}' missing")
                return False

        # Check jobs structure
        jobs = workflow.get('jobs', {})
        job_names = list(jobs.keys())
        print(f"🏗️  Jobs found: {', '.join(job_names)}")

        for job_name, job_config in jobs.items():
            if 'runs-on' not in job_config:
                print(f"❌ Missing 'runs-on' for job: {job_name}")
                return False

        # Check for environment variables
        if 'env' in workflow:
            print(f"🌍 Environment variables: {list(workflow['env'].keys())}")

        # Check permissions
        if 'permissions' in workflow:
            print(f"🔐 Permissions configured: {list(workflow['permissions'].keys())}")

        print("\n🎉 Workflow validation passed!")
        return True

    except yaml.YAMLError as e:
        print(f"❌ YAML syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = validate_workflow()
    sys.exit(0 if success else 1)
