#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Alerting module for the Agricultural AI System.

This module evaluates metrics collected by the MetricsCollector against
predefined rules and thresholds, triggering alerts through various channels
when conditions are met.
"""

import os
import time
import logging
import yaml
import smtplib
import requests
import threading
from email.mime.text import MIMEText
from datetime import datetime

# Import the metrics collector (assuming it's in the same directory or path)
try:
    from .metrics_collector import MetricsCollector
except ImportError:
    # Allow running standalone for testing
    from metrics_collector import MetricsCollector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=\'%(asctime)s - %(name)s - %(levelname)s - %(message)s\'
)
logger = logging.getLogger(\'alerter\')

class Alerter:
    """
    Evaluates metrics and triggers alerts based on configured rules.
    
    This class works in conjunction with the MetricsCollector. It periodically
    checks the latest metrics against rules defined in a configuration file
    and sends notifications through configured channels (log, email, webhook)
    if any rules are triggered.
    """
    
    def __init__(self, metrics_collector, config_path="../config/monitoring.yaml"):
        """
        Initialize the Alerter.
        
        Args:
            metrics_collector (MetricsCollector): Instance of the metrics collector
            config_path (str): Path to the monitoring configuration file
        """
        self.metrics_collector = metrics_collector
        self.config_path = config_path
        self.config = self._load_config()
        
        # Alert state management to avoid spamming
        self.alert_states = {} # {rule_name: {\"triggered\": bool, \"last_triggered_time\": timestamp}}
        self.cooldown_period = self.config.get(\"alerting\", {}).get(\"cooldown_period_seconds\", 300) # 5 minutes default
        
        # Thread control
        self.running = False
        self.evaluation_thread = None
        self.evaluation_interval = self.config.get(\"alerting\", {}).get(\"evaluation_interval_seconds\", 60) # 1 minute default
        
        logger.info("Alerter initialized")

    def _load_config(self):
        """Loads monitoring and alerting configuration from YAML file."""
        try:
            # Adjust path relative to this script\s location if needed
            script_dir = os.path.dirname(os.path.abspath(__file__))
            absolute_config_path = os.path.join(script_dir, self.config_path)
            
            with open(absolute_config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            logger.info(f"Monitoring configuration loaded from {absolute_config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found at {absolute_config_path}. Using defaults.")
            return {}
        except Exception as e:
            logger.error(f"Error loading configuration: {e}. Using defaults.")
            return {}

    def start(self):
        """Start the alert evaluation thread."""
        if self.running:
            logger.warning("Alerter is already running")
            return
        
        if not self.config or "alerting" not in self.config or "rules" not in self.config["alerting"]:
            logger.error("Alerting configuration is missing or invalid. Cannot start alerter.")
            return
            
        self.running = True
        self.evaluation_thread = threading.Thread(target=self._evaluation_loop, daemon=True)
        self.evaluation_thread.start()
        logger.info("Alert evaluation started")

    def stop(self):
        """Stop the alert evaluation thread."""
        self.running = False
        if self.evaluation_thread:
            self.evaluation_thread.join(timeout=5.0)
            logger.info("Alert evaluation stopped")

    def _evaluation_loop(self):
        """Main loop for evaluating metrics against rules."""
        while self.running:
            try:
                latest_metrics = self.metrics_collector.get_latest_metrics()
                if latest_metrics:
                    self._evaluate_rules(latest_metrics)
            except Exception as e:
                logger.error(f"Error during alert evaluation loop: {e}", exc_info=True)
            
            time.sleep(self.evaluation_interval)

    def _evaluate_rules(self, metrics):
        """Evaluate all configured rules against the latest metrics."""
        rules = self.config.get(\"alerting\", {}).get(\"rules\", [])
        current_time = time.time()
        
        for rule in rules:
            rule_name = rule.get(\"name\")
            metric_path = rule.get(\"metric\") # e.g., \"system.cpu_usage\"
            condition = rule.get(\"condition\") # e.g., \">\"
            threshold = rule.get(\"threshold\")
            severity = rule.get(\"severity\", \"info\")
            channels = rule.get(\"channels\", [\"log\"])
            
            if not all([rule_name, metric_path, condition, threshold is not None]):
                logger.warning(f"Skipping invalid rule: {rule}")
                continue

            # Get metric value
            try:
                metric_parts = metric_path.split(\".\")
                value = metrics
                for part in metric_parts:
                    if isinstance(value, dict):
                        value = value.get(part)
                    else:
                        value = None # Metric not found or path invalid
                        break
                
                if value is None:
                    logger.debug(f"Metric \"{metric_path}\" not found for rule \"{rule_name}\"")
                    continue
                    
                # Handle nested metrics like response times
                if isinstance(value, dict) and metric_path.endswith(\"response_times\"):
                    # Example: Check average response time
                    if \"avg\" in value:
                        value = value[\"avg\"]
                    else:
                         logger.debug(f"Specific response time metric (e.g., avg) not found in {metric_path}")
                         continue

            except Exception as e:
                logger.error(f"Error accessing metric \"{metric_path}\" for rule \"{rule_name}\": {e}")
                continue

            # Evaluate condition
            triggered = False
            try:
                if condition == \">\":
                    triggered = value > threshold
                elif condition == \">=\":
                    triggered = value >= threshold
                elif condition == \"<\":
                    triggered = value < threshold
                elif condition == \"<=\":
                    triggered = value <= threshold
                elif condition == \"==\":
                    triggered = value == threshold
                elif condition == \"!=\":
                    triggered = value != threshold
                else:
                    logger.warning(f"Unsupported condition \"{condition}\" in rule \"{rule_name}\"")
                    continue
            except TypeError:
                 logger.warning(f"Type error comparing metric \"{metric_path}\" ({type(value)}) with threshold \"{threshold}\" ({type(threshold)}) for rule \"{rule_name}\"")
                 continue
            except Exception as e:
                logger.error(f"Error evaluating condition for rule \"{rule_name}\": {e}")
                continue

            # Manage alert state and cooldown
            state = self.alert_states.get(rule_name, {"triggered": False, "last_triggered_time": 0})
            
            if triggered:
                if not state["triggered"]:
                    # Check cooldown
                    if current_time - state.get(\"last_resolved_time\", 0) > self.cooldown_period:
                        logger.info(f"Alert triggered for rule: {rule_name}")
                        self._trigger_alert(rule, value)
                        state["triggered"] = True
                        state["last_triggered_time"] = current_time
                    else:
                        logger.debug(f"Alert {rule_name} is in cooldown period.")
                # Keep updating last triggered time while alert is active
                state["last_triggered_time"] = current_time 
            else:
                if state["triggered"]:
                    logger.info(f"Alert resolved for rule: {rule_name}")
                    self._resolve_alert(rule)
                    state["triggered"] = False
                    state["last_resolved_time"] = current_time # Record resolution time for cooldown
            
            self.alert_states[rule_name] = state

    def _trigger_alert(self, rule, current_value):
        """Send alert notifications through configured channels."""
        rule_name = rule[\"name\"]
        severity = rule[\"severity\"]
        message = f\"ALERT [{severity.upper()}]: Rule \\\"{rule_name}\\\" triggered. Metric {rule[\"metric\"]} ({current_value}) {rule[\"condition\"]} {rule[\"threshold\"]}.\"
        
        for channel_name in rule[\"channels\"]:
            channel_config = self.config.get(\"alerting\", {}).get(\"channels\", {}).get(channel_name)
            if not channel_config:
                logger.warning(f"Channel \"{channel_name}\" not configured for rule \"{rule_name}\"")
                continue
                
            channel_type = channel_config.get(\"type\")
            
            try:
                if channel_type == \"log\":
                    self._send_log_alert(message, severity)
                elif channel_type == \"email\":
                    self._send_email_alert(channel_config, f\"Alert: {rule_name}\", message)
                elif channel_type == \"webhook\":
                    self._send_webhook_alert(channel_config, rule, current_value, message, is_resolved=False)
                else:
                    logger.warning(f"Unsupported channel type \"{channel_type}\" for rule \"{rule_name}\"")
            except Exception as e:
                logger.error(f"Failed to send alert via channel \"{channel_name}\" for rule \"{rule_name}\": {e}")

    def _resolve_alert(self, rule):
        """Send notification when an alert condition is resolved."""
        # Optional: Send resolution notifications
        send_resolution = self.config.get(\"alerting\", {}).get(\"send_resolution_notifications\", False)
        if not send_resolution:
            return
            
        rule_name = rule[\"name\"]
        severity = rule[\"severity\"]
        message = f\"RESOLVED [{severity.upper()}]: Alert condition for rule \\\"{rule_name}\\\" is no longer met.\"
        
        for channel_name in rule[\"channels\"]:
            channel_config = self.config.get(\"alerting\", {}).get(\"channels\", {}).get(channel_name)
            if not channel_config:
                continue
                
            channel_type = channel_config.get(\"type\")
            
            try:
                if channel_type == \"log\":
                    self._send_log_alert(message, \"info\") # Log resolution as info
                elif channel_type == \"email\":
                    self._send_email_alert(channel_config, f\"Resolved: {rule_name}\", message)
                elif channel_type == \"webhook\":
                    # Send minimal info for resolution
                    self._send_webhook_alert(channel_config, rule, None, message, is_resolved=True)
            except Exception as e:
                logger.error(f"Failed to send resolution notification via channel \"{channel_name}\" for rule \"{rule_name}\": {e}")

    def _send_log_alert(self, message, severity):
        """Send alert to system log."""
        if severity == \"critical\":
            logger.critical(message)
        elif severity == \"error\":
            logger.error(message)
        elif severity == \"warning\":
            logger.warning(message)
        else:
            logger.info(message)

    def _send_email_alert(self, config, subject, body):
        """Send alert via email."""
        smtp_server = config.get(\"smtp_server\")
        smtp_port = config.get(\"smtp_port\", 587)
        smtp_user = config.get(\"smtp_user\")
        smtp_password = config.get(\"smtp_password\")
        sender_email = config.get(\"sender_email\")
        recipient_emails = config.get(\"recipients\")
        use_tls = config.get(\"use_tls\", True)

        if not all([smtp_server, smtp_user, smtp_password, sender_email, recipient_emails]):
            logger.error(\"Email channel configuration is incomplete\")
            return

        msg = MIMEText(body)
        msg[\"Subject\"] = subject
        msg[\"From\"] = sender_email
        msg[\"To\"] = \", \".join(recipient_emails)

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                if use_tls:
                    server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(sender_email, recipient_emails, msg.as_string())
            logger.info(f"Email alert sent to {recipient_emails}")
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")

    def _send_webhook_alert(self, config, rule, current_value, message, is_resolved):
        """Send alert via webhook."""
        url = config.get(\"url\")
        method = config.get(\"method\", \"POST\").upper()
        headers = config.get(\"headers\", {\"Content-Type\": \"application/json\"})
        payload_template = config.get(\"payload\")

        if not url:
            logger.error(\"Webhook URL is not configured\")
            return

        # Construct payload
        if payload_template:
            # Use a simple template format
            payload = json.loads(json.dumps(payload_template).format(
                rule_name=rule[\"name\"],
                metric=rule[\"metric\"] if not is_resolved else \"N/A\",
                condition=rule[\"condition\"] if not is_resolved else \"N/A\",
                threshold=rule[\"threshold\"] if not is_resolved else \"N/A\",
                current_value=current_value if not is_resolved else \"N/A\",
                severity=rule[\"severity\"],
                message=message,
                status=\"resolved\" if is_resolved else \"firing\",
                timestamp=datetime.now().isoformat()
            ))
        else:
            # Default payload
            payload = {
                "rule_name": rule[\"name\"],
                "status": \"resolved\" if is_resolved else \"firing\",
                "severity": rule[\"severity\"],
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            if not is_resolved:
                 payload.update({
                     "metric": rule[\"metric\"],
                     "condition": rule[\"condition\"],
                     "threshold": rule[\"threshold\"],
                     "current_value": current_value
                 })

        try:
            response = requests.request(method, url, headers=headers, json=payload, timeout=10)
            response.raise_for_status() # Raise exception for bad status codes
            logger.info(f"Webhook alert sent to {url}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send webhook alert to {url}: {e}")

# Example usage
if __name__ == "__main__":
    # Create a dummy metrics collector
    class DummyCollector:
        def get_latest_metrics(self):
            # Simulate some metrics
            return {
                \"system\": {
                    \"cpu_usage\": random.uniform(10, 95),
                    \"memory_usage\": random.uniform(30, 90),
                    \"disk_usage\": 75.0,
                },
                \"application\": {
                    \"request_count\": random.randint(50, 150),
                    \"error_count\": random.randint(0, 10),
                    \"response_times\": {\"avg\": random.uniform(0.1, 1.5), \"p95\": random.uniform(0.5, 2.5)}
                },
                \"model\": {}
            }
        def start(self): pass
        def stop(self): pass

    import random
    
    # Create dummy config file
    dummy_config_content = """
alerting:
  evaluation_interval_seconds: 10
  cooldown_period_seconds: 30
  send_resolution_notifications: true
  channels:
    log_channel:
      type: log
    email_channel: # Placeholder - requires real SMTP details
      type: email
      smtp_server: \"smtp.example.com\"
      smtp_port: 587
      smtp_user: \"user@example.com\"
      smtp_password: \"password\"
      sender_email: \"alerts@example.com\"
      recipients:
        - \"admin@example.com\"
    webhook_channel: # Placeholder - use a service like webhook.site for testing
      type: webhook
      url: \"https://webhook.site/your-unique-url\" # Replace with your test URL
      method: POST
      payload: # Example custom payload for Slack
        text: \"> {status}: *{rule_name}*\n> _{message}_\"
        # payload: # Default payload example
        #   rule_name: \"{rule_name}\"
        #   status: \"{status}\"
        #   severity: \"{severity}\"
        #   message: \"{message}\"
        #   timestamp: \"{timestamp}\"

  rules:
    - name: \"High CPU Usage\"
      metric: \"system.cpu_usage\"
      condition: \">\"
      threshold: 85.0
      severity: \"warning\"
      channels: [\"log_channel\", \"webhook_channel\"]
    - name: \"High Memory Usage\"
      metric: \"system.memory_usage\"
      condition: \">\"
      threshold: 80.0
      severity: \"error\"
      channels: [\"log_channel\", \"email_channel\"] # Email for critical errors
    - name: \"High Error Rate\"
      metric: \"application.error_count\"
      condition: \">\"
      threshold: 5 # Errors per interval (10s in this example)
      severity: \"warning\"
      channels: [\"log_channel\"]
    - name: \"Slow Response Time (Avg)\"
      metric: \"application.response_times.avg\"
      condition: \">\"
      threshold: 1.0 # seconds
      severity: \"info\"
      channels: [\"log_channel\"]
"""
    dummy_config_path = "../config/monitoring.yaml"
    os.makedirs(os.path.dirname(dummy_config_path), exist_ok=True)
    with open(dummy_config_path, "w") as f:
        f.write(dummy_config_content)

    # Create alerter instance
    collector = DummyCollector()
    alerter = Alerter(collector, config_path=dummy_config_path)
    alerter.start()

    print("Alerter started. Monitoring for alerts... Press Ctrl+C to stop.")

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping alerter...")
    finally:
        alerter.stop()
        # Clean up dummy config
        # os.remove(dummy_config_path)
        print("Alerter stopped.")

