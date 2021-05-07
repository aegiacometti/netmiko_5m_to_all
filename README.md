This is the most basic HOWTO / use of netmiko for beginners.

Throw commands from 0 to the whole inventory in 5 minutes.

Install dependencies with `pip3 install -r requirements.txt`

* **1_basic.py:** the minimal expression. Modify device info in the script to suit your devices.
* **2_intermediate.py:** Add an inventory.yml to run the command in all devices.
* **3_complete.py:** Add a filter string to filter devices before running the command.
* **4_bonus.py:** Add a show of matching devices, confirm, and stay in loop to issue several commands on the same matched devices.


In the next lab I will update the scripts to use diffent concurrency methods:
* multiprocessing
* sync multithreading
* async multithreding

Find it at: https://github.com/aegiacometti/netmiko_full_speed