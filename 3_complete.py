# This example show how to execute a command in several devices devices.
# The list of devices and credentials is specified in an external yaml file.
# Then with an input string filter we select which one are we interesting in.
# This filter can be by partial or full, name or IP, or 'all'
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
    hostname = dev['hostname']
    # remove key hostname from dictionary since it is not expected/valid for netmiko
    del dev['hostname']
    try:
        # Use context manager to open and close the SSH session
        with ConnectHandler(**dev) as ssh:
            ssh.enable()
            output = ssh.send_command(cmd)
        output = output.strip()
    except NetmikoTimeoutException:
        output = 'Connection timed out'
    except NetmikoAuthenticationException:
        output = 'Authentication failed'

    # re add key for future use
    dev['hostname'] = hostname

    return output


def get_devices(device_filter: str) -> dict:
    """
    Get match devices from inventory bases on name or IP
    :param device_filter: string to look for
    :return: matching inventory
    """
    with open('inventory.yml') as f:
        inventory = yaml.safe_load(f.read())
    matched_devices = []
    if device_filter != 'all':
        for device in inventory['hosts']:
            if device_filter in device['hostname'] or device_filter in device['host']:
                matched_devices.append(device)
        inventory['hosts'] = matched_devices

    return inventory


if __name__ == "__main__":
    # get parameters from CLI. Choose the following 2 lines OR the next 2
    # device_filter = sys.argv[1]
    # command = ' '.join(sys.argv[2:])
    device_filter = input('\nSpecify device filter: ')
    command = input('\nCommand to run: ')

    # Load devices from file with the filter
    inventory = get_devices(device_filter)

    # get the common variables for all devices
    credentials = inventory['common_vars']

    devices_counter = len(inventory['hosts'])

    print(f'\nExecuting command: {command}\n')

    # Start timer variable
    execution_start_timer = time.perf_counter()

    # Loop to repeat the command in all the inventory
    for device in inventory['hosts']:
        # update the device dictionary with the credentials and send command
        device.update(credentials)
        print('*** host: {} - ip: {}'.format(device['hostname'], device['host']))
        # send command and store results
        result = send_command(device, command)
        # show result
        print(f'{result}\n')

    # Get and print finishing time
    elapsed_time = time.perf_counter() - execution_start_timer
    print(f"\n\"{command}\" executed in {devices_counter} devices in {elapsed_time:0.2f} seconds.\n")
