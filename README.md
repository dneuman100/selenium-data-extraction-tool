# Selenium Data Extraction Tool

Python automation project that uses Selenium to extract structured records from a dynamic web platform and export them to CSV.

## Overview

This project automates repetitive record lookups in a browser-based system. It reads record IDs from an input CSV, navigates through a web interface, extracts structured contact information, and writes the results to an output CSV.

This public version is intentionally sanitized:
- no real credentials
- no sensitive URLs
- no private data
- generic selectors and field names

## Files in This Repo

- `extractor.py` - main Selenium automation script
- `sample_input.csv` - example input file
- `requirements.txt` - Python dependency list

## Setup

### 1. Install Python
Make sure Python 3 is installed on your computer.

### 2. Install ChromeDriver
Download ChromeDriver and note the path on your machine.

### 3. Install the required package

```bash
pip install -r requirements.txt
