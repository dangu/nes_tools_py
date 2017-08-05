import Tkinter as tk
import constants

class MainWindow(tk.Frame):
    counter = 0
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.button = tk.Button(self, text="Create new",
                                command=self.create_window)
        self.button.pack(side="top")
        
    def create_window(self):
        self.counter += 1
        t = tk.Toplevel(self)
        t.wm_title("Window #%s" %(self.counter))
        l = tk.Label(t, text="This is window #%s" % self.counter)
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)
        
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
    """The color picker window"""
    def __init__(self, main):
        """Init"""
        toplevel = tk.Toplevel(main)
 
        canvas = tk.Canvas(toplevel, width=500, height=400, bd=0, highlightthickness=0)
        canvas.pack()
        self.canvas = canvas
        
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
        col = event.x/self.settings['cellSize'][0]
        row = event.y/self.settings['cellSize'][1]
        if (0<=col<=15) and (0<=row<=3):
            index = row*16+col
            print row,col, index
            self._fgColor = self._colors[index]
            self.drawFgBgColors()

     
        
    def canvas_rightMouseBtn(self, event):
        """Callback for right mouse button"""
                
if __name__ == "__main__":
    root = tk.Tk()
    main = MainWindow(root)
   

    
    colorPicker = ColorPicker(main)
    
    main.pack(side="top", fill="both", expand=True)

    root.mainloop()

import Tkinter

root = Tkinter.Tk()
root.title = "Game"
root.resizable(0,0)
root.wm_attributes("-topmost", 1)

canvas = Tkinter.Canvas(root, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()

class Ball:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)

        self.canvas.bind("<Button-3>", self.canvas_onclick)
        self.canvas.bind("<Button-1>", self.canvas_paint)
        self.text_id = self.canvas.create_text(300, 200, anchor='se')
        self.canvas.itemconfig(self.text_id, text='hello')

    def canvas_onclick(self, event):
        self.canvas.itemconfig(
            self.text_id, 
            text="You clicked at ({}, {})".format(event.x, event.y)
        )
    
    def canvas_paint(self, event):
        """Try to paint some pixels when left mouse button is pressed"""
        self.canvas.create_rectangle(event.x-10, event.y-10, event.x, event.y)

    def draw(self):
        self.canvas.move(self.id, 0, -1)
        self.canvas.after(50, self.draw)


palette_window = Tkinter.Toplevel(root)
palette_canvas = Tkinter.Canvas(palette_window,  width=500, height=400, bd=0, highlightthickness=0)
palette_canvas.pack()


ball = Ball(canvas, "red")
ball.draw()  #Changed per Bryan Oakley's comment.
root.mainloop()