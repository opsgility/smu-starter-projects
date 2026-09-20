"""PyForge Data Pipeline — Capstone Project

Build a complete CLI tool that:
1. Reads configuration from environment variables and a JSON config file
2. Fetches data from a REST API with pagination
3. Transforms the data using classes and list comprehensions
4. Handles errors gracefully with logging
5. Outputs results as both CSV and JSON files
6. Prints a summary report to the terminal
"""

from pyforge.cli import run

if __name__ == "__main__":
    run()
