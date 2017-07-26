import Tkinter

import unittest

def run():
    """Run graphics"""
    top = Tkinter.Tk()
    
    C = Tkinter.Canvas(top, bg="grey", height=200, width=200, cursor = "crosshair")
    coord = 10, 50, 100, 120
    arc = C.create_arc(coord, start=0, extent = 150, fill="red")
    
    C.pack()
    top.mainloop()
    
def bitstreamToByte(bitstream):
    """Convert a bitstream ([0, 0, 1, 0, ...]) 
    to a byte (0xAB)"""
    assert len(bitstream)==8
    byte = 0
    for i in range(8):
        if bitstream[i] == 1:
            byte += 2**(7-i)
    return byte

class Pixel:
    """A pixel with  specific color"""
    def __init__(self):
        """Init"""
        pass
    
class Tile:
    """An 8x8 pixel tile
    
    A tile is stored s two 8 byte color channels. 
    nice explanation is found in [1]. The corresponding
    colors are pulled from the palette.
    
    Channel A  | Channel B | Composite
    F0, F0 ...  | 10, 0F ... | 1113 0000, 1111 2222, ...
    
    
    Ref
    [1]: https://sadistech.com/nesromtool/romdoc.html"""
    def __init__(self):
        """Init"""
        self.data = None
        
    def setData(self, pixels):
        """Set the data according to the input pixels"""
        assert(len(pixels) == 8)
        
        bytestreamA=[]
        bytestreamB=[]
        for row in pixels:
            bitstreamA=[]
            bitstreamB=[]
            for col in row:
                if col==0:
                    bitstreamA.append(0)
                    bitstreamB.append(0)
                elif col==1:
                    bitstreamA.append(1)
                    bitstreamB.append(0)
                elif col==2:
                    bitstreamA.append(0)
                    bitstreamB.append(1)
                elif col==3:
                    bitstreamA.append(1)
                    bitstreamB.append(1)
                else:
                    raise AttributeError("Wrong pixel value!")
            bytestreamA.append(bitstreamToByte(bitstreamA))
            bytestreamB.append(bitstreamToByte(bitstreamB))
        self.data = [bytestreamA, bytestreamB]

        
    def setRawData(self, data):
        """Set the data directly to the tile as a 16 byte array"""
        self.data = [data[:8],data[8:16]]
        
    def getRawData(self):
        """Return 8x8 pixels of data
        in the correct raw data format"""
        return self.data
    
    def getAsciiMatrix(self):
        """Return an 8x8 ascii matrix of the tile,
        where 0,1,2,3 defines the color value
        Example:
        00010000
        00120000
        ..."""
        asciiStr = ""
        for i in range(8):
            # Loop through 8 bytes
            byteA=self.data[0][i]
            byteB=self.data[1][i]
            for bit in range(8):
                char = ((byteA>>(7-bit))&0x01) + 2*((byteB>>(7-bit))&0x01)
                asciiStr += "%d" %char
            asciiStr += '\n'
        return asciiStr
class Screen:
    """A full screen containing N number of Tiles.
    256x240 pixels
    Could also be called a nametable"""
    def __init__(self):
        pass

 
class TestBitstreamToByte(unittest.TestCase):
    def test_1(self):
        self.assertEqual(bitstreamToByte([0,0,0,0,0,0,0,1]), 1)
    def test_2(self):
        self.assertEqual(bitstreamToByte([0,0,0,0,0,0,1,0]), 2)
    def test_FF(self):
        self.assertEqual(bitstreamToByte([1,1,1,1,1,1,1,1]), 0xFF)
        
class TestTile(unittest.TestCase):
 
    def setUp(self):
        self.tile = Tile()
        self.pixels = [[0,0,0,0,0,0,0,0],  # Dummy tile
                  [0,0,0,0,1,0,0,0],
                  [0,0,0,1,0,1,0,0],
                  [0,0,1,0,3,0,1,0],
                  [0,0,1,0,2,0,1,0],
                  [0,0,1,0,3,0,1,0],
                  [0,0,0,1,0,1,0,0],
                  [0,0,0,0,1,0,0,0]]
        
    def createDummyTile(self):
        """Create a dummy tile to work with"""

        self.tile.setData(self.pixels)
 
    def test_init(self):
        # Start with empty tile data
        self.assertEqual(self.tile.data, None)
        
        self.createDummyTile()
        # self.assertEqual(self.tile.data, self.pixels)
       
    def test_inverse(self):
        self.createDummyTile()
        asciiMatrix=self.tile.getAsciiMatrix()
        
        asciiMatrixNoWhitespace = asciiMatrix.replace('\n', '')
        i=0
        for row in self.pixels:
            for pixel in row:
                self.assertEqual(pixel, int(asciiMatrixNoWhitespace[i]))
                i+=1
        
    def test_load_graphics(self):
        """Load graphics data from file"""
        filename = r"../game/src/test.chr"
        
        tileNr=0
        with open(filename, "rb") as f:
            byte = f.read(1)
            col = 0
            byteArray = []
            while byte !="":
                if col>15:
                    print "Tile %d (0x%02X)" %(tileNr, tileNr)
                    self.tile.setRawData(byteArray) # Write the raw data directly to the tile object
                    print self.tile.getAsciiMatrix()    # Print the tile as ascii graphic
                    col = 0
                    byteArray = []
                    tileNr += 1
                byteArray.append(ord(byte))
                print "0x%02X" %(ord(byte)),
                col += 1
                byte = f.read(1)

    def test_setRawData(self):
        """Test setting raw data values"""
        rawData = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        self.tile.setRawData(rawData)
        rawDataReadback = self.tile.getRawData()
        
        i=0
        for channel in rawDataReadback:
            for data in channel:
                self.assertEqual(data, rawData[i])
                i+=1