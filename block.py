import unittest
from plotter import Tile

class Block:
    """A block is composed of 4*4 tiles and an attribute byte.
    The block unit is used in a nametable for the actual graphics.
    The nametable is composed of several blocks"""
    def __init__(self):
        """Init"""
        self.tiles = None
        self.attribute = None
    
    def getTiles(self):
        """Get the tiles list"""
        return self.tiles
    
    def setTiles(self, tiles):
        """Set the list of tiles"""
        assert(len(tiles)==4*4)
        self.tiles = tiles
        
    def getRowForNametable(self, rowNumber):
        """Get a complete row of tile indexes
        for creating nametable"""
        assert(0<=rowNumber<=3)
        
        row = []
        
        # Create the mapping for this row
        tileNums = [tileNum+rowNumber*4 for tileNum in [0,1,2,3]]
        
        for tileNum in tileNums:
            row.append(self.tiles[tileNum].getIndex())

        return row
        
    def getAttribute(self):
        """Get the attribute"""
        return self.attribute
        
    def setAttribute(self, attr):
        """Set the attribute"""
        self.attribute = attr    
        
class Attribute:
    """The attribute is used in a block to set the palette used
    for the separate tiles within the block.
    
    The attribute is a byte which uses two bits for every 
    subset of 2x2 tiles as shown in the following diagram:
    Attribute byte (8 bits): aabbccdd
    Block: dd | cc
           ---|---
           bb | aa
           
    The tile numbering within a block is as follows:
     0  1| 2  3
     4  5| 6  7
    -----|-----
     8  9|10 11
    12 13|14 15
    """
    def __init__(self):
        """Init"""
        self.attributeByte = None
    
    def getAttributeByte(self):
        """Return the attribute byte"""
        return self.attributeByte
    
    def setAttributeByte(self, attributeByte):
        """Set the attribute byte"""
        self.attributeByte = attributeByte
        
    def getAttribute(self, tileId):
        """Get the attribute of the specified tile"""
        assert(0<=tileId<=15)
        
        nibble = self._getNibble(tileId)
        attr = (self.attributeByte>>(6-nibble*2))&0x03
        return attr
    
    def _getNibble(self, tileId):
        """As the block is divided of subblocks with
        2*2 tiles, each using a nibble (2 bits) of the attribute,
        there is a need for some kind of mapping.
        
        This method resilves the mapping of tile to attribute nibble"""
        if tileId in [0,1,4,5]:
            nibble=0
        elif tileId in [2,3,6,7]:
            nibble=1
        elif tileId in [8,9,12,13]:
            nibble=2
        elif tileId in [10,11,14,15]:
            nibble=3
        else:
            raise AttributeError("tileId not found")
        return nibble
    
    def setAttribute(self, tileId, attr):
        """Set the attribute of the specified tile
        
        Note that this will affect all tiles in the subblock of
        2*2 tiles
        """
        assert(0<=tileId<=15)
        nibble = self._getNibble(tileId)
        mask = ~(0x03<<(6-nibble*2)) # Mask: ^0b11000000 for tileId=0
        attrShifted = attr<<(6-nibble*2)
        self.attributeByte = (self.attributeByte & mask) | attrShifted
    
    def getAttributeByteStr(self):
        """Return the attribute byte as an ascii string.
        
        Example:
        01011100
        """
        attrStr = ""
        for i in range(8):
            attrStr += "%d" %((self.attributeByte>>(7-i))&0x01)
        return attrStr
        
# *************** Unit tests ***********
class TestTile(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_attribute(self):
        a = Attribute()
        a.setAttributeByte(0xC6)
        #print a.getAttributeByteStr()
        
        self.assertEqual(a.getAttributeByte(), 0xC6) # 0xC6 = 0b11000110
        
        self.assertEqual(a.getAttribute(tileId=0), 0x03)
        self.assertEqual(a.getAttribute(tileId=1), 0x03)
        self.assertEqual(a.getAttribute(tileId=2), 0x00)
        self.assertEqual(a.getAttribute(tileId=3), 0x00)
        self.assertEqual(a.getAttribute(tileId=9), 0x01)
        self.assertEqual(a.getAttribute(tileId=14), 0x02)
            
        # Now change one attribute at a time
        a.setAttribute(tileId=0, attr=0x02)
        self.assertEqual(a.getAttribute(tileId=0), 0x02)
        self.assertEqual(a.getAttribute(tileId=1), 0x02)
        self.assertEqual(a.getAttribute(tileId=2), 0x00)
        self.assertEqual(a.getAttribute(tileId=3), 0x00)
        self.assertEqual(a.getAttribute(tileId=9), 0x01)
        self.assertEqual(a.getAttribute(tileId=14), 0x02)
        #print a.getAttributeByteStr()
  
        a.setAttribute(tileId=6, attr=0x01)
        self.assertEqual(a.getAttribute(tileId=0), 0x02)
        self.assertEqual(a.getAttribute(tileId=1), 0x02)
        self.assertEqual(a.getAttribute(tileId=2), 0x01)
        self.assertEqual(a.getAttribute(tileId=3), 0x01)
        self.assertEqual(a.getAttribute(tileId=9), 0x01)
        self.assertEqual(a.getAttribute(tileId=14), 0x02)
        #print a.getAttributeByteStr()
        
        a.setAttribute(tileId=13, attr=0x00)
        self.assertEqual(a.getAttribute(tileId=0), 0x02)
        self.assertEqual(a.getAttribute(tileId=1), 0x02)
        self.assertEqual(a.getAttribute(tileId=2), 0x01)
        self.assertEqual(a.getAttribute(tileId=3), 0x01)
        self.assertEqual(a.getAttribute(tileId=9), 0x00)
        self.assertEqual(a.getAttribute(tileId=14), 0x02)
        
        a.setAttribute(tileId=11, attr=0x03)
        self.assertEqual(a.getAttribute(tileId=0), 0x02)
        self.assertEqual(a.getAttribute(tileId=1), 0x02)
        self.assertEqual(a.getAttribute(tileId=2), 0x01)
        self.assertEqual(a.getAttribute(tileId=3), 0x01)
        self.assertEqual(a.getAttribute(tileId=9), 0x00)
        self.assertEqual(a.getAttribute(tileId=14), 0x03)
        
class TestBlock(unittest.TestCase):
    def test_init(self):
        b = Block()
        
        # Create four tiles to use
        tiles = []
        for i in range(4*4):
            tiles.append(Tile())
        a = Attribute()
        a.setAttributeByte(0xCA)
        
        b.setTiles(tiles)
        b.setAttribute(a)