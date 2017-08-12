import Tkinter as tk
import constants
        
class Color():
    """Containing methods for handling a color"""
    def __init__(self, rgbValues):
        """Init"""
        self._rgbValues = rgbValues
        
    def tkColor(self):
        """Return in a format that Tkinter can understand
        
        Example:
        "#12FA43"
        """
        colorInHex = "#%02X%02X%02X" %(self._rgbValues[0], 
                                       self._rgbValues[1], 
                                       self._rgbValues[2])
        return colorInHex
    
def importColors():
    """Import all colors and wrap them in Color objects"""
    colors = []
    for color in constants.PALETTE:
        colors.append(Color(color))
    return colors
    
    
class ColorPicker():
    """The color picker window
    main             The main window
    plotterCanvas    The plotter canvas window"""
    def __init__(self, main, plotterCanvas):
        """Init"""
        toplevel = tk.Toplevel(main)
 
        canvas = tk.Canvas(toplevel, width=500, height=400, bd=0, highlightthickness=0)
        canvas.pack()
        self.canvas = canvas
        self.plotterCanvas = plotterCanvas
        
        self._colors = importColors()
        self._fgColor = self._colors[0]
        self._bgColor = self._colors[2]
        self.settings = {'cellSize':[20,20],}
        
        self.drawPalette()
        self.drawFgBgColors()
        # Bind events
        self.canvas.bind("<Button-1>", self.canvas_leftMouseBtn)
        self.canvas.bind("<Button-3>", self.canvas_rightMouseBtn)

    
    def drawPalette(self):
        """Show the complete palette"""
        x=0
        y=0
        width=self.settings['cellSize'][0]
        height=self.settings['cellSize'][1]
        rowWidth = 16
        ct = 0
        for color in self._colors:
            self.canvas.create_rectangle(x,y, x+width,y+height, fill=color.tkColor())
            x+=width
            ct += 1
            if ct>=rowWidth:
                ct=0
                y+=height
                x=0
    def drawFgBgColors(self):
        """Draw the two foreground/background color fields"""
        xFg = 300
        yFg = 300
        szFg = 30
        xBg = xFg+10
        yBg = yFg+10
        szBg = szFg
        self.canvas.create_rectangle(xBg,yBg,xBg+szBg,yBg+szBg, fill=self._bgColor.tkColor())
        self.canvas.create_rectangle(xFg,yFg,xFg+szFg,yFg+szFg, fill=self._fgColor.tkColor())
        
    def canvas_leftMouseBtn(self, event):
        """Callback for left mouse button"""
        self._changeFgBgColor(event, which="fg")

    def canvas_rightMouseBtn(self, event):
        """Callback for right mouse button"""
        self._changeFgBgColor(event, which="bg")    
    
    def _changeFgBgColor(self, event, which):
        """Change either the foreground or the background 
        color, depending on the input parameter which.
        which=="fg" => Foreground color
        which=="bg" => Background color"""
        assert((which == "fg") or (which == "bg"))
        
        col = event.x/self.settings['cellSize'][0]
        row = event.y/self.settings['cellSize'][1]
        if (0<=col<=15) and (0<=row<=3):
            index = row*16+col
            print row,col, index
            if which == "fg":
                self._fgColor = self._colors[index]
            elif which=="bg":
                self._bgColor = self._colors[index]
            # Communicate the colors to the plotter window
            self.plotterCanvas.setFgBgColors(self._fgColor, self._bgColor)
            self.drawFgBgColors()
     