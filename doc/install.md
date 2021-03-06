Installation
============

Requirements
------------

  * Linux-compatible computer.
  
  * Bluetooth adapter with Bluetooth Low Energy support.
  
  * Debian-based Linux distro, such as Ubuntu or RaspberryPi OS. Debian 9 might work, 
  but Debian 10 or later is recommended.
  
Instructions
------------

  1. Download the latest package from the [releases page](https://github.com/teuvo486/ble2json-py/releases),
  **or** run the following command:
  
    curl --proto =https -L -O https://github.com/teuvo486/ble2json-py/releases/download/v0.2.3/ble2json_0.2.3-1_all.deb

  2. Change to the folder with the downloaded package and run 
  `sudo apt install ./ble2json_0.2.3-1_all.deb`. (If installing on x86, you should run the
  command with `--no-install-recommends` to prevent `apt` from complaining about a missing dependency.)

  3. Run `sudo python3 -m ble2json.scanner` and name the discovered devices, **or** write the 
  [config file](https://github.com/teuvo486/ble2json-py/blob/main/doc/config.md) manually. 
 
  4. Reboot your computer and the app should be running. If not, see
  [troubleshooting.](https://github.com/teuvo486/ble2json-py/blob/main/doc/troubleshooting.md)
