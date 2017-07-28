import unittest

class Block:
    """A block is composed of four tiles and an attribute byte.
    The block unit is used in a nametable for the actual graphics.
    The nametable is composed of several blocks"""
    def __init__(self):
        """Init"""
        self.tiles = None
        self.attribute = None
        
        
class Attribute:
    """The attribute is used in a block to set the palette used
    for the separate tiles within the block.
    
    The attribute is a byte which uses two bits for every tile:
    Attribute byte (8 bits): aabbccdd
    Block: aa | bb
           ---|---
           cc | dd
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
        """Get the attribute of the specified tile. The
        tile numbering is as follows:
        0|1
        -|-
        2|3
        """
        assert(0<=tileId<=3)
        attr = (self.attributeByte>>(6-tileId*2))&0x03
        return attr
    
    def setAttribute(self, tileId, attr):
        """Set the attribute of the specified tile. The
        tile numbering is as follows:
        0|1
        -|-
        2|3
        """
        assert(0<=tileId<=3)
        mask = ~(0x03<<(6-tileId*2)) # Mask: ^0b11000000 for tileId=0
        attrShifted = attr<<(6-tileId*2)
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
        
        self.assertEqual(a.getAttributeByte(), 0xC6)
        
        self.assertEqual(a.getAttribute(tileId=0), 0x03)
        self.assertEqual(a.getAttribute(tileId=1), 0x00)
        self.assertEqual(a.getAttribute(tileId=2), 0x01)
        self.assertEqual(a.getAttribute(tileId=3), 0x02)
        
        # Now change one attribute at a time
        a.setAttribute(tileId=0, attr=0x02)
        self.assertEqual(a.getAttribute(tileId=0), 0x02)
        self.assertEqual(a.getAttribute(tileId=1), 0x00)
        self.assertEqual(a.getAttribute(tileId=2), 0x01)
        self.assertEqual(a.getAttribute(tileId=3), 0x02)
        #print a.getAttributeByteStr()
  
        a.setAttribute(tileId=1, attr=0x01)
        self.assertEqual(a.getAttribute(tileId=0), 0x02)
        self.assertEqual(a.getAttribute(tileId=1), 0x01)
        self.assertEqual(a.getAttribute(tileId=2), 0x01)
        self.assertEqual(a.getAttribute(tileId=3), 0x02)
        #print a.getAttributeByteStr()
        
        a.setAttribute(tileId=2, attr=0x00)
        self.assertEqual(a.getAttribute(tileId=0), 0x02)
        self.assertEqual(a.getAttribute(tileId=1), 0x01)
        self.assertEqual(a.getAttribute(tileId=2), 0x00)
        self.assertEqual(a.getAttribute(tileId=3), 0x02)
        #print a.getAttributeByteStr()
        
        a.setAttribute(tileId=3, attr=0x03)
        self.assertEqual(a.getAttribute(tileId=0), 0x02)
        self.assertEqual(a.getAttribute(tileId=1), 0x01)
        self.assertEqual(a.getAttribute(tileId=2), 0x00)
        self.assertEqual(a.getAttribute(tileId=3), 0x03)
        #print a.getAttributeByteStr()
        