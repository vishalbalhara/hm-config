from time import sleep
from gpiozero import LED

from gatewayconfig.logger import logger
from gatewayconfig.gatewayconfig_shared_state import GatewayconfigSharedState

LED_REFRESH_SECONDS = 2

class LEDProcessor:
    def __init__(self, status_led: LED, shared_state: GatewayconfigSharedState, is_gpio_enabled):
        self.status_led = status_led
        self.shared_state = shared_state
        self.is_gpio_enabled = is_gpio_enabled

    def run(self):
        logger.debug("LED LEDProcessor (GPIO enabled = %s)" % self.is_gpio_enabled)

        if self.is_gpio_enabled:
            while True:
                # Blink fast if diagnostics are not OK
                if(self.shared_state.are_diagnostics_ok is False):
                    # logger.debug("Diagnostics are not OK, blinking fast")
                    self.status_led.blink(0.1, 0.1, 10, False)
                # Blink slow if advertising bluetooth
                elif(self.shared_state.is_advertising_bluetooth is True):
                    self.status_led.blink(1, 1, 1, False)
                # Solid if diagnostics are OK and not advertising
                else:
                    self.status_led.on()
                sleep(LED_REFRESH_SECONDS)