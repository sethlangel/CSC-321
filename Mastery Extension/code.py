from machine import Pin
from utime import sleep
from libs.mfrc522 import SimpleMFRC522
import time

def log_event(tagId: str, tagData, type: str):
    with open("log.txt", "a") as f:
        t = time.localtime()
        timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(t[0], t[1], t[2], t[3], t[4], t[5])

        access_status = ""

        if type == "Read":
            access_status = " - Access Granted" if str(tagData).strip() in authorized_uids else " - Access Denied"

        log_msg = f"{timestamp} - Type: {type} - Tag ID: {tagId} - Tag Data (UID): {tagData} {access_status}"
        f.write(log_msg + "\n")

def read_tag(reader: SimpleMFRC522):
    try:
        print("Reading... Please place the card...")
        tagId, tagData = reader.read()
        print("ID: ", tagId, " Data: ", tagData)

        if str(tagData).strip() in authorized_uids:
            LED_Green.on()
            print("Access Granted")
        else:
            LED_Red.on()
            print("Access Denied")
            
        log_event(tagId, tagData, "Read")

        sleep(2)
        LED_Green.off()
        LED_Red.off()
        
    except Exception as e:
        print(f"Error Reading Tag: {e}")

def write_tag(reader: SimpleMFRC522):
    data = input("Enter new UID...\n")
    try:
        print("Attempting to write... Please place tag...")
        tagId, tagData =reader.write(data)
        log_event(tagId, tagData, "Write")
        print("Write to tag successful!")
    except Exception as e:
        print(f"Error Writing to Tag: {e}")

def spoof_tag(reader: SimpleMFRC522):
    try:
        print("------ Demonstrating Spoof Attack ------\n")
        print("Reading... Please place the card...\n")
        tagId, tagData = reader.read()
        log_event(tagId, tagData, "Read")
        print("Please remove card...")
        sleep(1)
        print("Writing... Please place the card...\n")
        tagId, tagData = reader.write(tagData)
        log_event(tagId, tagData, "Write")

    except Exception as e:
        print(f"Error Spoofing: {e}")

reader = SimpleMFRC522(spi_id=0, sck=18, miso=16, mosi=19, cs=17, rst=9)
LED_Green = Pin(14, Pin.OUT)
LED_Red = Pin(15, Pin.OUT)
authorized_uids = {"1"}

while True:
    mode = input("""
                ------ Basic Operations ------
                Read [r]
                Write [w]
                Quit [q]
                
                ------ Attack Operations ------
                UID Spoofing [s]
                 """)
    
    if mode == "r":
        read_tag(reader)
    elif mode == "w":
        write_tag(reader)
    elif mode == "s":
        spoof_tag(reader)
    elif mode == "q":
        quit()
    else:    
        print("Incorrect option selected. Please try again.\n")