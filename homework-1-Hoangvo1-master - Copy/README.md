# Digital Image Processing 
Assignment #1

Due: Thur 9/13/18 11:59 PM

1. Resampling:

(8 pts.) Write code for zooming and shrinking an image using the nearest neighbor and bilinear interpolation. The input to your program is: (i) image, (ii) transformation parameters, and (iii) interpolation method.
 
  - Starter code available in directory resize/      
  - resize/resample.py: One is required to edit the functions "nearest_neighbor" and "bilinear", you are welcome to add more       function. Do not edit the function "resize"
  - resize/interpolation.py: Write code for linear and bilinear interpolation in there respective function definitions, you are welcome to write new functions and call them from these functions
  - Describe your method and findings in the report.md file
  - This part of the assignment can be run using dip_hw1_resize.py (there is no need to edit this file)
  - Usage: ./dip_hw1_resize.py -i image-name -fx scalex -fy scaley -m method                   
       - image-name: name of the image
       - scalex, scaley: scale to resize the image (eg. fx 0.5, fy 0.5 to make it half the original size)
       - method: "nearest_neightbor" or "bilinear" 
  - Example: - ./dip_hw1_resize.py -i cell2.jpg -fx 0.75 -fy 0.75 -m nearest_neighbor
             - or 
             - python dip_hw1_resize.py -i cell2.jpg -fx 0.75 -fy 0.75 -m nearest_neighbor
  - Please make sure your code runs when you run the above command from prompt/Terminal
  - Any output images or files must be saved to "output/" folder
  
----------------------
2. (2 Pts.) Describe your method and report you findings in report.md for each problem of the assignemnt.

----------------------
Two images are provided for testing: cells.png and cell2.jpg
  
PS. Files not to be changed: requirements.txt and .circleci directory 

If you do not like the structure, you are welcome to change the over all code, under two stipulations:

1. the code has to run using command

 - ./dip_hw1_resize.py -i image-name -fx scalex -fy scaley -m method
 - or
 - python dip_hw1_resize.py -i image-name -fx scalex -fy scaley -m method
  
2. Any output file or image should be written to output/ folder

The TA will only be able to see your results if these two conditions are met

1. Resampling      - 8 Pts
3. Report          - 2 Pts

    Total          - 10 Pts.

----------------------
