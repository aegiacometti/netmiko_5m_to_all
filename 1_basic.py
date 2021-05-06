# This example shows the most basic command execution in 1 device

import netmiko
import sys

# device dictionary expected by netmiko library
device_info = {
    "device_type": "cisco_ios",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}

# get host IP and command to execute from CLI
# host = sys.argv[1]
# command = ' '.join(sys.argv[2:])
host = input('Enter host IP: ')
command = input('Enter command to run: ')
# add the IP address of the host to the dictonary
device_info['host'] = host

# Start SSH session and login to device
ssh_session = netmiko.ConnectHandler(**device_info)

# Enter enable mode
ssh_session.enable()

# Send command to device and store it in a variable
result = ssh_session.send_command(command)

# End SSH session
ssh_session.disconnect()

# Show results of the command
print(result)
