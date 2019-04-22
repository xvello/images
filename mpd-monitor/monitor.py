from time import sleep
import traceback
import os

from mpd import MPDClient
import upnpclient

# The following envvars are needed:
#   - DEVICE_UDN
#   - MPD_ADDR

def turn_on(device):
    device.AVTransport.LeaveStandby(InstanceID=0)

def turn_off(device):
    device.AVTransport.EnterManualStandby(InstanceID=0)

def detect_device(udn):
    devices = upnpclient.discover()
    for d in devices:
        if udn in d.udn:
            return d
    return None

def connect_mpd(host, port):
    cli = MPDClient()
    cli.timeout = 10
    cli.idletimeout = None
    cli.connect(host, port)
    return cli

SPEAKER_UDN = os.environ["SPEAKER_UDN"]
MPD_ADDR = os.environ["MPD_ADDR"]

err_count = 0
last_state = ""

def listen_loop(client, device):
    global last_state
    while True:
        client.idle("player")
        if client.status()["state"] == last_state:
            continue
        last_state = client.status()["state"]
        if client.status()["state"] == "play":
            turn_on(device)

while True:
    try:
        speaker = detect_device(SPEAKER_UDN)
        if speaker is None:
            raise ValueError("Cannot find speaker")
        print("Found speaker at %s" % speaker.location)

        mpd_server = connect_mpd(MPD_ADDR, 6600)
        listen_loop(mpd_server, chopin)
    except (KeyboardInterrupt, SystemExit):
        exit(0)
    except Exception:
        traceback.print_exc()
        err_count += 1
        if err_count > 20:
            print("Too many errors, exiting")
            exit(1)
        sleep(10)
        pass
