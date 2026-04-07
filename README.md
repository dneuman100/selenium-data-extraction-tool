# Selenium Data Extraction Tool

Python automation project that uses Selenium to extract structured records from a dynamic web platform and export them to CSV.

## Overview

This project was built to automate repetitive record lookups in a browser-based system. It reads IDs from an input CSV, navigates through a web interface, extracts structured contact information, and writes the results to an output CSV.

The script demonstrates:

- Selenium browser automation
- Dynamic page handling with explicit waits
- Extraction from inconsistent page layouts
- CSV input/output workflows
- Basic error handling and fallback logic

## Features

- Reads input records from CSV
- Searches each record through a web interface
- Extracts primary and secondary contact details
- Handles alternate page layouts
- Exports normalized results to CSV
- Uses a pluggable authentication step

## Tech Stack

- Python
- Selenium
- CSV module
- Chrome WebDriver

## Project Structure

```text
.
├── extractor.py
├── requirements.txt
├── README.md
└── sample_input.csv
