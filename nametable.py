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
                
                
            
        
    
if __name__ == "__main__":
    #nv = NametableViewer()
    t = Tiles()
    t.open(r"../game/src/test.chr")