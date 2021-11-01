'''def do_connect():
    
    #ssid = "Yuma"
    #password = "Dulcinea23928."
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect("Yuma", "Dulcinea23928.")
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())'''

from network import WLAN
import machine
 
def do_connect():
    ssid = "Yuma"
    password = "Dulcinea23928."

    wlan = WLAN(mode=WLAN.STA)

    if wlan.isconnected() == True:
        print("Already connected")
        return

    wlan.connect(ssid, auth=(WLAN.WPA2, password), timeout=5000)

    while not wlan.isconnected():
        machine.idle()

    print("Connection successful")
    print(wlan.ifconfig())
    ip = wlan.ifconfig()
    return ip[0]
