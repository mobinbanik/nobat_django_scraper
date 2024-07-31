import os
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init()

# File path for the CSV log
log_file_path = 'log.csv'

# Define the log levels and their colors
log_levels = {
    'INFO': Fore.GREEN,
    'WARNING': Fore.YELLOW,
    'ERROR': Fore.RED,
}

# Define the colors for each part of the log message
time_color = Fore.CYAN
level_color_map = {
    'INFO': Fore.GREEN,
    'WARNING': Fore.YELLOW,
    'ERROR': Fore.RED,
}
message_color = Fore.MAGENTA

def log_message(*messages, level='INFO', custom_level=None):
    """
    Logs a message to a CSV file and prints it in color to the terminal.
    
    Parameters:
        *messages: Variable length argument list for log messages.
        level (str): The level of the log ('INFO', 'WARNING', 'ERROR').
    """
    if level not in log_levels:
        raise ValueError(f"Unsupported log level: {level}")

    # Get current time and date
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Prepare the log entry
    if custom_level is not None:
        log_entry = f"{current_time},{custom_level},{','.join(messages)}\n"
    else:
        log_entry = f"{current_time},{level},{','.join(messages)}\n"

    # Write the log entry to the CSV file
    with open(log_file_path, 'a', encoding="utf-8") as log_file:
        if os.stat(log_file_path).st_size == 0:
            # Write header if file is empty
            log_file.write("Time,Level,Messages\n")
        log_file.write(log_entry)

    # Get the color for the level
    level_color = level_color_map[level]

    # Print the log in color to the terminal
    if custom_level is not None:
        print(f"{time_color}{current_time}{Style.RESET_ALL} - {level_color}{custom_level}{Style.RESET_ALL} - {message_color}{' | '.join(messages)}{Style.RESET_ALL}")
    else:
        print(f"{time_color}{current_time}{Style.RESET_ALL} - {level_color}{level}{Style.RESET_ALL} - {message_color}{' | '.join(messages)}{Style.RESET_ALL}")


def main():
    # Examples of how to use the log_message function
    log_message('This is an info message', 'Additional info', level='INFO')
    log_message('This is a warning message', level='WARNING')
    log_message('This is an error message', 'Details of the error', level='ERROR')


if __name__ == '__main__':
    main()
