import Tkinter as tk
from colors import ColorPicker

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