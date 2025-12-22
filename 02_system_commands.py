import subprocess
from pathlib import Path

# ==========================================
# SCENARIO:
# System commands and file traversal using 'pathlib'.
# 'pathlib' is the Object-Oriented replacement for os.path and os.walk.
# ==========================================

def check_disk_usage(mount_point: str = "/", threshold_percent: int = 80) -> None:
    print("--- Checking Disk Usage ---")
    
    command = ["df", "-h", mount_point]
    
    try:
        # Modern subprocess.run usage
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        output_lines = result.stdout.strip().split('\n')
        data_line = output_lines[1] 
        parts = data_line.split()
        
        use_percent_str = parts[4].replace('%', '')
        use_percent = int(use_percent_str)
        
        print(f"Current Disk Usage: {use_percent}%")
        
        if use_percent > threshold_percent:
            print(f"ALERT: Disk usage is critical! (> {threshold_percent}%)")
        else:
            print("Disk usage is within normal limits.")
            
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# ==========================================
# OPTIMIZATION: pathlb.Path.rglob()
# Faster and more readable than os.walk for simple finding tasks.
# ==========================================
def find_large_files(start_path: Path, size_mb: int = 100) -> None:
    print(f"\n--- Scanning for files larger than {size_mb}MB in {start_path} ---")
    
    limit_bytes = size_mb * 1024 * 1024
    
    # .rglob('*') recursively matches all files
    # Generator expression allows memory-efficient iteration
    try:
        for file_path in start_path.rglob('*'):
            if file_path.is_file():
                try:
                    # stat().st_size is the modern way to get size
                    size = file_path.stat().st_size
                    if size > limit_bytes:
                        size_in_mb = size / (1024 * 1024)
                        print(f"Large file found: {file_path} ({size_in_mb:.2f} MB)")
                except OSError:
                    # Skip permission errors
                    continue
    except Exception as e:
        print(f"Error scanning directory: {e}")

if __name__ == "__main__":
    check_disk_usage(threshold_percent=2)
    
    # Pass a Path object, not a string
    find_large_files(Path("."))