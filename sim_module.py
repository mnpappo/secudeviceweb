import serial
import time
import sys


class gsm():
    echo_on = 1

    def __init__(self, serialPort):
        self.serialPort = serialPort

    def sendCommand(self, at_command):
        self.serialPort.write(at_command + '\r')

    def getResponse(self):
        self.serialPort.flushInput()
        self.serialPort.flushOutput()
        if gsm.echo_on == 1:
            response = self.serialPort.readline()  # comment this line if echo off
        response = self.serialPort.readline()
        response = response.rstrip()
        return response

    def getPrompt(self):
        if gsm.echo_on == 1:
            response = self.serialPort.readline()  # comment this line if echo off
        if (self.serialPort.readline(1) == '>'):
            return True
        else:
            return False

    def sendMessage(self, phone_number, message):
        flag = False
        self.sendCommand('AT+CMGS=\"' + phone_number + '\"')
        time.sleep(2)
        # print ('SUCCESS')
        self.serialPort.write(message)
        self.serialPort.write('\x1A')  # send messsage if prompt received
        flag = True

        time.sleep(5)
        return flag

    def readMessage(self):
        flag = False
        message = ''
        self.sendCommand('AT+CMGR=1')
        self.serialPort.flushInput()
        self.serialPort.flushOutput()
        self.serialPort.readline().rstrip()
        while True:
            response = self.serialPort.readline().rstrip()
            if len(response) > 1:
                if response == 'OK':
                    break
                else:
                    message = message + " " + response
                    flag = True

        return flag, message


if __name__ == "__main__":
    gsm_ser = serial.Serial()
    gsm_ser.port = "/dev/ttyAMA0"
    gsm_ser.baudrate = 9600
    gsm_ser.timeout = 1
    # gsm_ser.xonxoff = False
    # gsm_ser.rtscts = False
    # gsm_ser.bytesize = serial.EIGHTBITS
    # gsm_ser.parity = serial.PARITY_NONE
    # gsm_ser.stopbits = serial.STOPBITS_ONE

    try:
        gsm_ser.open()
        gsm_ser.flushInput()
        gsm_ser.flushOutput()
    except:
        print ('Cannot open serial port')
        sys.exit()

    GSM = gsm(gsm_ser)

    GSM.sendCommand("AT")
    print (GSM.getResponse())

    time.sleep(.1)

    GSM.sendCommand("AT+CMGF=1;&W")
    print (GSM.getResponse())

    time.sleep(.1)

    GSM.sendCommand("AT+CREG?")
    print (GSM.getResponse())

    time.sleep(.1)

    status, msg = GSM.readMessage()
    if status == 0:
        print ('no new messages')
    else:
        print ('new messages arrived: ' + msg)

    message_text = "Hello From Device :P"
    phone_number = "01821081270"
    if (GSM.sendMessage(phone_number, message_text)):
        print 'Message sending Success'
    else:
        print 'Message sending Failed'
    
    time.sleep(.1)
    gsm_ser.close()
