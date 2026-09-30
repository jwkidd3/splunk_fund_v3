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
    # Fixed seed keeps the dataset reproducible so lab answer keys stay valid
    # across regenerations. Only the date window shifts to "last N days".
    SEED = 20240101

    # The labs tell students to search with Splunk's "Last 30 days" preset. If the
    # data also spanned a full 30 days, that preset would start clipping the oldest
    # events the moment the clock ticked past generation time, and every count in
    # the answer keys would drift. Generating a shorter window leaves SLACK_DAYS of
    # headroom, so "Last 30 days" still captures 100% of the data - and the answer
    # keys stay exact - for several days after the data is generated.
    SEARCH_WINDOW_DAYS = 30
    SLACK_DAYS = 4
    DEFAULT_DAYS = SEARCH_WINDOW_DAYS - SLACK_DAYS   # 26

    def __init__(self, days=DEFAULT_DAYS, output_dir=".", seed=SEED):
        random.seed(seed)
        self.days = days
        self.output_dir = output_dir
        self.start_date = datetime.now() - timedelta(days=days)
        self.end_date = datetime.now()
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Data tracking for consistency
        self.product_ids = PRODUCT_IDS
        self.product_categories = self._load_product_categories()
        
    def _load_product_categories(self):
        """Map productId -> categoryId from the static products.csv lookup, so the
        categoryId written into the access log always agrees with the lookup table."""
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.csv")
        mapping = {}
        try:
            with open(path, newline="") as fh:
                for row in csv.DictReader(fh):
                    mapping[row["productId"]] = row["categoryId"]
        except OSError:
            pass
        for pid in PRODUCT_IDS:
            mapping.setdefault(pid, "STRATEGY")
        return mapping

    def generate_web_access_logs(self, count=131645):
        """Generate access logs as realistic per-session customer journeys.

        Every session belongs to a single client IP and walks a funnel:

            browse categories -> view products -> add to cart -> (maybe) purchase

        so product views outnumber cart additions, which outnumber purchases, and
        `dc(JSESSIONID) by clientip` yields a genuine ranking instead of a tie.
        """
        client_ips = [
            "92.46.53.223", "212.58.253.71", "91.214.92.22", "193.33.170.23",
            "87.194.216.51", "108.65.113.83", "109.103.32.135", "118.138.38.229",
            "116.159.208.78", "95.134.237.97", "192.168.1.100", "10.0.0.50"
        ]
        # Uneven so a handful of IPs are clearly the heaviest talkers
        ip_weights = [18, 15, 13, 11, 9, 8, 7, 6, 5, 4, 3, 1]

        referrers = [
            "http://www.buttercupgames.com", "http://www.google.com", "http://www.bing.com",
            "http://www.yahoo.com", "http://www.facebook.com", "-"
        ]
        ref_weights = [30, 25, 12, 12, 13, 8]

        user_agents = [
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.28) Gecko/20120306 YFF3 Firefox/3.6.28 ( .NET CLR 3.5.30729; .NET4.0C)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; InfoPath.1; .NET4.0C; .NET4.0E; MS-RTC LM 8)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]

        categories = sorted(set(self.product_categories.values()))
        window = max(1, self.days * 24 * 3600 - 3600)
        logs = []

        while len(logs) < count:
            ip = random.choices(client_ips, weights=ip_weights, k=1)[0]
            session_id = (f"SD{random.randint(1,9)}SL{random.randint(1,99)}"
                          f"FF{random.randint(1,99)}ADFF{random.randint(1000,9999)}")
            user_agent = random.choice(user_agents)
            referrer = random.choices(referrers, weights=ref_weights, k=1)[0]
            clock = self.start_date + timedelta(seconds=random.randint(0, window))

            journey = []

            # 1. Landing and category browsing
            for _ in range(random.randint(1, 3)):
                journey.append(("/category.screen",
                                [f"categoryId={random.choice(categories)}"], "POST"))

            # 2. Product views - the top of the funnel
            viewed = random.sample(self.product_ids, k=random.randint(1, 5))
            for pid in viewed:
                journey.append(("/product.screen", [f"productId={pid}"], "GET"))

            # 3. Page furniture and the occasional stale link
            journey.append(("/stuff/logo.ico", [], "GET"))
            if random.random() < 0.10:
                journey.append(("/oldlink", [], "GET"))

            # 4. Cart activity - only a minority of sessions add anything
            in_cart = []
            if random.random() < 0.35:
                in_cart = random.sample(viewed, k=min(len(viewed), random.randint(1, 3)))
                for pid in in_cart:
                    journey.append(("/cart.do",
                                    ["action=addtocart", f"productId={pid}"], "POST"))
                if random.random() < 0.40:
                    journey.append(("/cart.do", ["action=view"], "POST"))
                if len(in_cart) > 1 and random.random() < 0.25:
                    dropped = random.choice(in_cart)
                    in_cart.remove(dropped)
                    journey.append(("/cart.do",
                                    ["action=remove", f"productId={dropped}"], "POST"))

                # 5. Checkout - only a minority of carts convert
                if in_cart and random.random() < 0.30:
                    for pid in in_cart:
                        journey.append(("/success.do",
                                        ["action=purchase",
                                         f"categoryId={self.product_categories[pid]}",
                                         f"productId={pid}"], "POST"))

            for path, params, method in journey:
                clock = min(clock + timedelta(seconds=random.randint(3, 180)), self.end_date)
                url = path + "?" + "&".join(params + [f"JSESSIONID={session_id}"])

                if "/stuff/" in path:
                    status, bytes_sent = 404, random.randint(1000, 2000)
                elif random.random() < 0.95:
                    status, bytes_sent = 200, random.randint(200, 4000)
                else:
                    status = random.choice([403, 404, 500])
                    bytes_sent = random.randint(0, 1000)

                logs.append(
                    f'{ip} - - [{clock.strftime("%d/%b/%Y:%H:%M:%S")}] '
                    f'"{method} {url} HTTP 1.1" {status} {bytes_sent} '
                    f'"{referrer}" "{user_agent}" {random.randint(50, 1000)}'
                )
                if len(logs) >= count:
                    break

        # Real access logs arrive in time order
        logs.sort(key=lambda l: datetime.strptime(
            l.split("[", 1)[1].split("]", 1)[0], "%d/%b/%Y:%H:%M:%S"))

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
        # Real audit tables come back in time order
        logs.sort(key=lambda r: datetime.strptime(r["Time"], "%d/%b/%Y %H:%M:%S"))

        output_file = os.path.join(self.output_dir, "db_audit_30DAY.csv")
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ["Time", "Type", "Command", "Duration"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for log in logs:
                writer.writerow(log)
        
        print(f"Generated {len(logs)} database audit logs in {output_file}")
        return logs
    
    def generate_linux_security_logs(self, count=8000):
        """Generate Linux security logs with realistic SSH attack patterns"""

        # Common patterns from original data - expanded list
        failed_users = ["zabbix", "operator", "dba", "admin", "root", "oracle", "postgres",
                       "mysql", "backup", "test", "git", "jenkins", "ubuntu", "user", "guest"]
        valid_users = ["nsharpe", "djohnson", "admin", "root", "user1", "analyst", "sysadmin"]

        # Source IPs - mix of suspicious and legitimate
        suspicious_ips = ["208.65.153.253", "202.179.8.245", "94.102.49.190", "185.234.218.110",
                         "103.99.0.122", "198.51.100.42", "45.33.32.156", "167.71.5.83"]
        legitimate_ips = ["192.168.1.100", "10.0.0.50", "172.16.0.10", "192.168.1.50"]

        log_patterns = [
            {"type": "failed_password", "weight": 0.45},  # More failed attempts for realism
            {"type": "successful_login", "weight": 0.25},
            {"type": "session_opened", "weight": 0.12},
            {"type": "session_closed", "weight": 0.10},
            {"type": "invalid_user", "weight": 0.05},     # New: explicitly invalid user attempts
            {"type": "server_events", "weight": 0.03}
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
                # 75% of failed attempts are on port 22 (realistic SSH brute force)
                # 25% are on random high ports (port scanning attempts)
                if random.random() < 0.75:
                    port = 22
                else:
                    port = random.randint(2222, 65535)

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

            elif selected_pattern == "invalid_user":
                # Explicit invalid user attempts (common in brute force attacks)
                user = random.choice(failed_users + ["admin123", "administrator", "test123", "default"])
                ip = random.choice(suspicious_ips)
                port = 22  # Always port 22 for these

                log_line = (f'{timestamp.strftime("%a %b %d %Y %H:%M:%S")} www1 '
                           f'sshd[{pid}]: Invalid user {user} from {ip} port {port}')

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
        # Real syslog arrives in time order
        logs.sort(key=lambda l: datetime.strptime(" ".join(l.split(" ")[1:5]),
                                                  "%b %d %Y %H:%M:%S"))

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
        default=DataGenerator.DEFAULT_DAYS,
        help=(f'Days of data to generate (default: {DataGenerator.DEFAULT_DAYS}). '
              f'Kept below the {DataGenerator.SEARCH_WINDOW_DAYS}-day search preset '
              f'the labs use so answer keys stay exact for '
              f'{DataGenerator.SLACK_DAYS} days after generation.')
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='.',
        help='Output directory for generated files (default: current directory)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        default=DataGenerator.SEED,
        help=f'Random seed for reproducible data (default: {DataGenerator.SEED})'
    )

    args = parser.parse_args()
    
    # Create data generator and generate all data
    generator = DataGenerator(days=args.days, output_dir=args.output_dir, seed=args.seed)
    generator.generate_all_data()

if __name__ == "__main__":
    main()