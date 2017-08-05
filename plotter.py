import Tkinter

import unittest

def run():
    """Run graphics"""
    top = Tkinter.Tk()
    
    tileGroup = TileGroup()
    filename = r"../game/src/test.chr"
    
    # Load a group of tiles from file
    tileGroup.loadFromFile(filename) 
    
    # Set the colors to use with the tiles
    palette = Palette()
    palette.setColors(['black', 'green', 'yellow', 'grey'])
    
    nTilesX = 16
    nTilesY = 32
    xScale  = 3
    yScale = xScale
    C = Tkinter.Canvas(top, bg="grey", width=8*nTilesX*xScale, height=8*nTilesY*yScale, cursor = "crosshair")
    p = PlotterCanvas(C)
    p.setScale(xScale, yScale)
    
    xOffset=0
    yOffset=0
    for tile in tileGroup.tilesIterator():
        print tile.index
        tile.setPalette(palette)
       
        p.plotTileInCanvas(tile, xOffset, yOffset)
        xOffset += 8*xScale
        # Start a new row
        if xOffset>=(nTilesX*8*xScale):
            yOffset += 8*yScale
            xOffset = 0
        
#        if tile.index>200:
#            break
    
    C.pack()
    top.mainloop()

 
class TileGroup:
    """Contains a group of tiles"""
    def __init__(self):
        """Init"""
        self.tiles=[]
    
    def loadFromFile(self, filename):
        """Load tiles from file"""
       
        tileNr=0
        with open(filename, "rb") as f:
            byte = f.read(1)
            col = 0
            byteArray = []
            while True:
                # A tile is 16 bytes. After each 16th byte, start a new tile
                if col>15:
                    tile = Tile()
                    #print "Tile %d (0x%02X)" %(tileNr, tileNr)
                    tile.setRawData(byteArray) # Write the raw data directly to the tile object
                    #print tile.getAsciiMatrix()    # Print the tile as ascii graphic
                    tile.setIndex(tileNr)
                    self.tiles.append(tile)
                    col = 0
                    byteArray = []
                    tileNr += 1
                if byte == "":
                    break
                byteArray.append(ord(byte))
                #print "0x%02X" %(ord(byte)),
                col += 1
                byte = f.read(1)

        print "Loaded %d tiles from file" %(tileNr)
    
    def tilesIterator(self):
        """This method is using "yield" for returning the
        tiles"""
        for tile in self.tiles:
            yield tile

class PlotterCanvas:
    def __init__(self, C):
        self.scale={'x':1, 'y':1}  # x and y scale
        self.canvas = C
        self.canvas.bind("<B1-Motion>", self.canvas_paint)
        
    def setScale(self, x, y):
        """Set the scale in x and y dimension"""
        self.scale['x'] = x
        self.scale['y'] = y
        
    def plotTileInCanvas(self, tile, xOffset, yOffset):
        """Plot a tile inside canvas"""
        matrix = tile.getIntMatrix()  # Get the data
        x=xOffset
        y=yOffset
        for row in matrix:
            for pixel in row:
                coord = x, y, x+self.scale['x'], y+self.scale['y']
                color = tile.getPalette().getColor(pixel)
                self.canvas.create_rectangle(coord, fill=color, outline="black")
                x += self.scale['x']
            y += self.scale['y']
            x = xOffset
            
    def canvas_paint(self, event):
        """Try to paint some pixels when left mouse button is pressed"""
        self.canvas.create_rectangle(event.x-10, event.y-10, event.x, event.y, fill = "yellow", outline = "yellow")
        
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
    
class Palette:
    """A palette with four colors"""
    def __init__(self):
        """Init"""
        self.colors=None
        
    def setColors(self, colors):
        """Set the four colors to use
        Arguments:
        colors    A list with four colors"""
        self.colors = colors
        
    def getColors(self):
        """Return the colors list"""
        return self.colors
    
    def getColor(self, index):
        """Return the color specified by index argument"""
        return self.colors[index]
    
class Tile:
    """An 8x8 pixel tile
    
    A tile is stored as two 8 byte color channels. 
    A nice explanation is found in [1]. The corresponding
    colors are pulled from the palette.
    
    Channel A  | Channel B | Composite
    F0, F0 ...  | 10, 0F ... | 1113 0000, 1111 2222, ...
    
    
    Ref
    [1]: https://sadistech.com/nesromtool/romdoc.html"""
    def __init__(self):
        """Init"""
        self.data = None
        self.index = None
        self.palette = None
        
    def setPalette(self, palette):
        """Set the palette to be used with this tile"""
        self.palette = palette
        
    def getPalette(self):
        """Return the palette used with this tile"""
        return self.palette
        
    def getIndex(self):
        """Get the tile index"""
        return self.index
    
    def setIndex(self, index):
        """Set the tile index property"""
        self.index = index
        
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
                val = ((byteA>>(7-bit))&0x01) + 2*((byteB>>(7-bit))&0x01)
                asciiStr += "%d" %val
            asciiStr += '\n'
        return asciiStr
    
    def getIntMatrix(self):
        """Return an 8x8 matrix (a list of lists) with numbers 0,1,2,3
        corresponding to colors.
        Example:
        [[0,0,0,1,0,0,3,0],[0,0,1,1,0,0,1,0],...]"""
        intMatrix = []
        for i in range(8):
            # Loop through 8 bytes
            byteA=self.data[0][i]
            byteB=self.data[1][i]
            intListInner=[]
            for bit in range(8):
                val = ((byteA>>(7-bit))&0x01) + 2*((byteB>>(7-bit))&0x01)
                intListInner.append(val)
            intMatrix.append(intListInner)
        return intMatrix


    
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
                
        
if __name__=="__main__":
    print "Running main..."
    run()