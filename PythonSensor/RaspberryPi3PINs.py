# Raspberry Pi 3 PIN module that checks the bcm pin input

RaspberryPi3PINs = range(1,28)

def checkPINInput(pin):
    if pin in RaspberryPi3PINs:
        return True
    else:
        print("BCM pin " + str(pin) + " does not exist on the device.")
        return False