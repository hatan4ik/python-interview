import subprocess
import shlex
import os

# ==========================================
# SCENARIO:
# You need to check disk usage on a server and alert if it's above a threshold.
# This requires running a shell command (`df -h`) and parsing the output.
# ==========================================

def check_disk_usage(threshold_percent=80):
    print("--- Checking Disk Usage ---")
    
    # 1. THE COMMAND
    # We want to run: df -h /
    # ALWAYS use shlex.split() or a list of strings for security (avoids shell injection)
    command = ["df", "-h", "/"]
    
    try:
        # 2. SUBPROCESS.RUN
        # capture_output=True: Grabs stdout/stderr so we can read it
        # text=True: Returns output as a string instead of bytes (Python 3.7+)
        # check=True: Raises CalledProcessError if the command fails (non-zero exit code)
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Output looks like:
        # Filesystem      Size  Used Avail Use% Mounted on
        # /dev/disk1s1s1  494G   10G  300G   3% /
        
        output_lines = result.stdout.strip().split('\n')
        
        # Parse the second line (the actual data)
        # Note: 'df' output format can vary by OS, but this is a standard interview pattern
        data_line = output_lines[1] 
        parts = data_line.split()
        
        # The percentage is usually the 5th element (index 4), e.g., "3%"
        use_percent_str = parts[4].replace('%', '')
        use_percent = int(use_percent_str)
        
        print(f"Current Disk Usage: {use_percent}%")
        
        if use_percent > threshold_percent:
            print(f"ALERT: Disk usage is critical! (> {threshold_percent}%)")
        else:
            print("Disk usage is within normal limits.")
            
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}")
        print(f"Error output: {e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# ==========================================
# BONUS: Walking a directory tree (os.walk)
# Common question: "Find all large files in a directory"
# ==========================================
def find_large_files(start_path, size_mb=100):
    print(f"\n--- Scanning for files larger than {size_mb}MB in {start_path} ---")
    
    limit_bytes = size_mb * 1024 * 1024
    
    # os.walk yields a 3-tuple: (current_directory, sub_directories, files)
    for root, dirs, files in os.walk(start_path):
        for name in files:
            filepath = os.path.join(root, name)
            try:
                # os.path.getsize returns size in bytes
                size = os.path.getsize(filepath)
                if size > limit_bytes:
                    print(f"Large file found: {filepath} ({size / (1024*1024):.2f} MB)")
            except OSError:
                # Permission errors, etc.
                pass

if __name__ == "__main__":
    check_disk_usage(threshold_percent=2) # Set low to trigger alert for demo
    
    # Using current directory for safety
    find_large_files(".") 
