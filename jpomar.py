import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import RPi.GPIO as io
# tuplje object met pin nummers
leds = (14,18)
buttons = (15,17,23)
ledliving=False
ledkitchen=False

# initialisatie functie voor leds met als parameter een tuple
def init_leds(leds):
    io.setmode(io.BCM)
    io.setup(leds, io.OUT)

def set_leds(leds, states):
    io.output(leds, states)



def init_buttons(buttons):
    io.setmode(io.BCM)
    io.setup(buttons,io.IN,pull_up_down=io.PUD_UP)

def stuur1(data):
    publish.single('home/groundfloor/livingroom/lights/lightx','led1',hostname="192.168.0.110")

def stuur2(data):
    publish.single('home/groundfloor/kitchen/lights/lightx',"led2",hostname="192.168.0.110")

def master(data):
    publish.single('home/groundfloor/','all',hostname="192.168.0.110")

# set state van de leds met als parameters 2 tuples
# tuple van pin nummers en een met bools van de state


# calback voor het verwerken van de berichten

def on_message(client, userdata, msg):
    global ledliving, ledkitchen, leds
    print(msg.payload)
    print("Message Recieved")

    print(ledliving)
    p = msg.payload.decode("utf-8")

    if p == 'led1':
        ledliving = not ledliving
        io.output(14, ledliving)
    if p == 'led2':
        ledkitchen = not ledkitchen
        io.output(18,ledkitchen)
    if p  =='all':
        io.output(18,False)
        io.output(14,False)
    try:
        # payload omzetten van bytestring naar string
        p = msg.payload.decode("utf-8")

        # json wordt verwacht json string moet omgezet worden naar een python
        #  dictonary voor verwerking
        x = json.loads(p)

        #
        set_leds(leds, tuple(x['leds']))
        return
    except Exception as e:
        print(e)



def main():
    try:
        init_leds(leds)
        init_buttons(buttons)
        mqttc = mqtt.Client()
        mqttc.on_message = on_message
        mqttc.connect("127.0.0.1")
        mqttc.subscribe('home/groundfloor/livingroom/lights/lightx')
        mqttc.subscribe('home/groundfloor/kitchen/lights/lightx')
        mqttc.subscribe('home/groundfloor/')
        io.add_event_detect(15, io.BOTH,callback=stuur1,bouncetime=400)
        io.add_event_detect(17, io.BOTH,callback=stuur2,bouncetime=400)
        io.add_event_detect(23, io.BOTH,callback=master,bouncetime=400)


        while True:
                mqttc.loop()




    except KeyboardInterrupt:
        pass
    finally:
        io.cleanup()

# main segment
if __name__ == "__main__":
    main()
                 