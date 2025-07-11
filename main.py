#!/usr/bin/env python3
"""
AI Security Testing Application
Main entry point for running security tests against AI models
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any

from src.config import Config
from src.test_runner import TestRunner
from src.report_generator import ReportGenerator
from src.utils.logger import setup_logger


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="AI Security Testing Application",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--target-model",
        required=True,
        help="Target model endpoint or identifier"
    )
    
    parser.add_argument(
        "--test-suite",
        choices=["basic", "comprehensive", "custom"],
        default="basic",
        help="Test suite to run (default: basic)"
    )
    
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Configuration file path (default: config.yaml)"
    )
    
    parser.add_argument(
        "--output-format",
        choices=["json", "html", "csv"],
        default="html",
        help="Output format (default: html)"
    )
    
    parser.add_argument(
        "--output-dir",
        default="results",
        help="Output directory for results (default: results)"
    )
    
    parser.add_argument(
        "--save-results",
        action="store_true",
        help="Save detailed results to file"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--custom-tests",
        help="Path to custom test definitions (JSON file)"
    )
    
    return parser.parse_args()


def main():
    """Main application entry point"""
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logger(verbose=args.verbose)
    logger.info("Starting AI Security Testing Application")
    
    try:
        # Load configuration
        config = Config(args.config)
        
        # Initialize test runner
        test_runner = TestRunner(
            target_model=args.target_model,
            config=config,
            logger=logger
        )
        
        # Load custom tests if specified
        if args.custom_tests:
            test_runner.load_custom_tests(args.custom_tests)
        
        # Run tests
        logger.info(f"Running {args.test_suite} test suite against {args.target_model}")
        results = test_runner.run_test_suite(args.test_suite)
        
        # Generate report
        report_generator = ReportGenerator(config, logger)
        
        # Create output directory
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Generate report based on format
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if args.output_format == "json":
            output_file = os.path.join(args.output_dir, f"security_test_{timestamp}.json")
            report_generator.generate_json_report(results, output_file)
        elif args.output_format == "html":
            output_file = os.path.join(args.output_dir, f"security_test_{timestamp}.html")
            report_generator.generate_html_report(results, output_file)
        elif args.output_format == "csv":
            output_file = os.path.join(args.output_dir, f"security_test_{timestamp}.csv")
            report_generator.generate_csv_report(results, output_file)
        
        # Print summary
        print_summary(results)
        
        if args.save_results:
            logger.info(f"Results saved to {output_file}")
            print(f"\\nDetailed results saved to: {output_file}")
        
    except Exception as e:
        logger.error(f"Error running security tests: {str(e)}")
        sys.exit(1)


def print_summary(results: Dict[str, Any]):
    """Print a summary of test results"""
    total_tests = results.get("total_tests", 0)
    passed_tests = results.get("passed_tests", 0)
    failed_tests = results.get("failed_tests", 0)
    vulnerabilities = results.get("vulnerabilities_found", 0)
    
    print("\\n" + "="*50)
    print("SECURITY TEST SUMMARY")
    print("="*50)
    print(f"Total Tests Run: {total_tests}")
    print(f"Tests Passed: {passed_tests}")
    print(f"Tests Failed: {failed_tests}")
    print(f"Vulnerabilities Found: {vulnerabilities}")
    
    if vulnerabilities > 0:
        print("\\n⚠️  SECURITY VULNERABILITIES DETECTED!")
        print("Please review the detailed report for remediation steps.")
    else:
        print("\\n✅ No major security vulnerabilities detected.")
    
    print("="*50)


if __name__ == "__main__":
    main()
