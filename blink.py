import gpiod
import time

# Pin 15 on the header is usually offset 12 or 15 on the chip.
# We will use the 'gpiod' way which is much more stable for "Super" boards.
LED_PIN = 15 

# On Orin Nano, the main header is usually chip 0
chip = gpiod.Chip('0')
line = chip.get_line(LED_PIN)
line.request(consumer='LED', type=gpiod.LINE_REQ_DIR_OUT)

try:
    print("Direct GPIO Access: Success!")
    while True:
        line.set_value(1)
        time.sleep(0.5)
        line.set_value(0)
        time.sleep(0.5)
except KeyboardInterrupt:
    line.release()
