from block import Block, Attribute
from plotter import Tile
import unittest

class Nametable:
    """A nametable is composed of a number of blocks, 
    each of which containing four tiles and an attribute byte
    
    The complete nametable has a size of 0x3C0 (960) bytes with
    a row width of 32 tiles (the height will then be 30 tiles
    which is 7.5 blocks. Todo: How is this handled?"""
    def __init__(self):
        """Init"""
        self.blocks = None
        self.nTiles={'x':16, 'y':15} # Tiles resolution
        self.settings={'numDumpedBytesInRow':16, # The number of bytes in a row in the dump file
                       'numDumpedAttrInRow':6,  # Number of attribute bytes in row
                       }
    
    def getBlocks(self):
        """Get all blocks in the nametable"""
        return self.blocks
    
    def setBlocks(self, blocks):
        """Set the blocks in the nametable"""
        self.blocks = blocks
        
    def dumpToFile(self, filename, ntTag, attrTag):
        """Dump the nametable to a file using the following format:
        .nametable .db $00, $01, $02, ...  
        
        .attribute .db %10110001, %10110010, ..."""
        f = open(filename, 'w')
        f.write("; Nametable generated from Python script\n\n")
        self._dumpNametableBytes(f, tag=ntTag)
        self._dumpAttributeBytes(f, tag=attrTag)
        f.close()
        
    def _dumpNametableBytes(self, f, tag):
        """Dump the bytes of the nametable
        One byte corresponds to a tile number
        
        The blocks are written line by line, which means
        that the top two tiles in each block in a row is written first.
        Then the bottom two tiles of each block is written in the next line.
        After this the next row uses the top two tiles of the next blocks and so on."""
        
        # The blocks need to be split into rows with bytes
        #       Block1  Block2  Block3
        # Row1  AB      EF      IJ
        # Row2  CD      GH      KL
        #
        dumpStr     = ""
        tilesInRow=0
        bytestream      = []
        bytestreamRow1  = []
        bytestreamRow2  = []
        for block in self.blocks:
            tiles = block.getTiles()
            # Split the block into row bytestreams
            bytestreamRow1.append(tiles[0].getIndex())
            bytestreamRow1.append(tiles[1].getIndex())
            bytestreamRow2.append(tiles[2].getIndex())
            bytestreamRow2.append(tiles[3].getIndex())
            tilesInRow += 2 # Add two tiles to the tiles row counter
            if tilesInRow >= self.nTiles['x']:
                # Finished one row
                # Add the rows to the bytestream
                bytestream += bytestreamRow1+bytestreamRow2
                tilesInRow=0
        
        # Now all tile indexes are stored in the list bytestream
        byteCounter = 0
        dumpStr += "\n%s:" %(tag)
        dumpStr += "\n    .db "
        for byte in bytestream:
            if byteCounter>=self.settings['numDumpedBytesInRow']:
                # Start a new row in the output file
                dumpStr = dumpStr[:-1] # Strip last ", "
                dumpStr += "\n    .db "
                byteCounter = 0
            dumpStr += "$%02X," %(byte)
            byteCounter += 1
        
        dumpStr = dumpStr[:-1] # Strip last ", "
        dumpStr += "\n"
        f.write(dumpStr)
            
                

    def _dumpAttributeBytes(self, f, tag):
        """Dump the attribute bytes in binary format
        for better readability"""
        dumpStr = ""
        
        byteCounter = 0
        dumpStr += "\n%s:" %(tag)
        dumpStr += "\n    .db "
        for block in self.blocks:
            if byteCounter>=self.settings['numDumpedAttrInRow']:
                # Start a new row in the output file
                dumpStr = dumpStr[:-1] # Strip last ", "
                dumpStr += "\n    .db "
                byteCounter = 0
            dumpStr += "%%%s," %(block.getAttribute().getAttributeByteStr())
            byteCounter += 1
        dumpStr = dumpStr[:-1] # Strip last ", "
        dumpStr += "\n"
        f.write(dumpStr)
        
    
class NametableViewer:
    def __init_(self):
        """Init"""
        pass
    
class Tiles:
    """Class for handling tiles"""
    def __init__(self):
        pass

    def open(self, filename):
        """Import file with tile data"""
        with open(filename, "rb") as f:
            byte = f.read(1)
            col = 0
            while byte !="":
                if col>7:
                    print
                    col = 0
                print "0x%02X" %(ord(byte)),
                col += 1
                byte = f.read(1)
                
                
class TestNametable(unittest.TestCase):
    def test_dump(self):
        n = Nametable()
        
        # Create four tiles in a list
        tiles = []
        for i in range(4):
            tiles.append(Tile())
            
        idNum=0
        for tile in tiles:
            tile.setIndex(idNum)
            idNum +=1

        # Create blocks with these tiles
        blocks = []
        attributeCt=0
        for i in range(16):
            block = Block()
            attr = Attribute()
            attr.setAttributeByte(attributeCt) # Set the attribute to a counter value
            block.setTiles(tiles)
            block.setAttribute(attr)
            blocks.append(block)
            
            attributeCt += 1
        n.setBlocks(blocks)
        filename = r"../game/src/test_dump.asm"
        n.dumpToFile(filename, "nametable2", "attribute2")
        
    
if __name__ == "__main__":
    #nv = NametableViewer()
    t = Tiles()
    t.open(r"../game/src/test.chr")