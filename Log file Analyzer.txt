import re
from collections import Counter, defaultdict

# Define the regular expression for Common Log Format (CLF)
LOG_PATTERN = re.compile(r'(\S+) - - \[(.*?)\] "(GET|POST|HEAD|PUT|DELETE|OPTIONS) (\S+) HTTP/\d\.\d" (\d{3}) (\d+)')

def parse_log_line(line):
    """Parse a log line and return the parsed components."""
    match = LOG_PATTERN.match(line)
    if match:
        ip, _, method, url, status, _ = match.groups()
        return {
            "ip": ip,
            "method": method,
            "url": url,
            "status": int(status)
        }
    return None

def analyze_logs(log_file_path):
    """Analyze the log file and return a summary."""
    # Counters to store analysis data
    ip_counter = Counter()
    page_counter = Counter()
    error_404_count = 0

    # Read the log file
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            log_data = parse_log_line(line)
            if log_data:
                ip_counter[log_data["ip"]] += 1
                page_counter[log_data["url"]] += 1
                if log_data["status"] == 404:
                    error_404_count += 1

    # Generate the report
    report = {
        "total_requests": sum(ip_counter.values()),
        "top_10_requested_pages": page_counter.most_common(10),
        "top_10_ip_addresses": ip_counter.most_common(10),
        "total_404_errors": error_404_count
    }
    return report

def print_report(report):
    """Print the summarized report in a readable format."""
    print("=== Web Server Log Analysis Report ===")
    print(f"Total Requests: {report['total_requests']}")
    print(f"Total 404 Errors: {report['total_404_errors']}\n")
    
    print("Top 10 Requested Pages:")
    for url, count in report["top_10_requested_pages"]:
        print(f"  {url}: {count} requests")
    
    print("\nTop 10 IP Addresses with Most Requests:")
    for ip, count in report["top_10_ip_addresses"]:
        print(f"  {ip}: {count} requests")

# Example usage
if __name__ == "__main__":
    log_file_path = "access.log"  # Path to your web server log file
    report = analyze_logs(log_file_path)
    print_report(report)

