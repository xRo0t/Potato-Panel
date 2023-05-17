import tkinter as tk

my_w = tk.Tk()
my_w.attributes('-fullscreen', True)

def my_callback(event):
    global f_img, my_img
    my_c.coords(my_img, event.x, event.y)

my_c = tk.Canvas(my_w,highlightthickness=0)
my_c.pack(fill='both', expand=True)
my_c.configure(background="#1c1c1c")

wallpaper_img = tk.PhotoImage(file="C:\\msys64\\9d.png")
my_c.create_image(0, 0, image=wallpaper_img)

# Create a draggable red div widget
class RedDiv(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="white", width=60, height=60)
        self.bind("<Button-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.on_move)
        self.place(x=100, y=100)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        self.place(x=self.winfo_x() + event.x - self.x,
                   y=self.winfo_y() + event.y - self.y)

    def stop_move(self, event):
        pass

# Create a RedDiv widget and add it to the canvas
red_div = RedDiv(my_c)
red_div = RedDiv(my_c)
red_div = RedDiv(my_c)

# Add an image to the canvas
#f_img = tk.PhotoImage(file="C:\\msys64\\black-hole.png")
#f_img = f_img.subsample(8)
#my_img = my_c.create_image(180, 50, image=f_img)

# Bind the mouse motion event to the callback function
my_w.bind('<B1-Motion>', my_callback)

# Start the main event loop
my_w.mainloop()
