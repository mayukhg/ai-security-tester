"""
Configuration management for AI Security Testing Application
"""

import yaml
import json
from typing import Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class AttackConfig:
    """Configuration for attack parameters"""
    max_attempts: int = 5
    timeout: int = 30
    rate_limit: float = 1.0  # requests per second
    retry_count: int = 3


@dataclass
class TestConfig:
    """Configuration for test parameters"""
    prompt_injection: AttackConfig = field(default_factory=AttackConfig)
    adversarial: AttackConfig = field(default_factory=AttackConfig)
    jailbreak: AttackConfig = field(default_factory=AttackConfig)
    data_extraction: AttackConfig = field(default_factory=AttackConfig)
    bias_testing: AttackConfig = field(default_factory=AttackConfig)


class Config:
    """Main configuration class"""
    
    def __init__(self, config_file: str = "config.yaml"):
        self.config_file = config_file
        self.config = self._load_config()
        self.test_config = self._parse_test_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                if self.config_file.endswith('.yaml') or self.config_file.endswith('.yml'):
                    return yaml.safe_load(f)
                elif self.config_file.endswith('.json'):
                    return json.load(f)
                else:
                    raise ValueError(f"Unsupported config file format: {self.config_file}")
        except FileNotFoundError:
            # Return default configuration if file doesn't exist
            return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "model_endpoints": {
                "openai": {
                    "api_key_env": "OPENAI_API_KEY",
                    "base_url": "https://api.openai.com/v1",
                    "model": "gpt-3.5-turbo"
                },
                "anthropic": {
                    "api_key_env": "ANTHROPIC_API_KEY",
                    "base_url": "https://api.anthropic.com/v1",
                    "model": "claude-3-sonnet-20240229"
                },
                "local": {
                    "base_url": "http://localhost:8000",
                    "model": "local-model"
                }
            },
            "test_suites": {
                "basic": [
                    "prompt_injection_basic",
                    "jailbreak_basic",
                    "data_extraction_basic"
                ],
                "comprehensive": [
                    "prompt_injection_comprehensive",
                    "adversarial_attacks",
                    "jailbreak_comprehensive",
                    "data_extraction_comprehensive",
                    "bias_testing",
                    "privacy_leakage"
                ]
            },
            "attack_parameters": {
                "max_attempts": 5,
                "timeout": 30,
                "rate_limit": 1.0,
                "retry_count": 3
            },
            "output": {
                "include_prompts": True,
                "include_responses": True,
                "include_metadata": True,
                "severity_threshold": "medium"
            },
            "safety": {
                "content_filtering": True,
                "harmful_content_detection": True,
                "automatic_stop": True
            }
        }
    
    def _parse_test_config(self) -> TestConfig:
        """Parse test configuration from loaded config"""
        attack_params = self.config.get("attack_parameters", {})
        
        return TestConfig(
            prompt_injection=AttackConfig(
                max_attempts=attack_params.get("max_attempts", 5),
                timeout=attack_params.get("timeout", 30),
                rate_limit=attack_params.get("rate_limit", 1.0),
                retry_count=attack_params.get("retry_count", 3)
            ),
            adversarial=AttackConfig(
                max_attempts=attack_params.get("max_attempts", 5),
                timeout=attack_params.get("timeout", 30),
                rate_limit=attack_params.get("rate_limit", 1.0),
                retry_count=attack_params.get("retry_count", 3)
            ),
            jailbreak=AttackConfig(
                max_attempts=attack_params.get("max_attempts", 5),
                timeout=attack_params.get("timeout", 30),
                rate_limit=attack_params.get("rate_limit", 1.0),
                retry_count=attack_params.get("retry_count", 3)
            ),
            data_extraction=AttackConfig(
                max_attempts=attack_params.get("max_attempts", 5),
                timeout=attack_params.get("timeout", 30),
                rate_limit=attack_params.get("rate_limit", 1.0),
                retry_count=attack_params.get("retry_count", 3)
            ),
            bias_testing=AttackConfig(
                max_attempts=attack_params.get("max_attempts", 5),
                timeout=attack_params.get("timeout", 30),
                rate_limit=attack_params.get("rate_limit", 1.0),
                retry_count=attack_params.get("retry_count", 3)
            )
        )
    
    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """Get configuration for a specific model"""
        return self.config.get("model_endpoints", {}).get(model_name, {})
    
    def get_test_suite(self, suite_name: str) -> List[str]:
        """Get test suite configuration"""
        return self.config.get("test_suites", {}).get(suite_name, [])
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration"""
        return self.config.get("output", {})
    
    def get_safety_config(self) -> Dict[str, Any]:
        """Get safety configuration"""
        return self.config.get("safety", {})
    
    def save_config(self, output_file: str = None):
        """Save current configuration to file"""
        output_file = output_file or self.config_file
        
        with open(output_file, 'w') as f:
            if output_file.endswith('.yaml') or output_file.endswith('.yml'):
                yaml.dump(self.config, f, default_flow_style=False)
            elif output_file.endswith('.json'):
                json.dump(self.config, f, indent=2)
            else:
                raise ValueError(f"Unsupported output file format: {output_file}")
    
    def update_config(self, updates: Dict[str, Any]):
        """Update configuration with new values"""
        self.config.update(updates)
        self.test_config = self._parse_test_config()
