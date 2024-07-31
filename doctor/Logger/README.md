# Advanced Python Logger


![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Pandas](https://img.shields.io/badge/pandas-1.2%2B-yellow)
![Colorama](https://img.shields.io/badge/colorama-0.4.4%2B-red)
![License](https://img.shields.io/badge/license-MIT-green)

A lightweight and efficient logging utility for Python, designed to log messages with different severity levels, save them to a CSV file, and display them with color-coded output in the terminal.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Requirements](#requirements)
- [Author](#author)
- [License](#license)

## Description

`Advanced Python Logger` is a simple yet powerful logging tool for Python applications. It allows you to log messages of varying importance (INFO, WARNING, ERROR) to a CSV file and also prints them in the terminal with distinct colors for better readability.

## Features

- **CSV Logging**: Saves logs in a lightweight CSV format.
- **Colored Terminal Output**: Displays logs in the terminal with different colors for time, severity level, and messages.
- **Customizable**: Easy to add new log levels and customize the output.
- **Efficient**: Uses incremental writing to the CSV file for better performance with high-frequency logging.

## Installation

To use the Advanced Python Logger, ensure you have Python 3.7 or higher installed. Then, install the necessary packages using pip:

```bash
pip install pandas colorama
```

## Usage

Here's a simple example of how to use the `Advanced Python Logger` in your Python application:

```python
from logger import AdvancedLogger

# Initialize the logger
logger = AdvancedLogger(log_file='log.csv')

# Log messages with different severity levels
logger.info('This is an info message.')
logger.warning('This is a warning message.')
logger.error('This is an error message.')
```

## Examples

### Logging an Info Message

```python
logger.info('Application started successfully.')
```

### Logging a Warning Message

```python
logger.warning('This action is deprecated.')
```

### Logging an Error Message

```python
logger.error('An error occurred while connecting to the database.')
```

## Requirements

- Python 3.7+
- pandas
- colorama

## Author

Developed by Mobin Banik.  
GitHub: [https://github.com/mobinbanik](https://github.com/mobinbanik)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
