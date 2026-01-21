import logging
import os
from datetime import datetime
import json

# Create logs directory
LOGS_DIR = 'logs'
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Get today's date for log filenames
today = datetime.now().strftime("%Y%m%d")

# Log file paths
APP_LOG_FILE = f'{LOGS_DIR}/application_{today}.log'
ACTIVITY_LOG_FILE = f'{LOGS_DIR}/user_activity_{today}.log'
REGISTRATION_LOG_FILE = f'{LOGS_DIR}/registrations_{today}.json'

# Create logger function
def create_logger(name, log_file, level=logging.INFO):
    """Create a logger with file and console handlers"""
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler (saves to file)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler (prints to terminal) - THIS IS IMPORTANT!
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# Create loggers
app_logger = create_logger('app', APP_LOG_FILE)
activity_logger = create_logger('activity', ACTIVITY_LOG_FILE)

# Helper functions
def log_app_startup():
    """Log when application starts"""
    app_logger.info("=" * 80)
    app_logger.info("🚀 APPLICATION STARTED")
    app_logger.info(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    app_logger.info("=" * 80)

def log_page_navigation(from_page, to_page):
    """Log when user navigates between pages"""
    activity_logger.info(f"PAGE_NAVIGATION | From: {from_page} → To: {to_page}")
    app_logger.info(f"User navigated from {from_page} to {to_page}")

def log_registration_attempt(name, email):
    """Log when someone tries to register"""
    activity_logger.info(f"REGISTRATION_ATTEMPT | Name: {name} | Email: {email}")
    app_logger.info(f"Registration attempt - Name: {name}, Email: {email}")

def log_validation_error(field, error_message, user_input=""):
    """Log validation failures"""
    activity_logger.warning(f"VALIDATION_FAILED | Field: {field} | Error: {error_message} | Input: {user_input}")
    app_logger.warning(f"Validation failed - {field}: {error_message}")

def log_validation_success(field):
    """Log successful validation"""
    activity_logger.info(f"VALIDATION_SUCCESS | Field: {field}")

def log_successful_registration(name, email, registration_date):
    """Log successful registration to JSON file and regular logs"""
    
    # Create registration data
    registration_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "email": email,
        "registration_date": registration_date,
        "status": "SUCCESS"
    }
    
    # Write to JSON file
    try:
        with open(REGISTRATION_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(registration_data, ensure_ascii=False) + '\n')
        
        activity_logger.info(f"✅ REGISTRATION_SUCCESS | Name: {name} | Email: {email} | Date: {registration_date}")
        app_logger.info(f"✅ Registration successful! User: {name} ({email})")
        
    except Exception as e:
        app_logger.error(f"Failed to save registration data: {str(e)}")

def log_registration_failure(email, errors):
    """Log when registration fails"""
    activity_logger.warning(f"❌ REGISTRATION_FAILED | Email: {email} | Errors: {len(errors)}")
    app_logger.warning(f"Registration failed for {email} - {len(errors)} validation errors")

def log_terms_not_accepted(email):
    """Log when user doesn't accept terms"""
    activity_logger.warning(f"TERMS_NOT_ACCEPTED | Email: {email}")
    app_logger.warning(f"User {email} did not accept terms and conditions")

def log_dashboard_access(name, email):
    """Log when user accesses dashboard"""
    activity_logger.info(f"DASHBOARD_ACCESS | Name: {name} | Email: {email}")
    app_logger.info(f"Dashboard accessed by {name} ({email})")
