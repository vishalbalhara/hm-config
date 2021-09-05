import os

from gatewayconfig.logger import logger
from gatewayconfig.gatewayconfig_app import GatewayconfigApp
from dotenv import load_dotenv

# Loads an initial environment, typically from example/.env for development
def load_env_from_dotenv():
    load_from_dotenv_filepath = os.getenv('LOAD_FROM_DOTENV_FILEPATH', False)
    if load_from_dotenv_filepath:
        logger.debug("Loading ENV from dotenv %s" % load_from_dotenv_filepath)
        load_dotenv(load_from_dotenv_filepath)

def load_env_from_system():
    global VARIANT
    VARIANT = os.getenv('VARIANT')
    # SENTRY_CONFIG currently being used in production

    global SENTRY_DSN
    SENTRY_DSN = os.getenv('SENTRY_CONFIG') # https://docs.sentry.io/product/sentry-basics/dsn-explainer/

    global BALENA_DEVICE_UUID
    BALENA_DEVICE_UUID = os.getenv('BALENA_DEVICE_UUID')

    global BALENA_APP_NAME
    BALENA_APP_NAME = os.getenv('BALENA_APP_NAME')

    global FIRMWARE_VERSION
    FIRMWARE_VERSION = os.getenv('FIRMWARE_VERSION')

    global ETH0_MAC_ADDRESS_FILEPATH
    ETH0_MAC_ADDRESS_FILEPATH = os.getenv('ETH0_MAC_ADDRESS_FILEPATH', '/sys/class/net/eth0/address')

    global WLAN0_MAC_ADDRESS_FILEPATH
    WLAN0_MAC_ADDRESS_FILEPATH = os.getenv('WLAN0_MAC_ADDRESS_FILEPATH', '/sys/class/net/wlan0/address')

    global MINER_KEYS_FILEPATH
    MINER_KEYS_FILEPATH = os.getenv('MINER_KEYS_FILEPATH', '/var/data/public_keys')

    global DIAGNOSTICS_JSON_URL
    DIAGNOSTICS_JSON_URL = os.getenv('DIAGNOSTICS_JSON_URL', 'http://localhost:80?json=true')

    global ETHERNET_IS_ONLINE_FILEPATH
    ETHERNET_IS_ONLINE_FILEPATH = os.getenv('ETHERNET_IS_ONLINE_FILEPATH', '/sys/class/net/eth0/carrier')

    # Store as a boolean value
    global IS_GPIO_ENABLED
    IS_GPIO_ENABLED = os.getenv('IS_GPIO_ENABLED', 'True') == 'True'

def validate_env():
    # TODO: Add some sanity checks
    logger.debug("Starting with the following ENV:\n\
        SENTRY_DSN=%s\n\
        BALENA_APP_NAME=%s\n\
        BALENA_DEVICE_UUID=%s\n\
        VARIANT=%s\n\
        ETH0_MAC_ADDRESS_FILEPATH=%s\n\
        WLAN0_MAC_ADDRESS_FILEPATH=%s\n\
        MINER_KEYS_FILEPATH=%s\n\
        DIAGNOSTICS_JSON_URL=%s\n\
        ETHERNET_IS_ONLINE_FILEPATH=%s\n\
        FIRMWARE_VERSION=%s\n\
        IS_GPIO_ENABLED=%s\n" % 
        (SENTRY_DSN, BALENA_APP_NAME, BALENA_DEVICE_UUID, VARIANT, ETH0_MAC_ADDRESS_FILEPATH, 
            WLAN0_MAC_ADDRESS_FILEPATH, MINER_KEYS_FILEPATH, DIAGNOSTICS_JSON_URL, 
            ETHERNET_IS_ONLINE_FILEPATH, FIRMWARE_VERSION, IS_GPIO_ENABLED))

def start():
    config_app = GatewayconfigApp(SENTRY_DSN, BALENA_APP_NAME, BALENA_DEVICE_UUID, VARIANT, 
        ETH0_MAC_ADDRESS_FILEPATH, WLAN0_MAC_ADDRESS_FILEPATH, MINER_KEYS_FILEPATH, 
        DIAGNOSTICS_JSON_URL, ETHERNET_IS_ONLINE_FILEPATH, FIRMWARE_VERSION, IS_GPIO_ENABLED)

    try:
        config_app.start()
    except Exception:
        logger.exception('__main__ failed for unknown reason')
        config_app.stop()

def main():
    load_env_from_dotenv()
    load_env_from_system()
    validate_env()
    start()

if __name__ == "__main__":
    main()