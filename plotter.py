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

class Pixel:
    """A pixel with  specific color"""
    def __init__(self):
        """Init"""
        pass
    
class Tile:
    """An 8x8 pixel tile"""
    def __init__(self):
        """Init"""
        self.data = None
    def getRaw(self):
        """Return 8x8 pixels of data
        in the correct raw data format"""
        return self.data
    
class Screen:
    """A full screen containing N number of Tiles.
    256x240 pixels
    Could also be called a nametable"""
    def __init__(self):
        pass

 
class TestTile(unittest.TestCase):
 
    def setUp(self):
        self.tile = Tile()
 
    def test_init(self):

        self.assertEqual(self.tile.data, None)
        
