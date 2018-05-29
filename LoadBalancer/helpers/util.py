import struct

class Utility():
    @staticmethod
    def packData(data):
        header = [241,len(data)]
        headPack = struct.pack("!2I", *header)
        data = headPack + data.encode()
        return data

    @staticmethod
    def unpackData(s, queue):
        payload = s.recv(1024)
        if not payload:
            continue
        else:
            dataBuffer += payload
            while True:
                if len(dataBuffer) < headerSize:
                    print("data packet(%s Byte) less than the length of the header" % len(dataBuffer))
                    break

                headPack = struct.unpack('!2I', dataBuffer[:headerSize])
                bodySize = headPack[1]

                if len(dataBuffer) < headerSize+bodySize :
                    print("data packet(%s Byte) is not complete, it should be(%s Byte)," % (len(dataBuffer), headerSize+bodySize))
                    break

                body = dataBuffer[headerSize:headerSize+bodySize]

                queue.put(body)

                dataBuffer = dataBuffer[headerSize+bodySize:]
