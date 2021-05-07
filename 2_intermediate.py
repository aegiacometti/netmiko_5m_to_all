# This example show how to execute a command in ALL the inventory
# The list of devices and credentials is specified in an external yaml file,
# imported and looped.
# It will also print how long it took to execute the command

# Change import settings
import yaml
import sys
import time
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException


# Reusable send command function
def send_command(dev: dict, cmd: str) -> str:
    """
    Send command to device using Netmiko
    :param dev: device info
    :param cmd: command to execute
    :return: Command output from device
    """
    try:
        # remove key hostname from dictionary since it is not expected/valid for netmiko
        del dev['hostname']
        # Use context manager to open and close the SSH session
        with ConnectHandler(**dev) as ssh:
            ssh.enable()
            output = ssh.send_command(cmd)
        return output.strip()
    except NetmikoTimeoutException:
        return 'Connection timed out'
    except NetmikoAuthenticationException:
        return 'Authentication failed'


if __name__ == "__main__":
    # get parameters from CLI
    # command = ' '.join(sys.argv[2:])
    command = input('\nCommand to run: ')

    # Load devices from file
    with open('inventory.yml') as f:
        inventory = yaml.safe_load(f.read())

    # get the common variables for all devices
    credentials = inventory['common_vars']
    # Start timer variable
    execution_start_timer = time.perf_counter()
    devices_counter = 0

    print(f'\nExecuting command: {command}\n')
    # Loop to repeat the command in all the inventory
    for device in inventory['hosts']:
        devices_counter += 1
        hostname = device['hostname']
        # update the device dictionary with the credentials and send command
        device.update(credentials)
        print('*** host: {} - ip: {}'.format(hostname, device['host']))
        # send command and store results
        result = send_command(device, command)
        # show result
        print(f'{result}\n')

    # Get and print finishing time
    elapsed_time = time.perf_counter() - execution_start_timer
    print(f"\n\"{command}\" executed in {devices_counter} devices in {elapsed_time:0.2f} seconds.\n")
