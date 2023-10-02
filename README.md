# Watermark-Application
An implementation of a Watermark application using Tkinter and Pillow python libraries.

## Requirements
python3 -m pip install --upgrade pip   
python3 -m pip install --upgrade Pillow

## How does it work?
First, the user should upload a picture by clicking the left button located on the bottom right corner. If the picture dimensions are smaller than 1200x650 pixels, the picture will be uploaded and saved on the computer system without resizing it. Otherwise, if the picture dimensions are bigger than 1200x650 pixels, the picture will be resized without losing the proportion between width and length. The allowed formats of the picture are: jpeg, png, bitmap, and gif. 

Functionality includes the following:
<ul>
  <li>Entering watermarking text up to 70 characters.</li>
  <li>The choice of text color, white is the default text color.</li>
  <li>The choice of font size, 50 is the default font size.</li>
  <li>The choice of font type, Impact.ttf is the default font type.</li>
  <li>Increase or decrease the opacity of watermark text, 125 is the default opacity value.</li>
  <li>Move the watermarking text up, down, left, or right. The default position is top left corner.</li>
  <li>Rotate the watermarking text on the leftside or rightside.</li>
</ul>

After modifying the watermark text's color, font size, font type, position and opacity, the user should click the right button located in the right bottom corner and filedialog will appear to save the modified picture with watermaker text.
## Demo
<ol>
  <li>Run main.py</li>
  <img width="1434" alt="Screenshot 2023-10-01 at 11 49 47 PM" src="https://github.com/CoboAr/Watermark-Application/assets/144629565/488ed117-6ec8-474c-846a-d6d69fe2df10">
  <li> Click upload button and select picture.</li>
  <img width="1440" alt="Screenshot 2023-10-02 at 12 17 33 AM" src="https://github.com/CoboAr/Watermark-Application/assets/144629565/e40839ed-2b15-408f-951a-cd599b725dc7">
  <li>Type the watermarker text.</li>
  <img width="1437" alt="Screenshot 2023-10-02 at 12 19 28 AM" src="https://github.com/CoboAr/Watermark-Application/assets/144629565/ef6676a1-e6fe-4c5d-9cc7-0b8c7a05a49c">
  <li>Use Application functionalities to change watermaker text color, font size, font type, opacity and position.</li>
  <img width="1438" alt="Screenshot 2023-10-02 at 12 29 58 AM" src="https://github.com/CoboAr/Watermark-Application/assets/144629565/64edfaf8-1a0d-4d1d-8802-bcaddc86bc2c">
  <li>Click the save button and save the watermarked picture in the desired directory in your computer system.</li>
  <img width="1440" alt="Screenshot 2023-10-02 at 12 36 06 AM" src="https://github.com/CoboAr/Watermark-Application/assets/144629565/24efb2d6-87fb-4fd3-9c0e-fa3cfc727b01">
</ol>

Enjoy! And please do let me know if you have any comments, constructive criticism, and/or bug reports.
## Author
## Arnold Cobo
