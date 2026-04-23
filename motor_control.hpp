#include <pigpio.h>
#include <unistd.h>

const int PWMA = 18;
const int AIN1 = 17;
const int AIN2 = 27;

void setup_motors() {
    if (gpioInitialise() < 0) return;
    gpioSetMode(PWMA, PI_OUTPUT);
    gpioSetMode(AIN1, PI_OUTPUT);
    gpioSetMode(AIN2, PI_OUTPUT);
    
    gpioWrite(AIN1, 0);
    gpioWrite(AIN2, 0);
    gpioPWM(PWMA, 255); // Full Speed
}

void spin_dispenser(float seconds) {
    gpioWrite(AIN1, 1);
    gpioWrite(AIN2, 0);
    usleep(seconds * 1000000); // Sleep in microseconds
    gpioWrite(AIN1, 0);
    gpioWrite(AIN2, 0);
}
