from tkinter import colorchooser
from watermark import *

#choose color function
def choose_color():
    # variable to store hexadecimal code of color
    color_code = colorchooser.askcolor (title="Choose color")[0]
    on_color_change(color_code)
#upload picture
def select_file():
        """Handles the Open button click event. Prompts user to select a file and loads it into
        photo_label.
        """
        filename = fd.askopenfilename(filetypes=[("jpeg", ".jpg .jpeg"),
                                                 ("png", ".png"),
                                                 ("bitmap", "bmp"),
                                                 ("gif", ".gif") ])
        if filename != "":
            photo_box.update_photo(filename)
            photo_box.update_watermark()
            open_save.enable_save()


#Create window
window = Tk()
window.geometry("1440x700")
window.title("Watermark")
window.resizable(False, False)

#change color
def on_color_change(inputTuple):
    watermark.change_color(inputTuple)
    photo_box.update_watermark()
#change size
def on_size_change(event):
    watermark.change_fontsize(event, sizeFont_widget.get_value())
    photo_box.update_watermark()
#change font type
def on_type_change(event):
    watermark.change_fonttype(event, typeFont_widget.get_value())
    photo_box.update_watermark()
#update entry text
def on_text_change(sv):
    watermark.text = sv.get()
    photo_box.update_watermark()
#rotate watermark text
def on_rotate(direction):
    watermark.rotate(direction)
    photo_box.update_watermark()
#change position of watermark text
def on_move(direction):
    watermark.move(direction)
    photo_box.update_watermark()
#change opacity of watermark text
def on_opacity_change(direction):
    watermark.change_opacity(direction)
    photo_box.update_watermark()
#Create watermark object
watermark = Watermark(window)
watermark.text = ""

# Create Display Image Box
photo_box = ImageDisplay(window, watermark)
photo_box.grid(column=0,columnspan=10, row=0, padx=5, rowspan=11)
# Create Text Entry Widget
watermark_text = TextEntryWidget(window, on_text_change)
watermark_text.grid(column=0, row=11, padx=6, pady=5)
# Create Color Widget
color_control = ColorWidget(window, choose_color)
color_control.grid(column=10,columnspan=2, row=0,pady=5)
# Create Font Size Widget
sizeFont_widget = FontSizeWidget(window, on_size_change)
sizeFont_widget.grid(column=10,columnspan=2, row=1,pady=5)
# Create Font Type Widget
typeFont_widget = FontTypeWidget(window, on_type_change)
typeFont_widget.grid(column=10,columnspan=2, row=2,rowspan=2, pady=5)
# Create Opacity Widget
OpacityWidget(window, on_opacity_change).grid(column=10,columnspan=2, row=4, pady=5)
# Create Direction Widget
DirectionWidget(window, on_move).grid(column=10,columnspan=2, row=5,rowspan=3, pady=5)
# Create Rotation Widget
RotationWidget(window, on_rotate).grid(column=10,columnspan=2, row=8, pady=5)
# Create Open/Save buttons
open_save = OpenSaveWidget(window, select_file, photo_box.save)
open_save.grid(column=8,columnspan=2, row=11)

window.mainloop()