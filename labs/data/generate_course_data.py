#!/usr/bin/env python3
"""
Comprehensive Data Generator for Splunk Fundamentals Course
Generates all data types needed across all labs based on the original sample data files

This script generates:
- Web application access logs (access_combined_wcookie)
- Database audit logs (db_audit) 
- Linux security logs (linux_secure)
- Splunk audit logs (_audit)
- Product lookup data (CSV)
- Customer category lookups (CSV)

Usage: python generate_course_data.py [--days N] [--output-dir DIR]
"""

import random
import json
import csv
import argparse
from datetime import datetime, timedelta
import sys
import os

# Product IDs from the static products.csv file
PRODUCT_IDS = [
    "DB-SG-G01", "DC-SG-G02", "FS-SG-G03", "WC-SH-G04", "WC-SH-T02",
    "PZ-SG-G05", "CU-PG-G06", "MB-AG-G07", "MB-AG-T01", "FI-AG-G08",
    "BS-AG-G09", "SC-MG-G10", "WC-SH-A01", "WC-SH-A02", "GT-SC-G01", 
    "WSC-MG-G10"
]

class DataGenerator:
    def __init__(self, days=30, output_dir="."):
        self.days = days
        self.output_dir = output_dir
        self.start_date = datetime.now() - timedelta(days=days)
        self.end_date = datetime.now()
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Data tracking for consistency
        self.product_ids = PRODUCT_IDS
        self.session_ids = [f"SD{random.randint(1,9)}SL{random.randint(1,99)}FF{random.randint(1,99)}ADFF{random.randint(1000,9999)}" 
                           for _ in range(1000)]
        
    def generate_web_access_logs(self, count=50000):
        """Generate web application access logs in Apache combined log format"""
        
        # IP addresses based on original data
        client_ips = [
            "92.46.53.223", "212.58.253.71", "91.214.92.22", "193.33.170.23",
            "87.194.216.51", "108.65.113.83", "109.103.32.135", "118.138.38.229",
            "116.159.208.78", "95.134.237.97", "192.168.1.100", "10.0.0.50"
        ]
        
        # Referrers with realistic distribution
        referrers = [
            "http://www.buttercupgames.com", "http://www.google.com", "http://www.bing.com",
            "http://www.yahoo.com", "http://www.facebook.com", "-"
        ]
        
        # User agents from original data
        user_agents = [
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.28) Gecko/20120306 YFF3 Firefox/3.6.28 ( .NET CLR 3.5.30729; .NET4.0C)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; InfoPath.1; .NET4.0C; .NET4.0E; MS-RTC LM 8)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
        
        # URL patterns from original data
        url_patterns = [
            {"path": "/category.screen", "params": ["categoryId=STRATEGY", "categoryId=SHOOTER", "categoryId=ARCADE", "categoryId=TEE", "categoryId=SPORTS", "categoryId=SIMULATION", "categoryId=ACCESSORIES"]},
            {"path": "/product.screen", "params": [f"productId={pid}" for pid in self.product_ids]},
            {"path": "/cart.do", "params": ["action=addtocart", "action=remove", "action=view", "action=purchase"]},
            {"path": "/success.do", "params": ["action=purchase"]},
            {"path": "/cart/success.do", "params": []},
            {"path": "/oldlink", "params": []},
            {"path": "/stuff/logo.ico", "params": []}
        ]
        
        logs = []
        
        for i in range(count):
            timestamp = self.start_date + timedelta(
                seconds=random.randint(0, self.days * 24 * 3600)
            )
            
            ip = random.choice(client_ips)
            session_id = random.choice(self.session_ids)
            user_agent = random.choice(user_agents)
            referrer = random.choice(referrers)
            
            # Select URL pattern
            url_pattern = random.choice(url_patterns)
            path = url_pattern["path"]
            
            # Add parameters
            params = []
            if url_pattern["params"]:
                if path in ["/category.screen", "/product.screen"]:
                    params.append(random.choice(url_pattern["params"]))
                elif path == "/cart.do":
                    action = random.choice(["addtocart", "remove", "view"])
                    params.append(f"action={action}")
                    if action in ["addtocart", "remove"]:
                        params.append(f"productId={random.choice(self.product_ids)}")
                elif path == "/success.do":
                    params.append("action=purchase")
                    params.append(f"categoryId={random.choice(['STRATEGY', 'SHOOTER', 'ARCADE', 'TEE', 'SPORTS', 'SIMULATION', 'ACCESSORIES'])}")
                    params.append(f"productId={random.choice(self.product_ids)}")
                
            params.append(f"JSESSIONID={session_id}")
            url = path + ("?" + "&".join(params) if params else "")
            
            # HTTP method and version
            method = "POST" if path in ["/cart.do", "/success.do", "/category.screen"] else "GET"
            http_version = "HTTP 1.1"
            
            # Status code (mostly 200, some 404)
            if "/stuff/" in path:
                status = 404
                bytes_sent = random.randint(1000, 2000)
            else:
                status = 200 if random.random() < 0.95 else random.choice([403, 404, 500])
                bytes_sent = random.randint(200, 4000) if status == 200 else random.randint(0, 1000)
            
            # Response time (last number in original format)
            response_time = random.randint(50, 1000)
            
            # Format: IP - - [timestamp] "METHOD /path HTTP/1.1" status bytes "referrer" "user_agent" response_time
            log_line = (f'{ip} - - [{timestamp.strftime("%d/%b/%Y:%H:%M:%S")}] '
                       f'"{method} {url} {http_version}" {status} {bytes_sent} '
                       f'"{referrer}" "{user_agent}" {response_time}')
            
            logs.append(log_line)
        
        # Write to file
        output_file = os.path.join(self.output_dir, "access_30DAY.log")
        with open(output_file, 'w') as f:
            for log in logs:
                f.write(f"{log}\n")
        
        print(f"Generated {len(logs)} web access logs in {output_file}")
        return logs
    
    def generate_db_audit_logs(self, count=10000):
        """Generate database audit logs in CSV format"""
        
        # SQL commands from original data
        commands = [
            'UPDATE users SET email = {}@{}.{} WHERE userid = {}',
            'SELECT * FROM creditcard WHERE userid = {}',
            'INSERT INTO users (username, password, fname, lname, email) VALUES ({}, {}, {}, {}, {}@{}.{})',
            'SELECT ccexpire FROM creditcard WHERE userid = {}',
            'SELECT email FROM users WHERE userid = {}',
            'SELECT * FROM users WHERE userid = {}',
            'SELECT username FROM users WHERE userid = {}',
            'DELETE FROM sessions WHERE userid = {}',
            'UPDATE products SET stock = stock - 1 WHERE productid = {}',
            'INSERT INTO orders (userid, productid, quantity) VALUES ({}, {}, {})'
        ]
        
        connection_types = [
            'admin on BCG using TCP/IP',
            'dbuser on BCG using TCP/IP',
            'webapp on BCG using TCP/IP'
        ]
        
        # Generate names for realistic data
        first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "company.com", "example.org"]
        
        logs = []
        
        for i in range(count):
            timestamp = self.start_date + timedelta(
                seconds=random.randint(0, self.days * 24 * 3600)
            )
            
            # Choose between Query and Connect
            if random.random() < 0.8:  # 80% queries
                query_type = "Query"
                # Generate realistic SQL command
                command_template = random.choice(commands)
                
                if "UPDATE users SET email" in command_template:
                    email_user = random.choice(first_names).lower()
                    domain = random.choice(domains)
                    userid = random.randint(1000, 9999)
                    command = f'UPDATE users SET email = {email_user}@{domain} WHERE userid = {userid}'
                elif "INSERT INTO users" in command_template:
                    username = random.choice(first_names).lower() + str(random.randint(10, 99))
                    password_hash = "1e3f0e4291be8533bce600d32c41da4fecfd0204"  # Sample hash
                    fname = random.choice(first_names)
                    lname = random.choice(last_names)
                    email = f"{random.choice(first_names).lower()}{random.randint(10,99)}@{random.choice(domains)}"
                    command = f'INSERT INTO users (username, password, fname, lname, email) VALUES ({username}, {password_hash}, {fname}, {lname}, {email})'
                else:
                    # Simple substitution
                    userid = random.randint(1000, 9999)
                    productid = random.choice(self.product_ids)
                    quantity = random.randint(1, 5)
                    command = command_template.replace('{}', str(userid), 1)
                    command = command.replace('{}', str(productid), 1) 
                    command = command.replace('{}', str(quantity), 1)
                
                # Duration varies by query type
                if "SELECT" in command:
                    duration = random.randint(5, 50)
                elif "UPDATE" in command or "INSERT" in command:
                    duration = random.randint(10, 100)
                else:
                    duration = random.randint(5, 30)
                    
            else:  # 20% connections
                query_type = "Connect"
                command = random.choice(connection_types)
                duration = ""  # No duration for connections
            
            log = {
                "Time": timestamp.strftime("%d/%b/%Y %H:%M:%S"),
                "Type": query_type,
                "Command": command,
                "Duration": duration
            }
            logs.append(log)
        
        # Write to CSV file
        output_file = os.path.join(self.output_dir, "db_audit_30DAY.csv")
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ["Time", "Type", "Command", "Duration"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for log in logs:
                writer.writerow(log)
        
        print(f"Generated {len(logs)} database audit logs in {output_file}")
        return logs
    
    def generate_linux_security_logs(self, count=5000):
        """Generate Linux security logs"""
        
        # Common patterns from original data
        failed_users = ["zabbix", "operator", "dba", "admin", "root", "oracle", "postgres", "mysql"]
        valid_users = ["nsharpe", "djohnson", "admin", "root", "user1", "analyst"]
        
        # Source IPs - mix of suspicious and legitimate
        suspicious_ips = ["208.65.153.253", "202.179.8.245", "94.102.49.190", "185.234.218.110"]
        legitimate_ips = ["192.168.1.100", "10.0.0.50", "172.16.0.10"]
        
        log_patterns = [
            {"type": "failed_password", "weight": 0.40},
            {"type": "successful_login", "weight": 0.30},
            {"type": "session_opened", "weight": 0.15},
            {"type": "session_closed", "weight": 0.10},
            {"type": "server_events", "weight": 0.05}
        ]
        
        logs = []
        
        for i in range(count):
            timestamp = self.start_date + timedelta(
                seconds=random.randint(0, self.days * 24 * 3600)
            )
            
            # Select log pattern
            rand_val = random.random()
            cumulative = 0
            selected_pattern = "failed_password"
            
            for pattern in log_patterns:
                cumulative += pattern['weight']
                if rand_val < cumulative:
                    selected_pattern = pattern['type']
                    break
            
            pid = random.randint(1000, 99999)
            
            if selected_pattern == "failed_password":
                if random.random() < 0.7:  # 70% invalid users
                    user = random.choice(failed_users)
                    user_desc = f"invalid user {user}"
                else:
                    user = random.choice(valid_users)
                    user_desc = user
                
                ip = random.choice(suspicious_ips)
                port = random.randint(22, 65535)
                
                log_line = (f'{timestamp.strftime("%a %b %d %Y %H:%M:%S")} www1 '
                           f'sshd[{pid}]: Failed password for {user_desc} from {ip} port {port} ssh2')
                
            elif selected_pattern == "successful_login":
                user = random.choice(valid_users)
                ip = random.choice(legitimate_ips + suspicious_ips[:1])  # Mostly legitimate
                port = 22
                
                log_line = (f'{timestamp.strftime("%a %b %d %Y %H:%M:%S")} www1 '
                           f'sshd[{pid}]: Accepted password for {user} from {ip} port {port} ssh2')
                
            elif selected_pattern == "session_opened":
                user = random.choice(valid_users)
                uid = 0 if user in ["root", "admin"] else random.randint(1000, 9999)
                
                log_line = (f'{timestamp.strftime("%a %b %d %Y %H:%M:%S")} www1 '
                           f'sshd[{pid}]: pam_unix(sshd:session): session opened for user {user} by (uid={uid})')
                
            elif selected_pattern == "session_closed":
                user = random.choice(valid_users)
                
                log_line = (f'{timestamp.strftime("%a %b %d %Y %H:%M:%S")} www1 '
                           f'sshd[{pid}]: pam_unix(sshd:session): session closed for user {user}')
                
            else:  # server_events
                events = [
                    f'sshd[{pid}]: Server listening on :: port 22.',
                    f'sshd[{pid}]: Server listening on 0.0.0.0 port 22.',
                    f'sshd[{pid}]: Received SIGHUP; restarting.',
                ]
                event = random.choice(events)
                
                log_line = f'{timestamp.strftime("%a %b %d %Y %H:%M:%S")} www1 {event}'
            
            logs.append(log_line)
        
        # Write to file
        output_file = os.path.join(self.output_dir, "linux_s_30DAY.log")
        with open(output_file, 'w') as f:
            for log in logs:
                f.write(f"{log}\n")
        
        print(f"Generated {len(logs)} Linux security logs in {output_file}")
        return logs
    
    def generate_all_data(self):
        """Generate all data types for the course"""
        print(f"Generating {self.days} days of data for Splunk Fundamentals course...")
        print(f"Output directory: {self.output_dir}")
        print("=" * 60)
        
        # Generate main data files (matching original volumes)
        self.generate_web_access_logs(131645)
        self.generate_db_audit_logs(44097)  
        self.generate_linux_security_logs(63884)
        
        print("=" * 60)
        print("Data generation complete!")
        print()
        print("Generated files:")
        print("- access_30DAY.log (Web application access logs)")
        print("- db_audit_30DAY.csv (Database audit logs)")
        print("- linux_s_30DAY.log (Linux security logs)")
        print()
        print("Note: products.csv is a static file and does not need regeneration")
        print()
        print("Data loading instructions:")
        print("1. Copy files to your Splunk instance")
        print("2. Use Settings > Add Data > Upload")
        print("3. For access logs: Set sourcetype=access_combined_wcookie, index=main") 
        print("4. For db audit: Set sourcetype=db_audit, index=main")
        print("5. For linux logs: Set sourcetype=linux_secure, index=main")
        print("6. Upload products.csv via Settings > Lookups > Lookup table files")

def main():
    parser = argparse.ArgumentParser(
        description="Generate comprehensive data for Splunk Fundamentals course"
    )
    parser.add_argument(
        '--days', 
        type=int, 
        default=30,
        help='Number of days of data to generate (default: 30)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='.',
        help='Output directory for generated files (default: current directory)'
    )
    
    args = parser.parse_args()
    
    # Create data generator and generate all data
    generator = DataGenerator(days=args.days, output_dir=args.output_dir)
    generator.generate_all_data()

if __name__ == "__main__":
    main()