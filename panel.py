import tkinter as tk
# Create a new window
window = tk.Tk()
pannelszie=40
window.attributes("-topmost", True)
# Set the title of the window
window.title("Panel")

# Set the dimensions of the window
window.overrideredirect(True)
window.configure(bg='#2c2c2c')



screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (screen_width // 2)   # center horizontally
y = (screen_height) # center vertically

# Set the window's position to the center of the screen
window.geometry(str(screen_width-30)+"x"+str(pannelszie)+"+{}+{}".format(x+14, y-int(pannelszie)-16))
# Run the main event loop to display the window
window.mainloop()
