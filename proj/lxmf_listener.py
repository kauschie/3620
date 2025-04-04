# if on windows and using wsl, uses these commands in powershell:
# usbipd list (to get the port number)
# usbipd bind --busid 3-2  (match 3-2 to the port number from usbipd list)

# and then 

# usbipd attach --wsl --busid 3-2 
# then it should be listed in the devices
# can view it with ls /dev/tty* 
# may be something like /dev/ttyACM0


import os
import time
import logging
import RNS
import LXMF
import audio_utils as audio
from LXMF import LXMessage as LXM

# === CONFIG ===
APP_NAME = "lxmf_listener"
STORAGE_DIR = os.path.expanduser(f"~/.rns_{APP_NAME}")
IDENTITY_FILE = os.path.join(STORAGE_DIR, "identity")
LOGFILE = os.path.join(STORAGE_DIR, "listener.log")
DISPLAY_NAME = "AudioNode"
STAMP_COST = 8
ANNOUNCE_INTERVAL = 30  # seconds
TEST_WAV_PATH = "/home/mkausch/dev/3620/proj/sup.wav"

os.makedirs(STORAGE_DIR, exist_ok=True)

# === Logging ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOGFILE),
        logging.StreamHandler()
    ]
)

# === Identity ===
if os.path.exists(IDENTITY_FILE):
    identity = RNS.Identity.from_file(IDENTITY_FILE)
    logging.info("[ID] Loaded identity from disk.")
else:
    identity = RNS.Identity()
    identity.to_file(IDENTITY_FILE)
    logging.info("[ID] Created new identity and saved to disk.")

# === Reticulum & LXMF ===
RNS.Reticulum()  # will use system config or ~/.reticulum
router = LXMF.LXMRouter(storagepath=STORAGE_DIR, enforce_stamps=True)
for iface in RNS.Transport.interfaces:
    logging.info(f"[IFACE] Found interface: {iface.name}, via port: {getattr(iface, 'serial_port', 'n/a')}")


# Register destination for receiving
destination = router.register_delivery_identity(
    identity,
    display_name=DISPLAY_NAME,
    stamp_cost=STAMP_COST
)

# === Handle incoming messages ===
def handle_delivery(message: LXM):
    try:
        logging.info("=== LXMF MESSAGE RECEIVED ===")
        logging.info(f"From      : {RNS.prettyhexrep(message.source_hash)}")
        logging.info(f"Title     : {message.title_as_string()}")
        logging.info(f"Content   : {message.content_as_string()}")
        logging.info(f"Fields    : {message.fields}")
        logging.info("==============================")


        # Detect and handle incoming audio message
        if message.fields and 7 in message.fields:
            logging.info("[AUDIO] Audio field detected. Attempting to decode...")
            decoded_path = audio.save_and_decode_audio(message.fields)

            if decoded_path:
                logging.info(f"[AUDIO] Audio saved and decoded to: {decoded_path}")
                print(f"[🎧 AUDIO] Message from {RNS.prettyhexrep(message.source_hash)} saved to {decoded_path}")
            else:
                logging.warning("[AUDIO] Failed to decode audio message.")
        
        reply = audio.create_lxmf_audio_message(message.source, destination, TEST_WAV_PATH, codec="codec2", title="Voice Message", bitrate=1200)
            
        router.handle_outbound(reply)
        print("[AudioNode] Replied.")


    except Exception as e:
        logging.error(f"Error handling message: {e}")

router.register_delivery_callback(handle_delivery)

logging.info(f"[READY] Listening on: {RNS.prettyhexrep(destination.hash)}")

# === Announce destination periodically ===

def periodic_announce():
    boot_time = time.time()
    while True:
        success = router.announce(destination.hash)
        logging.info("[AudioNode] Announced to LXMF network. Success: {}".format(success))
        # if time.time() - boot_time < 10:
        time.sleep(5)  # fast announce for first 10 seconds
        # else:
            # time.sleep(120)  # slow down after  



# Start it explicitly with error logging
try:
    import threading
    announce_thread = threading.Thread(target=periodic_announce, daemon=True)
    announce_thread.start()
    logging.info("[ANNOUNCE] Announce thread started.")
except Exception as e:
    logging.error(f"[ANNOUNCE] Failed to start announce thread: {e}")

# === Keep the script alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logging.info("Exiting.")
