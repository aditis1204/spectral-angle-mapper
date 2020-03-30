# Spectral_angle_mapper
SAM classifier for remote sensing images.
Python libraries required -Ratserio,OpenCV,Numpy,Tkinter,matplot.
Allows user to click on a part of image to act as training data for a class.
Threshold for classification angle < 0.1 radians else unclassified.
Steps of execution the python file:
1. Run the program.
2. Browse and select the 4 band input image.( If inpput image is not 4 band it will give a error message saying " NOT A 4 BAND Image"
3. Click on "Show TCC&FCC".
    	Two windows will open, titled as Figure1 corresponding to TCC & Figure 2 corresponding to FCC.
4. Double click on pixels which you want to consider as reference pixels( In FCC image i.e. Figure2)
5. After selecting reference pixels close all windows including main window and wait for the classified image to pop up in some time.
6. If you want to save classified image you can save it.
7. After closing the classified image a new window will appear showing the TCC, FCC and Classified image at once.
8. There is a default palatte loaded to classify, which is also incuded in folder named as "palette.jpg"
