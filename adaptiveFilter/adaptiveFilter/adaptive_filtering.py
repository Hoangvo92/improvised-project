import numpy as np
import scipy
from scipy import ndimage
import warnings
warnings.simplefilter("ignore")


class adaptive_filtering:
    image = None
    filter = None
    filter_h = None
    filter_w = None
    sizeMax = None
    variance = None
    aWallis = None
    bWallis = None

    def __init__(self, image, adaptive_filter_name, filter_h, filter_w, sizeMax=0, a=0, b = 0):
        """initializes the variables frequency filtering on an input image
        takes as input:
        image: the input image
        filter_name: the name of the mask to use
        cutoff: the cutoff frequency of the filter
        sizeMax: the maximum allowed size of the filter (only for median)
        returns"""
        self.image = image
        self.variance = ndimage.variance(image)
       
        if adaptive_filter_name == 'reduction':
            self.filter = self.get_reduction_filter
        
        elif adaptive_filter_name == 'median':
            self.filter = self.get_median_filter
        elif adaptive_filter_name == 'wallis':
            self.filter = self.get_wallis_filter
        

        self.filter_h = filter_h
        self.filter_w = filter_w
        self.sizeMax = sizeMax
        self.aWallis = a
        self.bWallis = b

    def zero_pad(self, image, pad_h, pad_w):
        """Take input image and size of filter
         return a pad zero image"""
        image_pad = np.pad(image, ((pad_h,pad_h), (pad_w,pad_w)), 'constant', constant_values=0)
        return image_pad

    def get_reduction_filter(self, image_slice, value, filter_h, filter_w, variance):
        """Take inputs as a window image, the intensity, height of filter or window,
            width of filter or window, and global variance of the image
            output the computed intensity of local noise reduction filter"""
        v = variance  # the variance of the image
       
        if v == 0:
            return value
        else:
             vl = ndimage.variance(image_slice) # the local variance of image slice
             m = 1/(filter_h*filter_w) * np.sum(image_slice)  # the mean or average intensity of local pixels in the slice
             
             if variance == vl:
                 return np.uint8(m)
             elif int(vl) == 0:
                 return value  #if local variance ->0 => all pixels have the same intensity=> value= mean=> keep the original value
             else:
                 return np.uint8(value - v/vl*(value - m)) #compute the value of reduced intensity
            
    def get_wallis_filter(self, image_slice, sxy, mf, sf, a, b):
        mk = np.mean(image_slice)
        sk = np.std(image_slice)
        if a==1 and b==1:
            if sk==0:
                return sxy
            else:
                return np.uint8((sxy-mk)*sf/sk +mf)
        else:
            alpha = a*sf/(a*sk + (1-a)*sf)
            beta = b*mf + (1-b)*mk
            return np.uint8((sxy-mk)*alpha + beta)

    def get_median_filter(self, image_slice, zxy, filter_h, filter_w, max):
         """Take the inputs: image slice, the intensity at h and w, the height of filter, the width of filter, sizemax
        return the value of adaptive median filter"""
         
         a = int(1/2*(max-filter_h))
         b = int(1/2*(max-filter_w))
        
         a1 = int(1/2*(max+filter_h)) 
         b1 = int(1/2*(max+filter_w))
         windowS = image_slice[a:a1 , b:b1]
        
         try:
             zmed= np.median(windowS)
             
         except ValueError: #raise if zero-size array is empty
             zmed = zxy
             
         try:
             zmin = np.min(windowS)
         except ValueError:  #raise if zero-size array is empty
             zmin =  zxy
         try:
             zmax = np.max(windowS)
         except ValueError:
             zmax = zxy
        
             #stage A 
         if zmed>zmin and zmed<zmax:
             #stage B
             if zxy>zmin and zxy<zmax:
                 return zxy
             else:
                 return zmed
                 
         else:
                  
             if (filter_h + 2)> max or (filter_w+ 2)> max:
                 return zmed
             else:
                 return self.get_median_filter(image_slice, zxy, filter_h+2, filter_w+2, max)
  
         
   

    

    def full_contrast_stretch(self, image):
        """Create a full contrast stretch of the image
        input: image
        return an image with full contrast stretch
        """
        min_pixel = np.min(image)
        max_pixel = np.max(image)
        image = np.uint8(255 / (max_pixel - min_pixel) * (image - min_pixel) + 0.5)

        return image

    def filtering(self):
        

        height, width = self.image.shape
        
        image_filtered = np.zeros(shape=(height, width))
        
        
        if self.filter == self.get_reduction_filter: 
            pad_h = int(1/2 * (self.filter_h - 1))
            pad_w = int(1/2 * (self.filter_w - 1))
            image_pad = self.zero_pad(self.image, pad_h, pad_w) #self.image
            for h in range(height):
                for w in range(width):
   
                    vert_start = h
                    vert_end = h + self.filter_h
                    horiz_start = w
                    horiz_end = w + self.filter_w
                    image_slice = image_pad[vert_start:vert_end, horiz_start:horiz_end]
                    image_filtered[h, w] = self.get_reduction_filter(image_slice, self.image[h,w], self.filter_h, self.filter_w, self.variance)
        elif self.filter ==self.get_wallis_filter:
             pad_h = int(1/2 * (self.filter_h - 1))
             pad_w = int(1/2 * (self.filter_w - 1))
             image_pad = self.zero_pad(self.image, pad_h, pad_w)
             mf = np.mean(self.image)
             sf = np.std(self.image)
             for h in range(height):
                for w in range(width):
                    
                    
                    vert_start = h
                    vert_end = h + self.filter_h
                    horiz_start = w
                    horiz_end = w + self.filter_w
                    image_slice = image_pad[vert_start:vert_end, horiz_start:horiz_end]
                    image_filtered[h, w] = self.get_wallis_filter(image_slice, self.image[h,w], mf, sf, self.aWallis, self.bWallis)
        else:
            maxN = int(1/2*(self.sizeMax -1))
            max_pad = self.zero_pad(self.image, maxN, maxN)
            begin = int (self.sizeMax -np.floor(self.sizeMax/2))
            for h in range(height):
                for w in range( width):
                    vert_start = h
                    vert_end = h + self.sizeMax
                    horiz_start = w
                    horiz_end = w + self.sizeMax
                    image_slice =  max_pad[vert_start:vert_end, horiz_start:horiz_end]
                 
                    value = self.image[h,w]
                    image_filtered[h, w] = self.get_median_filter(image_slice, value, self.filter_h, self.filter_w, self.sizeMax)
       
        image_filtered = self.full_contrast_stretch(image_filtered)
        return image_filtered



