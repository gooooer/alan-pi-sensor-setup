import time
import board
import busio
import logging
from PIL import Image, ImageDraw, ImageFont
import adafruit_as7341
import adafruit_scd4x
import adafruit_ssd1306
import adafruit_tsl2591
# ---------- logging ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
log = logging.getLogger("sensors")
# ---------- I2C ----------
i2c = busio.I2C(board.SCL, board.SDA)
# ---------- Sensors ----------
# AS7341 (10-channel color/light @ 0x39)
spec = adafruit_as7341.AS7341(i2c)
# Optional tuning (sane defaults usually fine):
# spec.gain = adafruit_as7341.Gain.GAIN_64X  # try 4X..256X depending on ambient
# spec.ATIME = 100    # integration time steps (2.78 ms units)
# spec.ASTEP = 999    # measurement step count
# spec.led_current = 25  # mA for onboard LED (if present)
# spec.led = False       # leave LED off for ambient measurements
# TSL2591 (lux @ 0x29)
try:
    tsl = adafruit_tsl2591.TSL2591(i2c)
except Exception as e:
    log.warning(f"TSL2591 init failed: {e}")
    tsl = None
# SCD4x (CO2/Temp/RH @ 0x62)
scd = adafruit_scd4x.SCD4X(i2c)
scd.start_periodic_measurement()
time.sleep(5)
# ---------- OLED (SSD1306, 128x32 @ 0x3C) ----------
WIDTH = 128
HEIGHT = 32
display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)
display.rotation = 2   # try 0,1,2,3
display.fill(0)
display.show()
image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()
def read_spectrum(spec):
    # AS7341 exposes per-band properties (F1..F8, plus clear & NIR)
    # These are raw counts (dimensionless)
    f415 = spec.channel_415nm
    f445 = spec.channel_445nm
    f480 = spec.channel_480nm
    f515 = spec.channel_515nm
    f555 = spec.channel_555nm
    f590 = spec.channel_590nm
    f630 = spec.channel_630nm
    f680 = spec.channel_680nm
    clr  = spec.channel_clear
    nir  = spec.channel_nir
    return {
        "415": f415, "445": f445, "480": f480, "515": f515,
        "555": f555, "590": f590, "630": f630, "680": f680,
        "CLR": clr,  "NIR": nir
    }
while True:
    # ----- clear canvas -----
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    # ----- spectral read -----
    try:
        spec_data = read_spectrum(spec)
    except Exception as e:
        log.warning(f"AS7341 read failed: {e}")
        spec_data = None
    # ----- brightness (Lux) from TSL2591 -----
    if tsl is not None:
        try:
            lux = tsl.lux  # may be None in very low light
            if lux is not None:
                draw.text((0, 0), f"lx:{lux:.1f}", font=font, fill=255)
                log.info("TSL2591 Lux: %.2f", lux)
            else:
                # Keep logging a hint, but don't spam
                log.info("TSL2591 Lux: None (very low light?)")
        except Exception as e:
            log.warning(f"TSL2591 read failed: {e}")
    # For tiny OLED, show Clear and 555 nm (~green peak) as proxies
    if spec_data:
        clr = spec_data["CLR"]
        f555 = spec_data["555"]
        draw.text((40, 0), f"C:{clr:4d} G:{f555:4d}", font=font, fill=255)
        # Log a compact spectrum line (helpful in journalctl)
        log.info(
            "AS7341 F[nm] counts | 415:%d 445:%d 480:%d 515:%d 555:%d 590:%d 630:%d 680:%d CLR:%d NIR:%d",
            spec_data["415"], spec_data["445"], spec_data["480"], spec_data["515"],
            spec_data["555"], spec_data["590"], spec_data["630"], spec_data["680"],
            spec_data["CLR"], spec_data["NIR"]
        )
    else:
        draw.text((0, 0), "AS7341 read error", font=font, fill=255)
    # ----- CO2 / Temp / RH -----
    try:
        if scd.data_ready:
            co2 = scd.CO2
            temp = scd.temperature
            humidity = scd.relative_humidity
            draw.text((0, 10), f"CO2:{int(co2)}ppm", font=font, fill=255)
            draw.text((0, 20), f"T:{temp:.1f}C H:{humidity:.1f}%", font=font, fill=255)
            log.info("SCD4x CO2:%d ppm | Temp:%.1f C | RH:%.1f %%", int(co2), temp, humidity)
        else:
            draw.text((0, 10), "CO2: waiting...", font=font, fill=255)
    except Exception as e:
        log.warning(f"SCD4x read failed: {e}")
        draw.text((0, 10), "SCD4x read err", font=font, fill=255)
    # ----- update OLED -----
    display.image(image)
    display.show()
    time.sleep(2)

