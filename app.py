#!/usr/bin/env python3
"""
Flask Web Application for AI Security Testing
Provides a web-based UI for the AI Security Testing Application
"""

import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
import threading
import time

from src.config import Config
from src.test_runner import TestRunner
from src.report_generator import ReportGenerator
from src.utils.logger import setup_logger

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Global variables for storing test results and status
test_results = {}
test_status = {}
logger = setup_logger(verbose=True)

# Configuration
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/configure')
def configure():
    """Test configuration page"""
    try:
        config = Config()
        return render_template('configure.html', config=config.config)
    except Exception as e:
        flash(f'Error loading configuration: {str(e)}', 'error')
        return render_template('configure.html', config={})


@app.route('/run-test', methods=['GET', 'POST'])
def run_test():
    """Run test page"""
    if request.method == 'POST':
        try:
            # Get form data
            target_model = request.form.get('target_model')
            test_suite = request.form.get('test_suite')
            output_format = request.form.get('output_format', 'html')
            
            if not target_model or not test_suite:
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('run_test'))
            
            # Generate unique test ID
            test_id = str(uuid.uuid4())
            
            # Start test in background thread
            thread = threading.Thread(
                target=run_test_background,
                args=(test_id, target_model, test_suite, output_format)
            )
            thread.daemon = True
            thread.start()
            
            flash(f'Test started with ID: {test_id}', 'success')
            return redirect(url_for('test_status_page', test_id=test_id))
            
        except Exception as e:
            flash(f'Error starting test: {str(e)}', 'error')
            return redirect(url_for('run_test'))
    
    # GET request - show form
    try:
        config = Config()
        return render_template('run_test.html', config=config.config)
    except Exception as e:
        flash(f'Error loading configuration: {str(e)}', 'error')
        return render_template('run_test.html', config={})


@app.route('/test-status/<test_id>')
def test_status_page(test_id):
    """Test status page"""
    return render_template('test_status.html', test_id=test_id)


@app.route('/api/test-status/<test_id>')
def test_status_api(test_id):
    """API endpoint to get test status"""
    status = test_status.get(test_id, {
        'status': 'unknown',
        'message': 'Test not found'
    })
    return jsonify(status)


@app.route('/results')
def results():
    """Results page showing all test results"""
    try:
        # Get all result files
        result_files = []
        if os.path.exists(RESULTS_FOLDER):
            for filename in os.listdir(RESULTS_FOLDER):
                if filename.endswith(('.json', '.html', '.csv')):
                    filepath = os.path.join(RESULTS_FOLDER, filename)
                    stat = os.stat(filepath)
                    result_files.append({
                        'filename': filename,
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    })
        
        # Sort by modification time (newest first)
        result_files.sort(key=lambda x: x['modified'], reverse=True)
        
        return render_template('results.html', result_files=result_files)
    except Exception as e:
        flash(f'Error loading results: {str(e)}', 'error')
        return render_template('results.html', result_files=[])


@app.route('/view-result/<filename>')
def view_result(filename):
    """View a specific result file"""
    try:
        filepath = os.path.join(RESULTS_FOLDER, secure_filename(filename))
        
        if not os.path.exists(filepath):
            flash('Result file not found', 'error')
            return redirect(url_for('results'))
        
        if filename.endswith('.html'):
            return send_file(filepath)
        elif filename.endswith('.json'):
            with open(filepath, 'r') as f:
                data = json.load(f)
            return render_template('view_json_result.html', data=data, filename=filename)
        else:
            return send_file(filepath, as_attachment=True)
            
    except Exception as e:
        flash(f'Error viewing result: {str(e)}', 'error')
        return redirect(url_for('results'))


@app.route('/download-result/<filename>')
def download_result(filename):
    """Download a result file"""
    try:
        filepath = os.path.join(RESULTS_FOLDER, secure_filename(filename))
        
        if not os.path.exists(filepath):
            flash('Result file not found', 'error')
            return redirect(url_for('results'))
        
        return send_file(filepath, as_attachment=True)
        
    except Exception as e:
        flash(f'Error downloading result: {str(e)}', 'error')
        return redirect(url_for('results'))


@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """API endpoint for configuration management"""
    if request.method == 'POST':
        try:
            config_data = request.get_json()
            config = Config()
            config.update_config(config_data)
            config.save_config()
            return jsonify({'status': 'success', 'message': 'Configuration updated'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    else:
        try:
            config = Config()
            return jsonify(config.config)
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500


def run_test_background(test_id, target_model, test_suite, output_format):
    """Run test in background thread"""
    try:
        # Update status
        test_status[test_id] = {
            'status': 'running',
            'message': 'Initializing test...',
            'progress': 0,
            'start_time': datetime.now().isoformat()
        }
        
        # Initialize components
        config = Config()
        test_runner = TestRunner(target_model, config, logger)
        report_generator = ReportGenerator(config, logger)
        
        # Update status
        test_status[test_id] = {
            'status': 'running',
            'message': 'Running tests...',
            'progress': 25,
            'start_time': test_status[test_id]['start_time']
        }
        
        # Run tests
        results = test_runner.run_test_suite(test_suite)
        
        # Update status
        test_status[test_id] = {
            'status': 'running',
            'message': 'Generating report...',
            'progress': 75,
            'start_time': test_status[test_id]['start_time']
        }
        
        # Generate report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if output_format == 'json':
            output_file = os.path.join(RESULTS_FOLDER, f"security_test_{timestamp}_{test_id[:8]}.json")
            report_generator.generate_json_report(results, output_file)
        elif output_format == 'html':
            output_file = os.path.join(RESULTS_FOLDER, f"security_test_{timestamp}_{test_id[:8]}.html")
            report_generator.generate_html_report(results, output_file)
        elif output_format == 'csv':
            output_file = os.path.join(RESULTS_FOLDER, f"security_test_{timestamp}_{test_id[:8]}.csv")
            report_generator.generate_csv_report(results, output_file)
        
        # Store results
        test_results[test_id] = results
        
        # Update status - completed
        test_status[test_id] = {
            'status': 'completed',
            'message': 'Test completed successfully',
            'progress': 100,
            'start_time': test_status[test_id]['start_time'],
            'end_time': datetime.now().isoformat(),
            'results': results,
            'output_file': os.path.basename(output_file)
        }
        
    except Exception as e:
        logger.error(f"Error in background test {test_id}: {str(e)}")
        test_status[test_id] = {
            'status': 'error',
            'message': f'Test failed: {str(e)}',
            'progress': 0,
            'start_time': test_status[test_id].get('start_time', datetime.now().isoformat()),
            'end_time': datetime.now().isoformat()
        }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
