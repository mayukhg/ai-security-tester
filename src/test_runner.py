"""
Test runner for AI Security Testing Application
"""

import json
from typing import Dict, Any, List


class TestRunner:
    """Runs the test suites against the specified target model"""

    def __init__(self, target_model: str, config: 'Config', logger: Any):
        self.target_model = target_model
        self.config = config
        self.logger = logger
        self.custom_tests = []

    def load_custom_tests(self, custom_tests_file: str):
        """Load custom tests from a JSON file"""
        self.logger.info(f"Loading custom tests from {custom_tests_file}")
        try:
            with open(custom_tests_file, 'r') as f:
                self.custom_tests = json.load(f).get('tests', [])
        except Exception as e:
            self.logger.error(f"Failed to load custom tests: {str(e)}")

    def run_test_suite(self, suite_name: str) -> Dict[str, Any]:
        """Run the specified test suite"""
        self.logger.info(f"Running test suite: {suite_name}")
        test_suite = self.config.get_test_suite(suite_name)
        results = {
            "total_tests": len(test_suite),
            "passed_tests": 0,
            "failed_tests": 0,
            "vulnerabilities_found": 0,
            "details": []
        }

        for test in test_suite:
            test_result = self.run_test(test)
            results["details"].append(test_result)
            if test_result.get("passed"):
                results["passed_tests"] += 1
            else:
                results["failed_tests"] += 1
                if test_result.get("vulnerable"):
                    results["vulnerabilities_found"] += 1

        self.logger.info(f"Test suite completed. {results['vulnerabilities_found']} vulnerabilities found.")
        return results

    def run_test(self, test_name: str) -> Dict[str, Any]:
        """Run a single test and return its result"""
        self.logger.debug(f"Running test: {test_name}")
        try:
            # Simulated test result
            result = self._simulate_test_run(test_name)

            self.logger.debug(f"Test {test_name} result: {result}")
            return result

        except Exception as e:
            self.logger.error(f"Error running test {test_name}: {str(e)}")
            return {
                "test_name": test_name,
                "passed": False,
                "vulnerable": False,
                "error": str(e)
            }

    def _simulate_test_run(self, test_name: str) -> Dict[str, Any]:
        """Simulate running a test and return a fake result"""
        # Simulate some tests passing or failing for the demo
        fake_results = {
            "prompt_injection_basic": {
                "passed": True,
                "vulnerable": False
            },
            "jailbreak_basic": {
                "passed": False,
                "vulnerable": True
            },
            "data_extraction_basic": {
                "passed": True,
                "vulnerable": False
            }
        }

        return {
            "test_name": test_name,
            **fake_results.get(test_name, {"passed": False, "vulnerable": False})
        }
