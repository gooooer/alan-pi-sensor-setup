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
Inventory used for single circuit is outlined below.

| HW Item | Count |
|------|-------|
| [Raspberry Pi Zero WH (Zero W with Headers)](https://www.adafruit.com/product/3708) | 1 |
| [SparkFun Qwiic or Stemma QT SHIM for Raspberry Pi / SBC](https://www.adafruit.com/product/4463) | 1 |
| [Adafruit PiOLED - 128x32 Monochrome OLED Add-on for Raspberry Pi](https://www.adafruit.com/product/3527) | 1 |
| [Adafruit TSL2591 High Dynamic Range Digital Light Sensor - STEMMA QT](https://www.adafruit.com/product/1980) | 1 |
| [Adafruit AS7341 10-Channel Light / Color Sensor Breakout - STEMMA QT / Qwiic](https://www.adafruit.com/product/4698) | 1 |
| [Adafruit SCD-41 - True CO2 Temperature and Humidity Sensor - STEMMA QT / Qwiic](https://www.adafruit.com/product/5190) | 1 |
| [6V Air Valve with 2-pin JST XH Connector - FA0520E](https://www.adafruit.com/product/4663) | 1 |
| [Adafruit STEMMA Non-Latching Mini Relay - JST PH 2mm](https://www.adafruit.com/product/4409) | 1 |
| [STEMMA JST PH 2mm 3-Pin to Female Socket Cable - 200mm](https://www.adafruit.com/product/3894) | 1 |
| [STEMMA QT / Qwiic JST SH 4-pin Cable - 100mm Long](https://www.adafruit.com/product/4210) | 3 |
| [2 x 4 AA Battery Holder housing with Leads, 2PCS 4 x 1.5V AA Battery Holder Case](https://www.amazon.com/dp/B0DZWK2TNY) | 1 |
| [AA Batteries](https://www.amazon.com/AmazonBasics-Performance-Alkaline-Batteries-20-Pack/dp/B00NTCH52W/) | 4 |

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
