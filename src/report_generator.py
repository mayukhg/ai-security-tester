"""
Report generator for AI Security Testing Application
"""

import json
import csv
from datetime import datetime
from typing import Dict, Any, List


class ReportGenerator:
    """Generates reports in various formats"""

    def __init__(self, config: 'Config', logger: Any):
        self.config = config
        self.logger = logger

    def generate_json_report(self, results: Dict[str, Any], output_file: str):
        """Generate a JSON report"""
        self.logger.info(f"Generating JSON report: {output_file}")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": results.get("total_tests", 0),
                "passed_tests": results.get("passed_tests", 0),
                "failed_tests": results.get("failed_tests", 0),
                "vulnerabilities_found": results.get("vulnerabilities_found", 0)
            },
            "test_results": results.get("details", [])
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"JSON report saved to {output_file}")

    def generate_html_report(self, results: Dict[str, Any], output_file: str):
        """Generate an HTML report"""
        self.logger.info(f"Generating HTML report: {output_file}")
        
        html_content = self._generate_html_content(results)
        
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        self.logger.info(f"HTML report saved to {output_file}")

    def generate_csv_report(self, results: Dict[str, Any], output_file: str):
        """Generate a CSV report"""
        self.logger.info(f"Generating CSV report: {output_file}")
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Test Name', 'Passed', 'Vulnerable', 'Error'])
            
            for test_result in results.get("details", []):
                writer.writerow([
                    test_result.get("test_name", ""),
                    test_result.get("passed", False),
                    test_result.get("vulnerable", False),
                    test_result.get("error", "")
                ])
        
        self.logger.info(f"CSV report saved to {output_file}")

    def _generate_html_content(self, results: Dict[str, Any]) -> str:
        """Generate HTML content for the report"""
        total_tests = results.get("total_tests", 0)
        passed_tests = results.get("passed_tests", 0)
        failed_tests = results.get("failed_tests", 0)
        vulnerabilities = results.get("vulnerabilities_found", 0)
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>AI Security Test Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .summary {{
            background-color: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .metric {{
            display: inline-block;
            margin: 10px 20px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }}
        .metric-label {{
            font-size: 0.9em;
            color: #7f8c8d;
        }}
        .vulnerable {{
            color: #e74c3c;
        }}
        .safe {{
            color: #27ae60;
        }}
        .test-results {{
            background-color: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .test-item {{
            padding: 10px;
            border-bottom: 1px solid #ecf0f1;
        }}
        .test-name {{
            font-weight: bold;
            color: #2c3e50;
        }}
        .test-status {{
            margin-left: 20px;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 0.9em;
        }}
        .passed {{
            background-color: #d5edda;
            color: #155724;
        }}
        .failed {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        .warning {{
            background-color: #fff3cd;
            color: #856404;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>AI Security Test Report</h1>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <h2>Summary</h2>
        <div class="metric">
            <div class="metric-value">{total_tests}</div>
            <div class="metric-label">Total Tests</div>
        </div>
        <div class="metric">
            <div class="metric-value safe">{passed_tests}</div>
            <div class="metric-label">Passed</div>
        </div>
        <div class="metric">
            <div class="metric-value">{failed_tests}</div>
            <div class="metric-label">Failed</div>
        </div>
        <div class="metric">
            <div class="metric-value {'vulnerable' if vulnerabilities > 0 else 'safe'}">{vulnerabilities}</div>
            <div class="metric-label">Vulnerabilities</div>
        </div>
    </div>
    
    <div class="test-results">
        <h2>Test Results</h2>
        {self._generate_test_items_html(results.get("details", []))}
    </div>
</body>
</html>
        """
        
        return html

    def _generate_test_items_html(self, test_details: List[Dict[str, Any]]) -> str:
        """Generate HTML for individual test items"""
        html = ""
        
        for test in test_details:
            test_name = test.get("test_name", "Unknown Test")
            passed = test.get("passed", False)
            vulnerable = test.get("vulnerable", False)
            error = test.get("error", "")
            
            if passed:
                status_class = "passed"
                status_text = "✓ PASSED"
            elif vulnerable:
                status_class = "warning"
                status_text = "⚠️ VULNERABLE"
            else:
                status_class = "failed"
                status_text = "✗ FAILED"
            
            html += f"""
            <div class="test-item">
                <div class="test-name">{test_name}</div>
                <span class="test-status {status_class}">{status_text}</span>
                {f'<div style="color: #e74c3c; margin-top: 5px; font-size: 0.9em;">Error: {error}</div>' if error else ''}
            </div>
            """
        
        return html
