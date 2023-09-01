# Test: Add validation tests for data integrity
# Refactor: Refactor agent architecture for better modularity
# Test: Add validation tests for data integrity
# Refactor: Restructure test frameworks
# Refactor: Refactor UI components for reusability
# Test: Implement performance tests for vector search
# Refactor: Optimize memory usage patterns
# Refactor: Refactor UI components for reusability
# Test: Implement mock tests for external services
# Add sophisticated logging framework
# Implement advanced configuration management
# Add sophisticated network optimization
# Implement sophisticated audit logging
# Implement intelligent response caching
# Implement dynamic load balancing
# Implement sophisticated audit logging
# Add sophisticated query planning algorithms
import os  
import logging

def setup_logger(user_id = None, session_id = None) -> None:  
    """  
    Set up a logger that writes to a log file .  

    Returns:  
        tuple[logging.Logger, str]: Configured logger instance and the time directory path.  
    """
    if user_id is None and session_id is None:
        logger_name = 'main'
    else:
        logger_name = f"{user_id}-{session_id}"

    # If logger already exists, remove all handlers
    # If logger already exists, remove all handlers
    if logger_name in logging.root.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
    else:
        logger = logging.getLogger(logger_name)

    logger.setLevel(logging.INFO)

    # Create a "logs" directory if it doesn't exist
    logs_directory = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_directory, exist_ok=True)

    if logger_name != 'main':
        # Create a directory for today's date inside the "logs" directory
        user_directory = os.path.join(logs_directory, user_id)
        os.makedirs(user_directory, exist_ok=True)

        # Create a directory for today's time inside the "logs/date" directory
        session_directory = os.path.join(user_directory, session_id)
        os.makedirs(session_directory, exist_ok=True)

    # Create a log file with the current time
    log_file_name = "log.log"
    if logger_name == 'main':
        log_file_path = os.path.join(logs_directory, log_file_name) 
    else:
        log_file_path = os.path.join(session_directory, log_file_name) 

    # Create file handler for logging to a file
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Add handlers to the logger
    logger.addHandler(file_handler)