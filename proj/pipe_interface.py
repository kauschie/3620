import time
import logging
import RNS
import os
import LXMF
from LXMF import LXMessage as LXM

proj_path = "/home/mkausch/dev/3620/proj/"
log_path = os.path.join(proj_path, "pipe_interface.log")

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path, mode="a"),
        logging.StreamHandler()
    ]
)

# Delivery callback
def delivery_callback(message: LXM):
    try:
        time_string      = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(message.timestamp))
        signature_string = "Signature is invalid, reason undetermined"
        if message.signature_validated:
            signature_string = "Validated"
        else:
            if message.unverified_reason == LXMF.LXMessage.SIGNATURE_INVALID:
                signature_string = "Invalid signature"
            if message.unverified_reason == LXMF.LXMessage.SOURCE_UNKNOWN:
                signature_string = "Cannot verify, source is unknown"
        if message.stamp_valid:
            stamp_string = "Validated"
        else:
            stamp_string = "Invalid"

        logging.info("\t+--- LXMF RECEIVED FROM PIPE ---------------------------")
        logging.info("\t| Source hash            : "+RNS.prettyhexrep(message.source_hash))
        logging.info("\t| Source instance        : "+str(message.get_source()))
        logging.info("\t| Destination hash       : "+RNS.prettyhexrep(message.destination_hash))
        logging.info("\t| Destination instance   : "+str(message.get_destination()))
        logging.info("\t| Transport Encryption   : "+str(message.transport_encryption))
        logging.info("\t| Timestamp              : "+time_string)
        logging.info("\t| Title                  : "+str(message.title_as_string()))
        logging.info("\t| Content                : "+str(message.content_as_string()))
        logging.info("\t| Fields                 : "+str(message.fields))
        if message.ratchet_id:
            logging.info("\t| Ratchet                : "+str(RNS.Identity._get_ratchet_id(message.ratchet_id)))
        logging.info("\t| Message signature      : "+signature_string)
        logging.info("\t| Stamp                  : "+stamp_string)
        logging.info("\t+---------------------------------------------------------------")


        # Optional echo
        reply = LXM(
            destination = message.source,
            source = my_lxmf_destination,
            content = f"Echo from pipe: {str(message.content_as_string())}",
            title = "Reply",
            desired_method = LXM.DIRECT,
            include_ticket = True
        )
        router.handle_outbound(reply)
        logging.info("[SEND] Echo sent from the pipe.")
        print(f"[PRINT FROM PIPE_INTERFACE] Echo sent from the pipe.")
    except Exception as e:
        logging.error(f"Error handling LXMF message: {e}")

# Reticulum & LXMF setup
RNS.Reticulum()
# router_path = os.path.join(proj_path, "pipe_storage")
router = LXMF.LXMRouter(storagepath="./pipe_storage", enforce_stamps=False)
identity = RNS.Identity()
my_lxmf_destination = router.register_delivery_identity(identity, display_name="PipeEcho")
router.register_delivery_callback(delivery_callback)
logging.info(f"[PipeInterface] Ready to receive on: {RNS.prettyhexrep(my_lxmf_destination.hash)}")
router.announce(my_lxmf_destination.hash)
logging.info(f"[PipeInterface] Announced on: {RNS.prettyhexrep(my_lxmf_destination.hash)}")
# Idle loop (Reticulum handles async)
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logging.info("Exiting.")
