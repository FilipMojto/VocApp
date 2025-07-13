import schedule
import time

if __name__ == "__main__":
    # Example usage

    schedule.every().day.at("08:00").do(send_revision_emails)