from tkinter import *
from tkinter import filedialog as fd, messagebox, ttk
import PIL
from PIL import ImageTk, Image, ImageDraw, ImageFont
import os

class ImageDisplay(Label):
    def __init__(self, parent,watermark):
        """Creates a new image object containing a blank image.
        Provide the parent tkinter object as parent.
        provide the watermark object as watermark."""

        super().__init__(parent)
        self.watermark = watermark
        self.image = Image.new (size=(1200, 650), mode="RGBA", color="white")
        self.photo = ImageTk.PhotoImage (self.image)
        self.configure (image=self.photo, padx=5, pady=5)

    def update_watermark(self):
        """Combines the watermark text with the image"""
        #width of picture uploaded from computer
        self.real_width = self.image.width
        #width of picture uploaded from computer
        self.real_height = self.image.height

        resize_factor = 1
        self.new_width = self.image.width
        self.new_height = self.image.height
        """resize picture so it does not lose quality and format
        If the picture size is bigger than 1200x650, 
        convert it in a picture with a smaller size but with the same raport of length and width """

        while self.new_width>1200 or self.new_height>650:
            resize_factor = resize_factor - 0.01
            self.new_width = int(self.image.width * resize_factor)
            self.new_height = int(self.image.height * resize_factor)
        # Resize picture based on the new width and length
        image = self.image.resize ((self.new_width,self.new_height), Image.Resampling.NEAREST)

        # create the transparent watermark
        txt = Image.new('RGBA', image.size)
        d = ImageDraw.Draw(txt, "RGBA")
        font = ImageFont.FreeTypeFont(f"fonts/{self.watermark.font_type}", size=self.watermark.font_size)
        d = ImageDraw.Draw(txt, "RGBA")
        d.text(xy=(10, 10),
                text=self.watermark.text,
                fill=(self.watermark.color),
                font=font)
        #Starting text width and height
        starting_width = txt.width
        starting_height = txt.height
        # rotate the watermark
        txt = txt.rotate(self.watermark.rotation, expand=True)
        # relocate the watermark after rotation
        offset_x = int((txt.width - starting_width) / 2)
        offset_y = int((txt.height - starting_height) / 2)
        #paste image at the new position
        image.paste(txt, (self.watermark.x - offset_x, self.watermark.y - offset_y), txt)
        #font ratio serves to resize font when the resized picture will be saved on the computer system
        self.font_ratio= int((self.watermark.font_size/self.new_width)*self.real_width)
        self.photo = ImageTk.PhotoImage(image)
        self.configure(image=self.photo)

    def update_photo(self, path):
        """Loads the file at the given path into the ImageDisplay object"""
        try:
            self.image = Image.open(path).convert("RGBA")
        except PIL.UnidentifiedImageError:
            messagebox.showerror("Invalid image", f"{path} is not a valid image file.")

    def save(self):
        """Combines the watermark text with the full-size image and saves file"""
        #load a copy of the uploaded picture
        image = self.image.copy()
        # resize ratio for width and length
        self.resize_ratio_x = self.real_width/self.new_width
        self.resize_ratio_y = self.real_height/self.new_height

        # create the transparent watermark
        txt = Image.new('RGBA', image.size)
        d = ImageDraw.Draw(txt, "RGBA")
        font = ImageFont.FreeTypeFont(f"fonts/{self.watermark.font_type}",self.font_ratio)
        d = ImageDraw.Draw(txt, "RGBA")

        d.text(xy=(10, 10),
                text=self.watermark.text,
                fill=(self.watermark.color),
                font=font)

        # rotate the watermark
        starting_width = txt.width
        starting_height = txt.height
        txt = txt.rotate(self.watermark.rotation, expand=True)

        # relocate the watermark after rotation
        offset_x = int((txt.width - starting_width) / 2)
        offset_y = int((txt.height - starting_height) / 2)

        x_loc = int(self.watermark.x* self.resize_ratio_x  - offset_x)
        y_loc = int(self.watermark.y* self.resize_ratio_y  - offset_y)
        image.paste(txt, (x_loc, y_loc), txt)

        #file_path = fd.asksaveasfile(mode='w', defaultextension=".png")

        file_path = fd.asksaveasfilename(confirmoverwrite=True,
                                         defaultextension="png",
                                         filetypes=[("jpeg", ".jpg"),
                                                    ("png", ".png"),
                                                    ("bitmap", "bmp"),
                                                    ("gif", ".gif") ])
        if file_path is not None: # if dialog not closed with "cancel".
            # Convert to RGB if saving as jpeg
            if os.path.splitext(file_path)[1] == ".jpg":
                image = image.convert("RGB")
            image.save(fp=file_path)

#Color widget
class ColorWidget (Frame):
    def __init__(self, frame, choose_col):
        """Creates a ColorWidget object containing multiple color selections
        Provide the parent tkinter object and a callback function that handles the button clicks"""
        super ().__init__ (frame)
        self.selected_color = ""
        #create select color button
        self.open_button = Button (self, text="Select Color", command=choose_col)
        self.open_button.grid (column=0, row=0)


# Placement button widget
class DirectionWidget (Frame):
    def __init__(self, frame, callback):
        """Creates a DirectionWidget that moves the watermark in any direction
        provide the parent tkinter object and a callback to handle the button clicks"""

        super ().__init__ (frame)
        Label (self, text="Move:").grid (column=0, row=1)
        buttons = [{"text": "▲", "direction": "up", "col": 1, "row": 0},
                   {"text": "◀", "direction": "left", "col": 0, "row": 1},
                   {"text": "▶", "direction": "right", "col": 2, "row": 1},
                   {"text": "▼", "direction": "down", "col": 1, "row": 2}]

        # Create buttons
        for button in buttons:
            btn = ttk.Button (self,
                              text=button["text"],
                              width=1,
                              command=lambda direction=button["direction"]: callback (direction))
            btn.grid (column=button["col"]+1, row=button["row"])

# Rotation widget
class RotationWidget (Frame):
    def __init__(self, frame, callback):
        """Creates a RotationWidget object that rotates the watermark clockwise or counter-clockwise
        provide the parent tkinter object and a callback that handles the button clicks"""

        super ().__init__ (frame)
        Label (self, text="Rotate").grid (column=0, row=0)
        clockwise_button = ttk.Button (self,
                                       text="↻",
                                       width=1,
                                       command=lambda: callback ("right"))
        clockwise_button.grid (column=1, row=0)
        counter_clockwise_button = ttk.Button (self,
                                               text="↺",
                                               width=1,
                                               command=lambda: callback ("left"))
        counter_clockwise_button.grid (column=2, row=0)

#Opacity widget
class OpacityWidget (Frame):
    def __init__(self, frame, callback):
        """Creates an OpacityWidget object that raises or lowers the opacity of the watermark.
        Provide the parent tkinter object and a callback that handles the button clicks"""

        super ().__init__ (frame)
        Label (self, text="Opacity:").grid (column=0, row=0)
        up_button = ttk.Button (self,
                                text="▲",
                                width=1,
                                command=lambda: callback ("up"))
        up_button.grid (column=1, row=0)
        down_button = ttk.Button (self,
                                  text="▼",
                                  width=1,
                                  command=lambda: callback ("down"))
        down_button.grid (column=2, row=0)

# Text Entry widget
class TextEntryWidget (Frame):
    def __init__(self, parent, callback):
        """Creates a TextEntryWidget object with a textbox that sets the watermark text.
        Provide the parent tkinter object and a callback called when the text changes"""
        super ().__init__ (parent)
        Label (self, text="Text:").grid (column=0, row=0)
        sv = StringVar ()
        sv.trace ("w", lambda name, index, mode, sv=sv: callback (sv))
        self.text_entry = Entry (self, textvariable=sv, width=70)
        self.text_entry.grid (column=1, row=0)

# Font size widget
class FontSizeWidget (Frame):
    def __init__(self, parent, callback):
        """Creates a SizeWidget object that allows changing the watermark font size.
        Provide the parent tkinter object and a callback that handles the selection changing of the drop-down"""
        super ().__init__ (parent)
        ttk.Label (self, text="Font Size:").grid (column=0, row=0)
        self.sizeFont_dropdown = ttk.Combobox (self,
                                           values=[i for i in range (10, 200, 4)],
                                           state="readonly",
                                           width=3
                                           )
        self.sizeFont_dropdown.current (5)
        self.sizeFont_dropdown.bind ('<<ComboboxSelected>>', callback)
        self.sizeFont_dropdown.grid (column=1, row=0)

    #get Selected Value of Font Size
    def get_value(self):
        """Returns the font size selected in the dropdown"""
        return self.sizeFont_dropdown.get()


# Font type widget
class FontTypeWidget (Frame):
    def __init__(self, parent, callback):
        """Creates a SizeWidget object that allows changing the watermark font size.
        Provide the parent tkinter object and a callback that handles the selection changing of the drop-down"""
        super ().__init__ (parent)
        ttk.Label (self, text="Font Type:").grid (column=0, row=0)

        fontList = []
        for filename in os.listdir ("fonts"):
            f = os.path.join ("fonts", filename)
            # checking if it is a file
            if os.path.isfile (f):
                # print (f.split ("/"))
                fontList.append (f.split ("/")[1])

        self.typeFont_dropdown = ttk.Combobox (self,
                                           values=[i for i in fontList],
                                           state="readonly",
                                           width=20
                                           )

        self.typeFont_dropdown.current (9)
        self.typeFont_dropdown.bind ('<<ComboboxSelected>>', callback)
        self.typeFont_dropdown.grid (column=0, row=1)

    def get_value(self):
        """Returns the font size selected in the dropdown"""
        return self.typeFont_dropdown.get()


# Open and Save buttons
class OpenSaveWidget(Frame):
    def __init__(self, parent, open_callback, save_callback):
        """Creates a new Open and Save button widget
        Provide both an open_callback function and a save_callback function to handle button clicks"""

        super().__init__(parent)
        self.open_button = Button(self, text="📂", command=open_callback)
        self.open_button.grid(column=0, row=0)
        self.save_button = Button(self, text="💾", command=save_callback, state="disabled")
        self.save_button.grid(column=1, row=0)

    def enable_save(self):
        self.save_button.configure(state="normal")

# Watermark object and methods.
# Supply the main Tk Toplevel widget
class Watermark():
    def __init__(self, parent):
        """Creates a new Watermark object.  Provide the parent ImageBox object"""
        self.parent = parent
        self.font_size = 50
        self.font_type = 'Impact.ttf'
        self.opacity = 125
        self.color = (255, 255, 255, self.opacity)
        self.rotation = 0
        self.x = 10
        self.y = 10
        self.text = ""

    def move(self, direction):
        """Changes the x and y cordinates of the Watermark object by 10 pixels
        direction needs to be a string containing 'up', 'down', 'left', or 'right'"""
        if direction == "up":
                self.y -= 10
        elif direction == "down":
                self.y += 10
        elif direction == "left":
                self.x -= 10
        elif direction == "right":
                self.x += 10

    def change_color(self, color=None):
        """Changes color of the watermark.
           color is a named color string
        """
        if color == None:
            list_color = list(self.color)[:3]
        else:
            list_color = list(color)

        list_color.append(self.opacity)
        self.color = tuple(list_color)

    def change_fontsize(self, event, size):
        """Changes the font_size of the watermark"""
        self.font_size = int(size)

    def change_fonttype(self, event, type):
        """Changes the font_size of the watermark"""
        self.font_type = type


    def change_opacity(self, direction):
        """Changes the opacity of the watermark
        direction is a string, either "up" or "down".  "up" makes it more opaque, "down" makes it more transparent"""
        if direction == "up":
            if self.opacity < 255:
                self.opacity += 5
        else:
            if self.opacity > 0:
                self.opacity -= 5
        self.change_color()

    def rotate(self, direction):
        """Rotates the watermark clockwise or counter-clockwise
        direction should be "left" for counter-clockwise or "right" for clockwise"""
        if direction == "left":
            if self.rotation == 355:
                self.rotation = 0
            else:
                self.rotation += 1.5
        else:
            if self.rotation == 0:
                self.rotation = 355
            else:
                self.rotation -= 1.5

