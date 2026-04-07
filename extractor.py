"""
Selenium Data Extraction Tool

This script demonstrates browser automation against a generic record-search
web platform. It reads record IDs from a CSV file, opens each record in the
browser, extracts structured contact information, and writes normalized output
to a new CSV file.

This public version is intentionally sanitized:
- No real credentials are included
- No sensitive URLs are included
- Field names are generic
- Authentication is a placeholder step you replace locally
"""

import csv
import os
import sys
import time
from dataclasses import dataclass
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ----------------------------
# Configuration
# ----------------------------

CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "/path/to/chromedriver")
TARGET_URL = os.getenv("TARGET_URL", "https://example.com/record-search")
INPUT_CSV = os.getenv("INPUT_CSV", "sample_input.csv")
OUTPUT_CSV = os.getenv("OUTPUT_CSV", "output_data.csv")
WAIT_TIMEOUT = int(os.getenv("WAIT_TIMEOUT", "10"))


# ----------------------------
# Data model
# ----------------------------

@dataclass
class ContactRecord:
    name: str = "N/A"
    relationship: str = "N/A"
    language_spoken: str = "N/A"
    language_written: str = "N/A"
    home_phone: str = "N/A"
    cell_phone: str = "N/A"
    email: str = "N/A"


# ----------------------------
# Browser helpers
# ----------------------------

def build_driver() -> WebDriver:
    """Create and return a Chrome WebDriver."""
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver


def wait_for_clickable(driver: WebDriver, by: By, value: str, timeout: int = WAIT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )


def wait_for_present(driver: WebDriver, by: By, value: str, timeout: int = WAIT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def safe_find_text(driver: WebDriver, by: By, value: str, default: str = "N/A") -> str:
    """Return element text if found, else default."""
    try:
        return driver.find_element(by, value).text.strip()
    except Exception:
        return default


def safe_wait_text(
    driver: WebDriver,
    by: By,
    value: str,
    timeout: int = 2,
    default: str = "N/A",
) -> str:
    """Wait briefly for an element and return its text if present."""
    try:
        element = wait_for_present(driver, by, value, timeout=timeout)
        return element.text.strip()
    except Exception:
        return default


# ----------------------------
# Authentication
# ----------------------------

def authenticate(driver: WebDriver) -> None:
    """
    Placeholder login step.

    Why this exists:
    - Your real login flow should not be pushed to GitHub if it contains
      credentials, secrets, or system-specific details.
    - For a public portfolio repo, it is better to leave login as a manual
      step or replace it with a local private helper on your own machine.

    How to use it:
    1. The script opens the target page.
    2. You log in manually in the browser window that appears.
    3. After login is complete, return to the terminal and press Enter.
    """
    print("\nManual login required.")
    print("1. Log into the site in the opened browser window.")
    print("2. Return here and press Enter once the record-search page is ready.\n")
    input("Press Enter to continue...")


# ----------------------------
# CSV helpers
# ----------------------------

def get_input_ids(csv_path: str) -> List[str]:
    """
    Read record IDs from the third column of the input CSV.

    Expected format:
    first_name,last_name,record_id
    Jane,Doe,12345
    """
    record_ids: List[str] = []

    with open(csv_path, newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        next(reader, None)  # skip header if present
        for row in reader:
            if len(row) >= 3 and row[2].strip():
                record_ids.append(row[2].strip())

    return record_ids


def flatten_contacts(record_id: str, contacts: List[ContactRecord]) -> Dict[str, str]:
    primary = contacts[0] if len(contacts) > 0 else ContactRecord()
    secondary = contacts[1] if len(contacts) > 1 else ContactRecord()

    return {
        "record_id": record_id,
        "primary_name": primary.name,
        "primary_relationship": primary.relationship,
        "primary_language_spoken": primary.language_spoken,
        "primary_language_written": primary.language_written,
        "primary_home_phone": primary.home_phone,
        "primary_cell_phone": primary.cell_phone,
        "primary_email": primary.email,
        "secondary_name": secondary.name,
        "secondary_relationship": secondary.relationship,
        "secondary_language_spoken": secondary.language_spoken,
        "secondary_language_written": secondary.language_written,
        "secondary_home_phone": secondary.home_phone,
        "secondary_cell_phone": secondary.cell_phone,
        "secondary_email": secondary.email,
    }


def get_output_fieldnames() -> List[str]:
    return [
        "record_id",
        "primary_name",
        "primary_relationship",
        "primary_language_spoken",
        "primary_language_written",
        "primary_home_phone",
        "primary_cell_phone",
        "primary_email",
        "secondary_name",
        "secondary_relationship",
        "secondary_language_spoken",
        "secondary_language_written",
        "secondary_home_phone",
        "secondary_cell_phone",
        "secondary_email",
    ]


# ----------------------------
# Extraction logic
# ----------------------------
#
# IMPORTANT:
# The selectors below are intentionally generic examples.
# You will need to replace them with selectors that match your local target site.
# Keeping them generic makes the repo GitHub-safe.
# ----------------------------

SEARCH_FIELD_ID = "recordID"
SEARCH_BUTTON_ID = "btnSearch"
RESULT_ROW_SELECTOR = "#results > tbody > tr > td:nth-child(5)"
CONTACT_SECTION_SELECTOR = "#main > div > div.section-contacts > div"

PRIMARY_STANDARD_XPATHS = {
    "name": '//*[@id="main"]/div/div/div[1]/h2',
    "relationship": '//*[@id="main"]/div/div/div[1]/div/div[1]',
    "language_spoken": '//*[@id="main"]/div/div/div[1]/div/div[6]',
    "language_written": '//*[@id="main"]/div/div/div[1]/div/div[7]',
    "home_phone": '//*[@id="main"]/div/div/div[1]/div/div[8]',
    "cell_phone": '//*[@id="main"]/div/div/div[1]/div/div[9]',
    "email": '//*[@id="main"]/div/div/div[1]/div/div[11]',
}

PRIMARY_ALTERNATE_XPATHS = {
    "name": '//*[@id="main"]/div/div/div/h2',
    "relationship": None,
    "language_spoken": '//*[@id="main"]/div/div/div/div/div[5]',
    "language_written": '//*[@id="main"]/div/div/div/div/div[6]',
    "home_phone": '//*[@id="main"]/div/div/div/div/div[7]',
    "cell_phone": '//*[@id="main"]/div/div/div/div/div[8]',
    "email": '//*[@id="main"]/div/div/div/div/div[10]',
}

SECONDARY_XPATHS = {
    "name": '//*[@id="main"]/div/div/div[2]/h2',
    "relationship": '//*[@id="main"]/div/div/div[2]/div/div[1]',
    "language_spoken": '//*[@id="main"]/div/div/div[2]/div/div[6]',
    "language_written": '//*[@id="main"]/div/div/div[2]/div/div[7]',
    "home_phone": '//*[@id="main"]/div/div/div[2]/div/div[8]',
    "cell_phone": '//*[@id="main"]/div/div/div[2]/div/div[9]',
    "email": '//*[@id="main"]/div/div/div[2]/div/div[11]/a',
}


def extract_contact_from_xpaths(driver: WebDriver, paths: Dict[str, str]) -> ContactRecord:
    return ContactRecord(
        name=safe_wait_text(driver, By.XPATH, paths["name"]) if paths.get("name") else "N/A",
        relationship=safe_wait_text(driver, By.XPATH, paths["relationship"]) if paths.get("relationship") else "N/A",
        language_spoken=safe_wait_text(driver, By.XPATH, paths["language_spoken"]) if paths.get("language_spoken") else "N/A",
        language_written=safe_wait_text(driver, By.XPATH, paths["language_written"]) if paths.get("language_written") else "N/A",
        home_phone=safe_find_text(driver, By.XPATH, paths["home_phone"]) if paths.get("home_phone") else "N/A",
        cell_phone=safe_find_text(driver, By.XPATH, paths["cell_phone"]) if paths.get("cell_phone") else "N/A",
        email=safe_find_text(driver, By.XPATH, paths["email"]) if paths.get("email") else "N/A",
    )


def search_record(driver: WebDriver, record_id: str) -> None:
    search_field = wait_for_clickable(driver, By.ID, SEARCH_FIELD_ID)
    search_field.click()

    # Select-all works on Mac and often on Windows Chrome as well.
    search_field.send_keys(Keys.COMMAND, "a")
    search_field.send_keys(Keys.BACK_SPACE)
    search_field.send_keys(record_id)

    search_button = driver.find_element(By.ID, SEARCH_BUTTON_ID)
    search_button.click()

    time.sleep(2)

    result_row = wait_for_clickable(driver, By.CSS_SELECTOR, RESULT_ROW_SELECTOR)
    result_row.click()


def open_contacts_section(driver: WebDriver) -> None:
    contacts_section = wait_for_present(driver, By.CSS_SELECTOR, CONTACT_SECTION_SELECTOR)
    contacts_section.click()


def extract_contacts(driver: WebDriver) -> List[ContactRecord]:
    try:
        open_contacts_section(driver)
    except Exception:
        input("Fix the page state manually if needed, then press Enter to continue...")
        open_contacts_section(driver)

    try:
        primary = extract_contact_from_xpaths(driver, PRIMARY_STANDARD_XPATHS)
        if primary.email == "N/A":
            primary = extract_contact_from_xpaths(driver, PRIMARY_ALTERNATE_XPATHS)
    except Exception:
        primary = extract_contact_from_xpaths(driver, PRIMARY_ALTERNATE_XPATHS)

    secondary = extract_contact_from_xpaths(driver, SECONDARY_XPATHS)
    return [primary, secondary]


def navigate_back_to_search(driver: WebDriver) -> None:
    driver.back()
    driver.implicitly_wait(2)
    driver.back()
    driver.implicitly_wait(2)


# ----------------------------
# Main workflow
# ----------------------------

def main() -> None:
    if not os.path.exists(INPUT_CSV):
        print(f"Input file not found: {INPUT_CSV}")
        print("Create the CSV file or set INPUT_CSV to the correct path.")
        sys.exit(1)

    if CHROMEDRIVER_PATH == "/path/to/chromedriver":
        print("Set CHROMEDRIVER_PATH before running this script.")
        print("Example:")
        print('  export CHROMEDRIVER_PATH="/Users/yourname/path/to/chromedriver"')
        sys.exit(1)

    driver = build_driver()

    try:
        driver.get(TARGET_URL)
        authenticate(driver)

        record_ids = get_input_ids(INPUT_CSV)
        fieldnames = get_output_fieldnames()

        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for record_id in record_ids:
                try:
                    search_record(driver, record_id)
                    contacts = extract_contacts(driver)
                    writer.writerow(flatten_contacts(record_id, contacts))
                    navigate_back_to_search(driver)
                    print(f"Processed record {record_id}")
                except Exception as exc:
                    print(f"Error processing record {record_id}: {exc}")
                    writer.writerow(flatten_contacts(record_id, []))
                    try:
                        navigate_back_to_search(driver)
                    except Exception:
                        pass

        print(f"\nDone. Output written to: {OUTPUT_CSV}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
