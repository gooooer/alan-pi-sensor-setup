ALAN Pi Environment Monitor
===========================

Description
-----------
This project is part of research conducted by [Dr. James Miksanek](https://orcid.org/0000-0001-5989-7527) at Louisiana State University at Alexandria (LSUA),
studying the effects of Artificial Light at Night (ALAN) and climate conditions on insect ecology.

The Raspberry Pi in this setup collects environmental data such as temperature, humidity, CO₂ concentration, and
spectral light information from Adafruit sensors. The data will later be used to correlate light and environmental
conditions with insect colony activity.

Repository Contents
-------------------
- Python script that reads Adafruit sensors
- requirements.txt listing all necessary Python packages
- sensor.service file for running the script automatically as a systemd service

Hardware Connection Setup
-------------------------
[TODO: Describe sensor wiring and pin connections here]

For now, ensure that all I²C-based sensors (e.g., AS7341, SCD4x, TSL2591) are properly connected to the Raspberry Pi’s
SCL and SDA pins, and that power (3.3V / 5V) and GND lines are secure.

Operating System Setup
----------------------
The following steps prepare the Raspberry Pi to run the monitoring script.

1. Flash Raspberry Pi OS (Lite is sufficient) to an SD card.
   You can use [Raspberry Pi Imager](https://www.raspberrypi.com/software/) or [Balena Etcher](https://etcher.balena.io/).

2. Enable SSH access before first boot:
   After flashing, open the boot partition on your computer and create an empty file named:
   ssh

   (This allows you to connect via SSH once the Pi starts.)

3. Boot the Raspberry Pi and log in.
   Default credentials for Raspberry Pi OS:  
   ```Username: pi```  
   ```Password: raspberry```

4. Update the system packages:  
```
sudo apt update
sudo apt upgrade -y
```

5. Enable the I²C interface:  
- Go to Interface Options → I2C → Enable  
- Finish and reboot:  
```
sudo reboot
```

6. Verify that I²C is enabled and working:  
```  
sudo apt install -y i2c-tools  
sudo i2cdetect -y 1  
```  
   (You should see addresses of connected sensors such as 0x29, 0x62, 0x3C, etc.)

7. Install Python tools:  
```
sudo apt install -y python3 python3-venv python3-pip
```

8. Clone this repository:  
```
cd ~  
git clone alan-pi-sensor-setup  
cd alan-pi-sensor-setup  
```

9. Create a virtual environment:  
```
python3 -m venv .venv  
source .venv/bin/activate  
python -m pip install –upgrade pip  
```

10. Install project dependencies:  
```
pip install -r requirements.txt
```

Testing the Script
------------------
Run the monitoring script manually to confirm it works:
```
source .venv/bin/activate
python main.py
```

If the script runs successfully and displays sensor readings, your setup is complete.
