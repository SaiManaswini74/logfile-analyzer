import os
import sys
import subprocess
import boto3
from datetime import datetime

def backup_to_remote(server_user, server_address, source_dir, remote_dir):
    """Backup a directory to a remote server using rsync over SSH."""
    try:
        print(f"Starting backup to remote server: {server_address}")
        # Build the rsync command
        command = [
            "rsync", "-avz", "--delete",
            source_dir,
            f"{server_user}@{server_address}:{remote_dir}"
        ]
        # Run the rsync command
        subprocess.run(command, check=True)
        print("Backup to remote server completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Backup to remote server failed: {e}")
        return False

def backup_to_s3(bucket_name, source_dir):
    """Backup a directory to an AWS S3 bucket."""
    s3 = boto3.client("s3")
    success = True
    print(f"Starting backup to S3 bucket: {bucket_name}")
    
    # Walk through the source directory
    for root, _, files in os.walk(source_dir):
        for file_name in files:
            local_path = os.path.join(root, file_name)
            # Construct the S3 object path
            relative_path = os.path.relpath(local_path, source_dir)
            s3_path = f"{datetime.now().strftime('%Y-%m-%d')}/{relative_path}"
            try:
                # Upload file to S3
                s3.upload_file(local_path, bucket_name, s3_path)
                print(f"Uploaded {local_path} to s3://{bucket_name}/{s3_path}")
            except Exception as e:
                print(f"Failed to upload {local_path}: {e}")
                success = False
    return success

def main():
    # Configuration
    backup_type = "remote"  # "remote" for server backup or "s3" for S3 backup
    source_dir = "/path/to/source/directory"
    
    # Remote server configuration
    server_user = "your_username"
    server_address = "your_server_address"
    remote_dir = "/path/to/remote/directory"
    
    # AWS S3 configuration
    bucket_name = "your-s3-bucket-name"

    # Perform backup based on backup type
    if backup_type == "remote":
        success = backup_to_remote(server_user, server_address, source_dir, remote_dir)
    elif backup_type == "s3":
        success = backup_to_s3(bucket_name, source_dir)
    else:
        print("Invalid backup type specified.")
        sys.exit(1)
    
    # Generate report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if success:
        print(f"\nBackup completed successfully at {timestamp}.")
    else:
        print(f"\nBackup failed at {timestamp}.")

if __name__ == "__main__":
    main()
