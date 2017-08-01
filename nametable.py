from block import Block, Attribute
from plotter import Tile
import unittest

class Nametable:
    """A nametable is composed of a number of blocks, 
    each of which containing 4*4 tiles and an attribute byte
    
    The complete nametable contains 0x3C0 (960) bytes of tile
    references corresponding to a width of 32 tiles (8 blocks) 
    and a height of 30 tiles (7.5 blocks).
    
    Total number of bytes or tiles: 960
                    blocks:         8*7=56 whole blocks and 8 half blocks
                    
    After the tile references comes an attribute table of 64 bytes
    (8*8 blocks). Each byte in the attribute table describes the palette
    used for each of the subblocks of 2*2 tiles within the block.
    Each nibble of the attribute byte sets the palette used for
    the corresponding subblock.
    
    Total number of bytes: 960+64=1024
    """
    def __init__(self):
        """Init"""
        self.blocks = None
        self.nTiles={'x':32, 'y':30} # The nametable size in sprites
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
        that the top four tiles of each block in a row is written first.
        Then the next four tiles of each block is written in the next line
        and so on."""
        
        # The blocks need to be split into rows with bytes
        #       Block1  Block2  Block3
        # Row1  AB      EF      IJ
        # Row2  CD      GH      KL
        #
        N_ROWS = 4      # Number of rows in a block
        N_COLS = 4      # Number of columns in a block
        dumpStr     = ""
        tilesInRow=0
        bytestream      = []
        bytestreamRows  = [[] for i in range(N_ROWS)]
        for block in self.blocks:
            # Dump the data four rows at a time
            for row in range(N_ROWS):
                bytestreamRows[row]+=block.getRowForNametable(row)
            # Split the block into row bytestreams
            tilesInRow += N_COLS # Add two tiles to the tiles row counter
            if tilesInRow >= self.nTiles['x']:
                # Finished one row
                # Add the rows to the bytestream
                for bytestreamRow in bytestreamRows:
                    bytestream += bytestreamRow
                    
                # Reset to beginning of next row
                tilesInRow=0
                bytestreamRows  = [[] for i in range(N_ROWS)]
        
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
        for i in range(4*4):
            tiles.append(Tile())
            
        idNum=0
        for tile in tiles:
            tile.setIndex(idNum)
            idNum +=1

        # Create blocks with these tiles
        blocks = []
        attributeCt=0
        for i in range(64):
            block = Block()
            attr = Attribute()
            attr.setAttributeByte(attributeCt) # Set the attribute to a counter value
            block.setTiles(tiles)
            block.setAttribute(attr)
            if i>=(8*7):
                block.isInBottomRow()  # This block is in the bottom row (half height)
            blocks.append(block)
            
            attributeCt += 1
        n.setBlocks(blocks)
        filename = r"../game/src/test_dump.asm"
        n.dumpToFile(filename, "nametable2", "attribute2")
        
    
if __name__ == "__main__":
    #nv = NametableViewer()
    t = Tiles()
    t.open(r"../game/src/test.chr")