import board, time,neopixel
from analogio import AnalogIn

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket

# setup bluetooth
ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)
# Give your CPB a unique name between the quotes below
advertisement.complete_name = "GlowBall"
ble.name = advertisement.complete_name  # This should make it show in the Bluefruit Connect app. It often takes time to show.
print(f"ble.name is {ble.name}")

WHITE = (200,80,255)# GBR
BLACK = (0,0,0)
strand = neopixel.NeoPixel(board.TX, 26)
pads = [board.A1, board.A2, board.A3, board.A4, board.A5, board.A6]
sensors = []
for i in range(6):
     sensors.append(AnalogIn(pads[i]))
color = WHITE
force = [0,0,0,0,0,0]

#layout of pixels surrounding each force sensor
l1 = [7,3,6,21,16,20,12,4,11]
l2 = [11,5,1,4,15,9,12,8,13]
l3 = [6,2,18,20,19,10,11,5,1]
l4 = [18,23,26,10,14,24,1,9,13]
l5 = [6,3,7,2,17,22,18,23,26]
l6 = [26,22,7,24,25,21,13,8,12]
lights = [l1, l2, l3, l4, l5, l6]

def glow():
    for i in range(6):
        force[i] = sensors[i].value
        if force[i] >1000:
            for light in lights[i]:
                strand[light-1] = color
        else:
            for light in lights[i]:
                strand[light-1] = BLACK
    # print(force)
    # strand.brightness = force/65000
    # time.sleep(0.2)

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        glow()
    while ble.connected:
        ble.stop_advertising()
        if uart_server.in_waiting:
            try:
                packet = Packet.from_stream(uart_server)
            except ValueError:
                continue  # or pass. This will start the next

            if isinstance(packet, ColorPacket):  # A color was selected from the app color picker
                R,G,B = packet.color
                color = (G,B,R)
        glow()





