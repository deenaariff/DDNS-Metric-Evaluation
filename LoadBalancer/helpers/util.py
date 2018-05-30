import struct
import json
import config
class Utility():
    @staticmethod
    def packData(data):
        d = json.dumps(data)
        header = [3,d.__len__()]
        headPack = struct.pack("!2I", *header)
        output = headPack + d.encode()
        return output

    @staticmethod
    def unpackData(s, queue):
        payload = s.recv(10000)
        dataBuffer = ''
        headerSize = 8
        if payload:
            dataBuffer += payload
            while True:
                if len(dataBuffer) < headerSize:
                    print("data packet(%s Byte) less than the length of the header" % len(dataBuffer))
                    break

                headPack = struct.unpack('!2I', dataBuffer[:headerSize])
                #print('util headPack',headPack)
                bodySize = headPack[1]
                if len(dataBuffer) < headerSize+bodySize :
                    print("data packet(%s Byte) is not complete, it should be(%s Byte)," % (len(dataBuffer), headerSize+bodySize))
                    break

                body = dataBuffer[headerSize:headerSize+bodySize]
                queue.put(body.decode())

                dataBuffer = dataBuffer[headerSize+bodySize:]
