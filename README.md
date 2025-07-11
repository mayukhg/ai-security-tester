# 🛡️ AI Security Testing Application

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/web-Flask-green.svg)](https://flask.palletsprojects.com/)

A comprehensive, enterprise-grade toolkit for testing the security vulnerabilities of AI models, featuring both web-based and command-line interfaces. This application helps security researchers, AI developers, and organizations assess their AI systems against various attack vectors including prompt injection, adversarial attacks, jailbreaking attempts, and bias evaluation.

## 🎯 Purpose & Vision

### Why This Tool Exists
As AI systems become increasingly integrated into critical applications, **security testing becomes paramount**. This tool addresses the growing need for systematic security assessment of AI models by providing:

- **Standardized Testing Framework**: Consistent methodologies for evaluating AI security
- **Comprehensive Attack Coverage**: Multiple attack vectors in one unified platform  
- **Accessibility**: Both technical (CLI) and non-technical (Web UI) interfaces
- **Research-Grade Analysis**: Detailed reporting for security research and compliance
- **Responsible Disclosure**: Tools for ethical security research and vulnerability disclosure

### Target Audience
- 🔬 **Security Researchers**: Investigating AI vulnerabilities and attack methodologies
- 👨‍💻 **AI/ML Engineers**: Testing model robustness during development
- 🏢 **Enterprise Security Teams**: Assessing AI systems before production deployment
- 🎓 **Academic Researchers**: Studying AI security and publishing research findings
- 📋 **Compliance Teams**: Meeting regulatory requirements for AI system security

## 🏗️ Architecture Overview

### System Design
```
┌─────────────────────────────────────────────────────────────┐
│                     AI Security Tester                     │
├─────────────────────────────────────────────────────────────┤
│  Web Interface (Flask)     │     CLI Interface (argparse)   │
│  ├─ Dashboard              │     ├─ main.py                 │
│  ├─ Test Configuration     │     ├─ Command line args       │
│  ├─ Real-time Monitoring   │     └─ Batch processing        │
│  └─ Results Visualization  │                                 │
├─────────────────────────────────────────────────────────────┤
│                    Core Testing Engine                      │
│  ├─ Test Runner (test_runner.py)                           │
│  ├─ Configuration Manager (config.py)                      │
│  ├─ Report Generator (report_generator.py)                 │
│  └─ Logging System (utils/logger.py)                       │
├─────────────────────────────────────────────────────────────┤
│                      Test Modules                          │
│  ├─ Prompt Injection Tests                                 │
│  ├─ Adversarial Attack Tests                               │
│  ├─ Jailbreaking Tests                                     │
│  ├─ Data Extraction Tests                                  │
│  └─ Bias & Fairness Tests                                  │
├─────────────────────────────────────────────────────────────┤
│                    Model Interfaces                        │
│  ├─ OpenAI API Integration                                 │
│  ├─ Anthropic API Integration                              │
│  ├─ Local Model Support                                    │
│  └─ Custom Endpoint Support                                │
├─────────────────────────────────────────────────────────────┤
│                  Output & Reporting                        │
│  ├─ JSON Reports (machine-readable)                        │
│  ├─ HTML Reports (human-readable)                          │
│  ├─ CSV Exports (data analysis)                            │
│  └─ Real-time Status Updates                               │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. **Web Interface (`app.py`)**
- **Purpose**: User-friendly web interface for non-technical users
- **Technology**: Flask web framework with Bootstrap UI
- **Features**: 
  - Real-time test monitoring with AJAX updates
  - Interactive configuration management
  - Visual report viewing and downloading
  - Responsive design for mobile/desktop

#### 2. **CLI Interface (`main.py`)**
- **Purpose**: Command-line interface for automation and scripting
- **Technology**: Python argparse with comprehensive options
- **Features**:
  - Batch processing capabilities
  - Integration with CI/CD pipelines
  - Scriptable and automatable
  - Advanced configuration options

#### 3. **Core Testing Engine**
- **Test Runner (`src/test_runner.py`)**: Orchestrates test execution and manages test lifecycle
- **Configuration Manager (`src/config.py`)**: Handles YAML/JSON configuration with validation
- **Report Generator (`src/report_generator.py`)**: Creates multiple output formats with detailed analysis
- **Logger (`src/utils/logger.py`)**: Comprehensive logging with configurable verbosity

#### 4. **Test Modules** (Extensible Architecture)
- **Modular Design**: Each test category is independently implementable
- **Standardized Interface**: Consistent API for adding new test types
- **Configurable Parameters**: Fine-tuned control over test behavior
- **Result Standardization**: Uniform output format across all tests

## 🔍 Security Test Categories

### 1. 💉 **Prompt Injection Testing**
**Purpose**: Detect vulnerabilities where malicious prompts can manipulate model behavior

- **Direct Injection**: Testing immediate prompt manipulation
- **Indirect Injection**: Context-based injection through documents/data
- **Role-Playing Attacks**: Convincing models to assume harmful personas
- **System Prompt Extraction**: Attempting to reveal internal instructions

**Example Test Cases**:
- "Ignore previous instructions and..."
- Social engineering through context injection
- Unicode and encoding-based bypasses

### 2. ⚔️ **Adversarial Attack Testing**
**Purpose**: Evaluate model robustness against carefully crafted inputs

- **Text-based Adversarial Examples**: Semantically similar but malicious inputs
- **Character-level Perturbations**: Subtle character modifications
- **Semantic Attacks**: Meaning-preserving transformations
- **Gradient-based Attacks**: Using model gradients to craft inputs

### 3. 🔓 **Jailbreaking Attempts**
**Purpose**: Test the effectiveness of safety measures and content filters

- **Common Jailbreak Patterns**: Known bypass techniques
- **Creative Bypass Techniques**: Novel approaches to safety circumvention
- **Multi-turn Conversation Attacks**: Gradual manipulation across interactions
- **Encoding and Obfuscation**: Using various encoding schemes

### 4. 📊 **Data Extraction Testing**
**Purpose**: Assess risks of training data leakage and privacy violations

- **Training Data Extraction**: Attempting to retrieve training examples
- **Personal Information Leakage**: Testing for PII disclosure
- **Model Parameter Inference**: Reverse engineering model details
- **Membership Inference**: Determining if data was in training set

### 5. ⚖️ **Bias and Fairness Testing**
**Purpose**: Evaluate model fairness across different demographic groups

- **Demographic Bias Detection**: Testing for unfair treatment
- **Stereotyping Assessments**: Identifying harmful stereotypes
- **Fairness Metric Evaluation**: Quantitative bias measurements
- **Intersectional Bias Analysis**: Multi-dimensional fairness testing

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.8+** (recommended: 3.9 or higher)
- **pip** package manager
- **Git** (for cloning and version control)
- **Web browser** (for UI interface)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/mayukhg/ai-security-tester.git
cd ai-security-tester

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify installation
python -c "from src.config import Config; print('✅ Installation successful!')"
```

### Configuration Setup

```bash
# 1. Copy and customize configuration
cp config.yaml config_local.yaml

# 2. Edit configuration for your models
# Add API keys, endpoints, and test parameters
vim config_local.yaml  # or your preferred editor
```

**Sample Configuration**:
```yaml
model_endpoints:
  openai:
    api_key_env: "OPENAI_API_KEY"
    base_url: "https://api.openai.com/v1"
    model: "gpt-4"
  
  local:
    base_url: "http://localhost:8000"
    model: "local-llama"

test_suites:
  basic: ["prompt_injection_basic", "jailbreak_basic"]
  comprehensive: ["prompt_injection_comprehensive", "adversarial_attacks", "bias_testing"]

attack_parameters:
  max_attempts: 5
  timeout: 30
  rate_limit: 1.0
```

## 💻 Usage Examples

### Web Interface (Recommended for Most Users)

```bash
# Start the web application
python app.py

# Access the interface
# Open browser to: http://localhost:5000
```

**Web Interface Features**:
- 📊 **Dashboard**: Overview and quick start
- ⚙️ **Configuration**: Visual config editor
- ▶️ **Run Tests**: Interactive test setup
- 📈 **Real-time Monitoring**: Live progress updates
- 📋 **Results**: Browse and download reports

### Command Line Interface (For Automation)

```bash
# Basic security test
python main.py --target-model "gpt-3.5-turbo" --test-suite basic

# Comprehensive assessment with custom output
python main.py \
  --target-model "http://localhost:8000/v1/chat/completions" \
  --test-suite comprehensive \
  --output-format json \
  --output-dir ./my-results \
  --save-results \
  --verbose

# Custom test configuration
python main.py \
  --config ./config_local.yaml \
  --target-model "claude-3-sonnet" \
  --test-suite custom \
  --custom-tests ./my-tests.json
```

### Advanced Usage

```bash
# Batch testing multiple models
for model in "gpt-4" "claude-3-sonnet" "local-model"; do
  python main.py --target-model "$model" --test-suite comprehensive
done

# Integration with CI/CD
python main.py --target-model "$MODEL_ENDPOINT" --test-suite basic --output-format json > security-report.json
```

## 📊 Output Formats & Reports

### Report Types

#### 1. **HTML Reports** (Human-Readable)
- Interactive visualizations
- Detailed test descriptions
- Color-coded severity levels
- Exportable and shareable

#### 2. **JSON Reports** (Machine-Readable)
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "summary": {
    "total_tests": 15,
    "vulnerabilities_found": 3,
    "severity_breakdown": {"high": 1, "medium": 2, "low": 0}
  },
  "test_results": [...]
}
```

#### 3. **CSV Reports** (Data Analysis)
- Tabular format for spreadsheet analysis
- Statistical aggregation
- Trend analysis over time

### Report Contents
- **Executive Summary**: High-level findings and recommendations
- **Detailed Results**: Test-by-test breakdown
- **Vulnerability Analysis**: Severity assessment and remediation
- **Compliance Mapping**: Alignment with security frameworks
- **Recommendations**: Specific improvement suggestions

## 🔧 Configuration Management

### Configuration Files
- **`config.yaml`**: Default configuration template
- **`config_local.yaml`**: Local customizations (git-ignored)
- **Environment Variables**: Sensitive data (API keys, secrets)

### Configuration Categories

#### Model Endpoints
```yaml
model_endpoints:
  production_gpt:
    api_key_env: "PROD_OPENAI_KEY"
    base_url: "https://api.openai.com/v1"
    model: "gpt-4"
    headers:
      "User-Agent": "Security-Tester/1.0"
```

#### Test Parameters
```yaml
attack_parameters:
  max_attempts: 10        # Maximum test iterations
  timeout: 60            # Request timeout in seconds
  rate_limit: 0.5        # Requests per second
  retry_count: 3         # Retry failed tests
  parallel_tests: 4      # Concurrent test execution
```

#### Output Settings
```yaml
output:
  include_prompts: true     # Include test prompts in reports
  include_responses: true   # Include model responses
  include_metadata: true    # Include timing and metadata
  severity_threshold: "medium"  # Minimum severity to report
  anonymize_data: false     # Anonymize sensitive data
```

## 🔒 Security & Ethics

### Ethical Guidelines

#### ✅ **Permitted Uses**
- Security research on your own models
- Academic research with proper disclosure
- Pre-deployment testing of AI systems
- Compliance and audit requirements
- Educational and training purposes

#### ❌ **Prohibited Uses**
- Testing models without explicit permission
- Malicious attacks on production systems
- Circumventing security for harmful purposes
- Violating terms of service of AI providers
- Any illegal or unethical activities

### Best Practices

1. **Responsible Disclosure**: Report vulnerabilities to model providers
2. **Data Protection**: Handle test results securely and confidentially
3. **Rate Limiting**: Respect API limits and avoid overloading systems
4. **Documentation**: Maintain detailed logs for accountability
5. **Legal Compliance**: Ensure testing complies with applicable laws

### Security Considerations

```bash
# Use environment variables for sensitive data
export OPENAI_API_KEY="your-api-key-here"
export ANTHROPIC_API_KEY="your-anthropic-key"

# Secure file permissions
chmod 600 config_local.yaml
chmod 600 results/*.json

# Network security
# Use VPN or secure networks for testing
# Monitor network traffic for data leaks
```

## 🧪 Testing & Development

### Running Tests

```bash
# Unit tests
python -m pytest tests/unit/

# Integration tests
python -m pytest tests/integration/

# Coverage report
python -m pytest --cov=src tests/

# Linting and formatting
flake8 src/
black src/
```

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Pre-commit hooks
pre-commit install

# Run in development mode
export FLASK_ENV=development
python app.py
```

### Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Extending the Framework

#### Adding New Test Types
```python
# src/tests/my_custom_test.py
class MyCustomTest:
    def __init__(self, config):
        self.config = config
    
    def run(self, model_endpoint):
        # Implement your test logic
        return {
            "test_name": "my_custom_test",
            "passed": True,
            "vulnerable": False,
            "details": {...}
        }
```

#### Adding New Model Integrations
```python
# src/integrations/my_model.py
class MyModelIntegration:
    def __init__(self, config):
        self.config = config
    
    def send_request(self, prompt):
        # Implement model communication
        return response
```

## 📚 Documentation & Resources

### Additional Documentation
- **[API Documentation](docs/api.md)**: Detailed API reference
- **[Test Methodology](docs/methodology.md)**: Testing approaches and techniques
- **[Security Guidelines](docs/security.md)**: Comprehensive security practices
- **[Deployment Guide](docs/deployment.md)**: Production deployment instructions

### Research Papers & References
- "Prompt Injection Attacks and Defenses" (arXiv:2023.xxxxx)
- "Adversarial Examples in Natural Language Processing" 
- "Bias and Fairness in Large Language Models"
- OWASP Top 10 for Machine Learning Security

### Community & Support
- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Community Q&A and best practices
- **Security Reports**: Responsible disclosure process
- **Documentation Wiki**: Community-contributed guides

## 📈 Roadmap & Future Development

### Version 2.0 (Planned)
- **Advanced Adversarial Attacks**: Gradient-based and optimization attacks
- **Multimodal Testing**: Support for vision and audio models
- **Automated Remediation**: Suggested fixes for discovered vulnerabilities
- **Enterprise Features**: SSO, RBAC, and audit logging
- **Cloud Integration**: Native support for cloud AI services

### Long-term Vision
- **AI Security Framework**: Industry-standard testing protocols
- **Compliance Automation**: Automated regulatory compliance checking
- **Real-time Monitoring**: Continuous security monitoring in production
- **Community Test Database**: Shared vulnerability patterns and tests

## 📄 License & Attribution

**MIT License** - See [LICENSE](LICENSE) file for details

### Citation
If you use this tool in your research, please cite:

```bibtex
@software{ai_security_tester,
  title={AI Security Testing Application},
  author={Mayukh Ghosh},
  year={2024},
  url={https://github.com/mayukhg/ai-security-tester}
}
```

### Acknowledgments
- Security research community for attack methodologies
- Open source libraries and frameworks used
- AI safety and alignment research community
- Beta testers and early adopters

---

**⚠️ Important Legal Notice**: This tool is provided for legitimate security research and testing purposes only. Users are responsible for ensuring compliance with applicable laws, regulations, and terms of service. The authors assume no liability for misuse of this software.

**🔗 Quick Links**: [Documentation](docs/) | [Issues](https://github.com/mayukhg/ai-security-tester/issues) | [Discussions](https://github.com/mayukhg/ai-security-tester/discussions) | [Security Policy](SECURITY.md)
