import spidev
import time
import requests
from requests.exceptions import HTTPError
_numValues = 0
_mean = 0
_s = 0

def server_sendLightData(newData):
        url = 'http://pi-wireless:8000/submitLightValue/'
        url = url + str(newData)
        try:
               response = requests.get(url)
               response.raise_for_status()
        except HTTPError as http_err:
               print ('HTTP error ',http_err)
        except Exception as err:
               print('other error ',err)
        else:
              obj = response.json()
              print(obj)
              return obj['Average']

def WelfordsAlgorithm(newLightValue):
        global _numValues
        global _mean
        global _s
        _numValues += 1
        if _numValues == 1:
                _mean = newLightValue
                _s = 0
        else:
                _oldMean = _mean
                _mean =  _oldMean + (newLightValue - _oldMean) /  _numValues
                _s =  _s + ((newLightValue - _oldMean) * (newLightValue - _mean))
        #print (_numValues)
        return _mean

def createSPI(device):
        spi = spidev.SpiDev()
        spi.open(0,device)
        spi.max_speed_hz=1000000
        spi.mode = 0
        return spi

if __name__ == '__main__':
        try:

    spiR = createSPI(0)                                                                                        
                spiS = createSPI(1)
                while True:
                       # newLightValue = (spiR.readbytes(1))
                       # average = WelfordsAlgorithm(newLightValue[0])
                        command = int(input("Enter a command \n"))
                        if(command == 1):
                                #print ("one \n")
                                spiR.xfer([0x10])
                                time.sleep(1)
                                newLightValue = (spiR.readbytes(1))
                                print (newLightValue[0])
                        elif(command == 2):
                                #print ("two \n")
                                spiS.xfer([0x20])
                                #average = WelfordsAlgorithm(newLightValue[0])
                                average = server_sendLightData(newLightValue[0])
                                print (average)
                                #spiS.xfer([int(average)])
                                print (average)
                        elif(command == 3):
                                #print ("three \n")
                                spiS.xfer([0x40])
                                lightValue = newLightValue[0]
                                #spiS.xfer([0x40])
                                spiS.xfer([int(lightValue)])
                                print (lightValue)
                        else:
                                print ("Enter commands \n")
                        #newLightValue = (spiR.readbytes(1))
                        #print (newLightValue)
                        #average = WelfordsAlgorithm(spiR.readbytes(1)[0])
                        #average = WelfordsAlgorithm(5)
                        #print (average)
                        #spiS.xfer([int(average)])
                        time.sleep(1)
        except KeyboardInterrupt:
                spiR.close()
                spiS.close()
                exit()


