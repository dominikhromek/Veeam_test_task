import os
import shutil
import time
import argparse
from datetime import datetime

# Log file handler class to manage logging operations
class LogFileHandler:
    def __init__(self, log_path):
        self.log_path = log_path

    def write_log(self, message):
        with open(self.log_path, 'a') as log_file:
            log_file.write(message)

# Folder synchronizer class for handling synchronization tasks
class FolderSynchronizer:
    def __init__(self, source_path, replica_path, log_handler):
        self.source_path = source_path
        self.replica_path = replica_path
        self.log_handler = log_handler

    def synchronize_folders(self):
        # Check if the source folder exists
        if not os.path.exists(self.source_path):
            print(f"Source folder '{self.source_path}' does not exist.")
            return

        # Create the replica folder if it doesn't exist
        os.makedirs(self.replica_path, exist_ok=True)

        # Log synchronization start time
        self.log_handler.write_log(f"\n\nSynchronization Log - {datetime.now()}\n")

        # Walk through the source folder's directory structure
        for root, dirs, files in os.walk(self.source_path):
            # Create corresponding directories in the replica folder
            replica_dir_path = os.path.join(self.replica_path, os.path.relpath(root, self.source_path))
            os.makedirs(replica_dir_path, exist_ok=True)

            # Copy/update files and log the operation
            for file in files:
                source_file_path = os.path.join(root, file)
                replica_file_path = os.path.join(self.replica_path, os.path.relpath(source_file_path, self.source_path))

                shutil.copy2(source_file_path, replica_file_path)
                shutil.copystat(source_file_path, replica_file_path)

                self.log_handler.write_log(f"Copied/Updated: {source_file_path} to {replica_file_path}\n")

                # Compare and log the sizes of corresponding files
                if os.path.exists(replica_file_path):
                    source_size = os.path.getsize(source_file_path)
                    replica_size = os.path.getsize(replica_file_path)

                    self.log_handler.write_log(f"Size: {source_file_path} ({source_size} bytes) and {replica_file_path} ({replica_size} bytes)\n")

# Main function for script execution
def main():
    parser = argparse.ArgumentParser(description="Folder Synchronization")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("log", help="Path to the log file")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")

    args = parser.parse_args()

    # Initialize log handler and folder synchronizer
    log_handler = LogFileHandler(args.log)
    synchronizer = FolderSynchronizer(args.source, args.replica, log_handler)

    # Main synchronization loop
    while True:
        synchronizer.synchronize_folders()
        print("Synchronization completed. Sleeping...")
        time.sleep(args.interval)

# Execute the script if it's the main module
if __name__ == "__main__":
    main()
