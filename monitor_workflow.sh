#!/bin/bash

# GitHub Actions workflow monitoring script
echo "🔍 Monitoring GitHub Actions workflow status..."

# Function to get latest workflow run status
get_workflow_status() {
    curl -s -H "Accept: application/vnd.github.v3+json" \
        https://api.github.com/repos/SaahilParmar/API-Test-Automation-Framework/actions/runs?per_page=1 | \
    python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if data['workflow_runs']:
        run = data['workflow_runs'][0]
        print(f'📊 Run #{run[\"run_number\"]} - {run[\"display_title\"]}')
        print(f'📅 Status: {run[\"status\"]}')
        if run.get('conclusion'):
            conclusion = run['conclusion']
            emoji = '✅' if conclusion == 'success' else '❌' if conclusion == 'failure' else '⚠️'
            print(f'{emoji} Conclusion: {conclusion}')
        print(f'🔗 URL: {run[\"html_url\"]}')
        print(f'⏰ Started: {run[\"run_started_at\"]}')
        print(f'📝 Commit: {run[\"head_sha\"][:8]}')
    else:
        print('❌ No workflow runs found')
except Exception as e:
    print(f'❌ Error: {e}')
"
}

# Monitor for up to 5 minutes with 30-second intervals
echo "⏱️  Monitoring for up to 5 minutes (30-second intervals)..."
echo ""

for i in {1..10}; do
    echo "🔄 Check $i/10:"
    get_workflow_status
    echo ""
    
    # Check if workflow is complete
    status=$(curl -s -H "Accept: application/vnd.github.v3+json" \
        https://api.github.com/repos/SaahilParmar/API-Test-Automation-Framework/actions/runs?per_page=1 | \
        python -c "import sys, json; data=json.load(sys.stdin); print(data['workflow_runs'][0]['status'] if data['workflow_runs'] else 'unknown')")
    
    if [ "$status" = "completed" ]; then
        echo "🎉 Workflow completed!"
        break
    fi
    
    if [ $i -lt 10 ]; then
        echo "⏳ Waiting 30 seconds before next check..."
        sleep 30
    fi
done

echo ""
echo "📋 Monitoring complete. Check the GitHub Actions tab for detailed logs:"
echo "   https://github.com/SaahilParmar/API-Test-Automation-Framework/actions"
