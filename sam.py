import rasterio #read and process rasters
from rasterio.plot import show #display rasters


import numpy #matrices
from numpy.linalg import norm #noramlised magnitude
import cv2 #saving classified image
import tkinter #gui

from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox # diplsay messages in UI

#UI

class Root(tkinter.Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("SAM")
        #self.wm_iconbitmap('icon1.ico')

        self.labelFrame1 = ttk.LabelFrame(self, text = "1.Open A File") #function1
        self.labelFrame1.grid(column = 0, row = 1, padx = 10, pady = 30)

        self.labelFrame2 = ttk.LabelFrame(self, text="2.Display TCC&FCC") #function2
        self.labelFrame2.grid(column=12, row=1, padx=10, pady=30)

        self.button1()
        self.button2()

    def button1(self):
        self.button1 = ttk.Button(self.labelFrame1, text = "Browse a File", command = self.fileDialog)
        self.button1.grid(column = 1, row = 1)

    def fileDialog(self): #readfile
        self.filename = filedialog.askopenfilename(initialdir = "\\", title = "Select a File", filetype = (("tiff", "*.tif"), ("All Files", "*.*")))
        self.label = ttk.Label(self.labelFrame1, text = "")
        self.label.grid(column = 1, row = 2)

        self.num_of_dir_till_file = len(self.filename.split("/"))
        self.just_file_name = self.filename.split("/")[self.num_of_dir_till_file - 1]

        self.label.configure(text="Selected : " + self.just_file_name)



    def button2(self):
        self.button2 = ttk.Button(self.labelFrame2, text = "Show TCC&FCC", command = self.fun1)
        self.button2.grid(column = 3, row = 4)


    def fun1(self):


        import matplotlib.pyplot as plt #for drawing images

        raster= rasterio.open(self.filename, 'r')
        #print(raster.shape)



        #read image with band
        # Read the grid values into numpy arrays
        nir= raster.read(4)
        red = raster.read(3)
        green = raster.read(2)
        blue = raster.read(1)



        #normalize the grid values
        def normalize(array):
            """Normalizes numpy arrays into scale 0.0 - 1.0"""
            array_min, array_max = array.min(), array.max()
            return ((array - array_min)/(array_max - array_min))

        # normalise the bands
        nirn = normalize(nir)
        redn = normalize(red)
        greenn = normalize(green)
        bluen = normalize(blue)
        """#to check values
        print("Normalized bands")
        print(redn.min(), '-', redn.max(), 'mean:', redn.mean())
        print(greenn.min(), '-', greenn.max(), 'mean:', greenn.mean())
        print(bluen.min(), '-', bluen.max(), 'mean:', bluen.mean())
        """
        # Create TCC
        rgb = numpy.dstack((redn, greenn, bluen))
        # Create FCC
        nrg = numpy.dstack((nirn,redn, greenn))
        #print(nrg.shape)

        plt.figure(1)
        plt.imshow(rgb)
        messagebox.showinfo("Information","Please Select reference points on the FCC(figure 2) by double click and close the User Interface and wait")


        #######to read refernce pixel coordinates
        self.ref_count = 0
        plt.figure(2)
        ref_cord = []
        ax = plt.gca()
        fig = plt.gcf()
        implot = ax.imshow(nrg)

        def onclick(event):
            if event.dblclick:      #read data on double click
                if event.xdata != None and event.ydata != None:

                    ref_cord.append([round(event.xdata), round(event.ydata)])
                    self.ref_count
                    self.ref_count=self.ref_count + 1
                    #print(self.ref_count)
                    #print(ref_cord)
                    #print(event.xdata, event.ydata)
        cid = fig.canvas.mpl_connect('button_press_event', onclick)

        plt.show()


        #default palettte made to classsify
        class_color = {0:[0, 0, 255], 1:[255, 0, 0], 2:[0, 255, 0], 3:[255,0,255], 4:[0,200,200],5:[200,200,0], 6:[100,100,0], 7:[250,255,80],8:[200,0,100],10:[0,0,0]}


        with rasterio.open(self.filename, 'r') as ds:
            arr=ds.read()
            ix=max(ds.height,ds.width)
            iy=min(ds.width,ds.height)
            if arr.shape[0] != 4:
                messagebox.showinfo("Error","Input image is not 4 band")



            arr = numpy.array(arr, dtype=numpy.float64)
            #show(arr)
            data=arr.shape
            #print(data)
            #test cases
        """
            print(arr[0,0,0])
            print(arr[1,0,0])
            print(arr[2,0,0])
            print(arr[3,0,0])"""
        #print("_______________")
            #print(arr[0,400,165],)
            #print(arr[2,400,165],)
            #print(arr[3,400,165],)


        #print(arr[0,ref_cord[0][0],ref_cord[0][1]])
        #print(ref_cord)
        #print(arr[0,int(ref_cord[0][0]),int(ref_cord[0][1])])
        #print(arr[0,400,165],)
        #ref_vect is refernce pixel
        ref_vect=[[0 for x in range(4)] for y in range(self.ref_count)]



        for i in range(self.ref_count):
            for j in range(4):
                ref_vect[i][j]=arr[j,int(ref_cord[i][0]),int(ref_cord[i][1])]
                #print(ref_vect)










            #print(data)

        #    print(arr[0,289,313])
        #    print(arr[1,289,313])
        #    print(arr[2,289,313])
        #    print(arr[3,289,313])

        c=numpy.ndarray((ix, iy, 3))
        #clas=numpy.ndarray((ix, iy))
        #    print(angle_between(arr,l))
        #print(arr.shape) #(4, 3925, 3085)

        #print(arr[0,0,0])
        #print(arr[1,0,0])
        #print(arr[2,0,0])
        #print(arr[3,0,0])"""
        p_mag = [0] * self.ref_count

        product_numtr=[0]*self.ref_count

        p_deno = [0]*self.ref_count
        p_ang = [0]*self.ref_count

        p_cos = [0]* self.ref_count
        refv_mag=[0]* self.ref_count
        for i in range(self.ref_count):
            refv_mag[i] = numpy.linalg.norm(ref_vect[i])
            #print(refv_mag[i])




        #temp=[100]
         #band number

        #ctr = 0

        for x in range(ix):
            for y in range(iy):
                #print(p_ang)
                for j in range(self.ref_count):
                    for bn in range(4):


                    #debug code
                    #ctr += 1
                    #

                        product_numtr[j]+=(arr[bn,x,y]*ref_vect[j][bn])
                        #l_numtr+=(arr[bn,x,y]*l[bn])
                        #u_numtr+=(arr[bn,x,y]*u[bn])
                        #b_numtr+=(arr[bn,x,y]*b[bn])
                        p_mag[j]=p_mag[j]+arr[bn,x,y]*arr[bn,x,y]
                        #l_pmag=l_pmag+arr[bn,x,y]*arr[bn,x,y]
                        #u_pmag=u_pmag+arr[bn,x,y]*arr[bn,x,y]
                        #b_pmag=b_pmag+arr[bn,x,y]*arr[bn,x,y]
                    p_deno[j]=(numpy.sqrt(p_mag[j]))
                    #print(product_numtr[j],p_deno[j])
                    #print(p_deno[j])
                    #print(product_numtr[j])
                    p_cos[j]=product_numtr[j]/(p_deno[j]*refv_mag[j])
                    #print("###")
                    #print(p_cos[j])


                    p_ang[j]=numpy.arccos(p_cos[j])
                    #class_no = numpy.argmin(p_ang, axis = 0)
                    #print(p_ang[j])

                    if p_ang[j] < 0.2:
                        class_no = numpy.argmin(p_ang, axis = 0)
                        print(class_no)
                    else:
                        class_no = 10
                        print("10")
                    #back to zero
                    p_mag = [0]* self.ref_count
                    #l_pmag = 0.0
                    #u_pmag = 0.0
                    #b_pmag=0
                    product_numtr=[0] * self.ref_count
                    #u_numtr=0.0
                    #l_numtr=0.0
                    #b_numtr=0

                    #temp=numpy.minmum()
                c[x,y,0]=class_color[class_no][0]   #class_color = {0:[234, 12, 1], 1:[34, 45, 46], 2:[34, 56, 123]}
                c[x,y,1]=class_color[class_no][1]
                #print(class_color[class_no][1])
                c[x,y,2]=class_color[class_no][2]
                #print("CLASS")
                #print(class_no)
                #print(c[x,y,bn-1],c[x,y,bn-2],c[x,y,bn-3])
                #print()
                #print()

                    #dst.write(data)
                   #print(m_ang,l_ang)
        plt.imshow(c)
        plt.show()

        f, axarr = plt.subplots(1,3)
        #plt.legend(["TCC", "FCC", "Classified"], loc=4)
        axarr[0].imshow(rgb)
        axarr[0].set_title('TCC')
        axarr[1].imshow(nrg)
        axarr[1].set_title('FCC')
        axarr[2].imshow(c)
        axarr[2].set_title('Classified')
        plt.show()

if __name__ == '__main__':
    root = Root()
    root.mainloop()

""" TRAIL CLASSES PIXEL
l=[9948,9209,8055,7358]    #LAKE
m=[9747,8956,7904,16434]   #mangroves
u=[13581,14973,17244,20404] #urbanairport
b=[10723,10111,10393,12682] #barreland
"""
