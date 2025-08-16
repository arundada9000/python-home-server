import logging
import sys
import time
from dns_service import DNSService

# Configure logging to stdout
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("zeroconf")
logger.setLevel(logging.DEBUG)

print("Starting mDNS test...")
try:
    service = DNSService(80, ["test-sajilo"])
    print(f"IP: {service.get_local_ip()}")
    service.register()
    print("Registered. Waiting 10 seconds...")
    time.sleep(10)
    service.unregister()
    print("Unregistered.")
except Exception as e:
    print(f"Error: {e}")
