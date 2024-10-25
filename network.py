import psutil
import argparse
import getpass
import subprocess
import platform
import time
import concurrent.futures

def authenticate():
    """Simple authentication for the CLI."""
    password = getpass.getpass("Enter password to access network details: ")
    if password != "secure_password":  # Use a secure method for real applications
        print("Authentication failed!")
        exit(1)

def get_network_connections():
    """Fetch and return network connections details."""
    connections = psutil.net_connections(kind='inet')
    return [
        {
            'local_address': f"{conn.laddr.ip}:{conn.laddr.port}",
            'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
            'protocol': conn.type,
            'status': conn.status
        }
        for conn in connections
    ]

def display_connections(connections):
    """Format and display the network connections."""
    print(f"{'Local Address':<25} {'Remote Address':<25} {'Protocol':<10} {'Status':<15}")
    print("-" * 75)
    for conn in connections:
        print(f"{conn['local_address']:<25} {conn['remote_address']:<25} {conn['protocol']:<10} {conn['status']:<15}")

def list_available_networks():
    """List available Wi-Fi networks."""
    print("Available Wi-Fi networks:")
    networks = []
    
    if platform.system() == "Windows":
        command = "netsh wlan show networks"
        output = subprocess.check_output(command, shell=True, text=True)
        for line in output.split('\n'):
            if "SSID" in line and "BSSID" not in line:
                ssid = line.split(":")[1].strip()
                networks.append(ssid)
                print(ssid)
    else:
        print("This functionality is currently supported only on Windows.")
        return []

    return networks

def connect_to_network(ssid, password):
    """Connect to a specified Wi-Fi network."""
    if platform.system() == "Windows":
        # Set the password for the SSID using netsh command (if not already saved)
        set_password_command = f'netsh wlan set hostednetwork mode=allow ssid="{ssid}" key="{password}"'
        subprocess.run(set_password_command, shell=True)

        command = f'netsh wlan connect name="{ssid}"'
        subprocess.run(command, shell=True)
        
        # Reduce the waiting time before checking connection status
        time.sleep(1)  # Wait for a second to allow the connection to establish

def check_connection(ssid):
    """Check if connected to the specified SSID."""
    connections = get_network_connections()
    return any(conn['remote_address'].startswith(ssid) for conn in connections)

def try_password(ssid, password):
    """Try to connect to a Wi-Fi network with the given password."""
    print(f"Trying password: {password}")
    connect_to_network(ssid, password)
    if check_connection(ssid):
        print(f"Successfully connected to {ssid} with password: {password}")
        return True
    else:
        print(f"Failed to connect with password: {password}")
        return False

def try_passwords(ssid, password_list):
    """Attempt to connect to a specified Wi-Fi network using a list of passwords concurrently."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_password = {executor.submit(try_password, ssid, password): password for password in password_list}
        
        for future in concurrent.futures.as_completed(future_to_password):
            password = future_to_password[future]
            try:
                if future.result():
                    # If a connection was successful, exit early
                    break
            except Exception as e:
                print(f"Error trying password {password}: {e}")

def main():
    """Main function to handle CLI operations."""
    authenticate()

    parser = argparse.ArgumentParser(description='Network Connection Details CLI')
    parser.add_argument('--list', action='store_true', help='List network connection details')
    parser.add_argument('--wifi', action='store_true', help='List available Wi-Fi networks')
    parser.add_argument('--try-passwords', nargs=2, metavar=('SSID', 'PASSWORD_FILE'), help='Try a list of passwords to connect to a Wi-Fi network')

    args = parser.parse_args()

    if args.list:
        connections = get_network_connections()
        display_connections(connections)
    elif args.wifi:
        list_available_networks()
    elif args.try_passwords:
        ssid = args.try_passwords[0]
        password_file = args.try_passwords[1]

        # Load passwords from the specified file
        try:
            with open(password_file, 'r') as f:
                passwords = [line.strip() for line in f if line.strip()]
            try_passwords(ssid, passwords)
        except FileNotFoundError:
            print(f"Password file '{password_file}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
