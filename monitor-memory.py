import csv
import re
import time
import subprocess
from datetime import datetime

def get_ps_mem_output():
    try:
        # Run the ps_mem.py script and capture the output
        result = subprocess.run(
            ['sudo', 'python3', '/home/ubuntu/.local/lib/python3.8/site-packages/ps_mem.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running ps_mem.py: {e}")
        return ""

def parse_ps_mem_output(output):
    lines = output.strip().split('\n')
    data = []
    pattern = re.compile(r'\s*(\d+\.\d+ [KM]iB)\s*\+\s*(\d+\.\d+ [KM]iB)\s*=\s*(\d+\.\d+ [KM]iB)\s+(.+)')
    for line in lines:
        match = pattern.match(line)
        if match:
            private = match.group(1)
            shared = match.group(2)
            total = match.group(3)
            program_info = match.group(4).strip()

            # Extract the number of processes if present
            program_name = program_info
            num_processes = 1
            proc_match = re.match(r'(.+?)\s*\((\d+)\)$', program_info)
            if proc_match:
                program_name = proc_match.group(1).strip()
                num_processes = int(proc_match.group(2))

            data.append((private, shared, total, program_name, num_processes))
        else:
            print(f"Line didn't match pattern: {line}")
    return data

def convert_to_megabytes(size_str):
    value, unit = size_str.split()
    value = float(value)
    if unit == 'KiB':
        value /= 1024
    return value

def write_to_csv(filename, data):
    try:
        with open(filename, 'a', newline='') as csvfile:
            fieldnames = ['timestamp', 'private (MiB)', 'shared (MiB)', 'total (MiB)', 'program', 'num_processes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            for entry in data:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                private = convert_to_megabytes(entry[0])
                shared = convert_to_megabytes(entry[1])
                total = convert_to_megabytes(entry[2])
                program = entry[3]
                num_processes = entry[4]
                writer.writerow({'timestamp': timestamp, 'private (MiB)': private, 'shared (MiB)': shared, 'total (MiB)': total, 'program': program, 'num_processes': num_processes})
    except Exception as e:
        print(f"Error writing to CSV: {e}")

def main():
    output = get_ps_mem_output()
    if output:
        data = parse_ps_mem_output(output)
        write_to_csv('./ps_mem.csv', data)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(1)