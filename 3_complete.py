# This example show how to execute a command in several devices devices
# The list of devices and credentials is specified in an external yaml file
# Then with a filter we select which one are we interesting in.
# The filter is by partial or full name or IP, or 'all'
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
        return output
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        return error


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
    device_filter = input('Specify device filter: ')
    command = input('Command to run: ')

    # Load devices from file with the filter
    inventory = get_devices(device_filter)

    # get the common variables for all devices
    credentials = inventory['common_vars']
    # Start timer variable
    execution_start_timer = time.perf_counter()
    devices_counter = 0

    print(f'Executing command: {command}\n')
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
