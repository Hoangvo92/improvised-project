import numpy as np
import cv2
import math
from resize import interpolation


class resample:
    def resize(self, image, fx=None, fy=None, interpolation=None):
        """calls the appropriate funciton to resample an image based on the interpolation method
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        interpolation: method used for interpolation ('either bilinear or nearest_neighbor)
        returns a resized image based on the interpolation method
        """
        if interpolation == 'bilinear':
            return self.bilinear_interpolation(image, float(fx), float(fy))

        elif interpolation == 'nearest_neighbor':
            return self.nearest_neighbor(image, float(fx), float(fy))

    def nearest_neighbor(self, image, fx, fy):
        """resizes an image using bilinear interpolation approximation for resampling
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        returns a resized image based on the nearest neighbor interpolation method
        """

        # Write your code for nearest neighbor interpolation here
        shape=image.shape
        print(shape)
        numro, numco = image.shape
        numro=math.ceil(numro*fx)
        numco=math.ceil(numco*fy)
        image1= np.zeros((numro, numco), np.uint8)
        
        for rowX in range(image1.shape[0]):
            for colY in range(image1.shape[1]):
                #(newX,newY)=image.nearestneighbor(i,j)
                newx = rowX/fx
                newy = colY/fy
                newx1 = math.floor(newx)
                if newx1 >= image.shape[0]:
                    newx1 = image.shape[0]-1
                newy1 = math.floor(newy)
                if newy1 >= image.shape[1]:
                    newy1= image.shape[1]-1
                newx2 = math.ceil(newx)
                if newx2 >= image.shape[0]:
                    newx2 = image.shape[0]-1
                               
                pt1= (newx1, newy1, image[newx1, newy1])
                pt2= (newx2, newy1, image[newx2, newy1])
                unknown= (newx, newy)
                operator= interpolation.interpolation()
                image1[rowX,colY]= operator.linear_interpolation( pt1, pt2, unknown)
        
        return image1

    def bilinear_interpolation(self, image, fx, fy):
        """resizes an image using bilinear interpolation approximation for resampling
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        returns a resized image based on the bilinear interpolation method
        """

        # Write your code for bilinear interpolation here
        shape=image.shape
        print(shape)
        numro, numco = image.shape
        numro=math.ceil(numro*fx)
        numco=math.ceil(numco*fy)
        image1= np.zeros((numro, numco), np.uint8)
        for rowX in range(image1.shape[0]):
            for colY in range(image1.shape[1]):
                #(N1,N2,N3,N4)=image.nearestneighbor4(i,j)
                newx=rowX/fx
                newy=colY/fy
                newx1=math.floor(newx)
                if newx1 >= image.shape[0]:
                    newx1= image.shape[0]-1
                newy1=math.floor(newy)
                if newy1 >= image.shape[1]:
                    newy1= image.shape[1]-1
                newx2=math.ceil(newx)
                if newx2 >= image.shape[0]:
                    newx2 = image.shape[0]-1
                newy2=math.ceil(newy)
                if newy2 >= image.shape[1]:
                    newy2= image.shape[1]-1
                    
                N1= (newx1, newy1, image[newx1, newy1])
                N2= (newx1, newy2, image[newx1, newy2])
                N3= (newx2, newy1, image[newx2, newy1])
                N4= (newx2, newy2, image[newx2, newy2])
                unknown = (newx, newy)
                operator= interpolation.interpolation()
                #imageChange[rowX,colY]= intensity.bilinear_interpolation(N1,N2,N3, N4, unknown)
                image1[rowX,colY]= operator.bilinear_interpolation( N1,N2,N3, N4, unknown)
        
        return image1