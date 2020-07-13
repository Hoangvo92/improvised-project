"""adaptiveFilter_main.py: Star file to run mean_filter"""

# Example Usage: -i image -f filter -r filter_h -c filter_w -s sizeMax -n noise

__author__ = "Hoang Vo"
__email__ = "hdvo9@uh.edu"
__version__ = "1.0.0"

import cv2
import sys
import numpy as np
from adaptive_filtering import adaptive_filtering
from datetime import datetime
import skimage
np.random.seed(1)


def main():
    """ The main function that parses input argument, calls the approciate
    filtering method and writes the output image"""

    # Parse input arguments
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument("-i", "--image", dest="image",
                        help="specify the name of the image", metavar="IMAGE")
    parser.add_argument("-f", "--adaptive_filter", dest="adaptive_filter",
                        help="specify name of the adaptive filter(median, reduction)", metavar="ADAPTIVE FILTER")
    parser.add_argument("-r", "--filter_h", dest="filter_h",
                        help="specify the height of filter", metavar="FILTER HEIGHT")
    parser.add_argument("-c", "--filter_w", dest="filter_w",
                        help="specify the width of filter", metavar="FILTER WIDTH")
    parser.add_argument("-s", "--sizeMax", dest="sizeMax",
                        help="specify the sizeMax for adaptive median filter", metavar="MAX SIZE")
    parser.add_argument("-n", "--noise_type", dest="noise_type",
                        help="specify the type of noise", metavar="NOISE TYPE")
    parser.add_argument("-w1", "--aWallis", dest="aWallis",
                        help="specify the expansion coefficient  for Wallis filter", metavar="EXPANSION COEFFICIENT")
    parser.add_argument("-w2", "--bWallis", dest="bWallis",
                        help="specify the luminance coefficient  for Wallis filter", metavar="LUMINANCE COEFFICIENT")
    
    args = parser.parse_args()

    # Load image
    if args.image is None:
        print("Please specify the name of image")
        print("use the -h option to see usage information")
        sys.exit(2)
    else:
        image_name = args.image.split(".")[0]
        input_image = cv2.imread(args.image, 0)

        output_dir = 'image_with_noise/'
        output_image_name = output_dir + image_name + "_grey" + ".jpg"
        cv2.imwrite(output_image_name, input_image)

    # Check filtering parameters
    if args.adaptive_filter is None:
        print("adaptive filter not specified using default (reduction)")
        print("use the -h option to see usage information")
        adaptive_filter = 'reduction'
    elif args.adaptive_filter not in ['reduction', 'median', 'wallis']:
        print("Unknown order statistic filter, using default (reduction)")
        print("use the -h option to see usage information")
        adaptive_filter = 'reduction'
    else:
        adaptive_filter = args.adaptive_filter

    if args.filter_h is None:
        print("Filter height not specified using default (5)")
        print("use the -h option to see usage information")
        filter_h = 5
    else:
        filter_h = int(args.filter_h)

    if args.filter_w is None:
        print("Filter width not specified using default (5)")
        print("use the -h option to see usage information")
        filter_w = 5
    else:
        filter_w = int(args.filter_w)

    if args.noise_type is None:
        print("Noise type not specified using default (gaussian)")
        print("use the -h option to see usage information")
        noise_type = 'gaussian'
    elif args.noise_type not in ['gaussian', 'salt', 'pepper','rayleigh']:
        print("Unknown noise, using default (gaussian)")
        print("use the -h option to see usage information")
        noise_type = 'gaussian'
    else:
        noise_type = args.noise_type
   
   

    if adaptive_filter in ['median']:
        if args.sizeMax is None:
            print("Maximum allowed size of adaptive median filter not specified, using default (filtersize+6)")
            print("use the -h option to see usage information")
            sizeMax = max(filter_w,filter_h) + 6
        else:
            sizeMax = int(args.sizeMax)
            if sizeMax < filter_w or sizeMax<filter_h:
                print("Maximum allowed size of adaptive median filter is less than input filter-size")
                print("use the -h option to see usage information")
                sizeMax = max(filter_w,filter_h) + 6
    if adaptive_filter in ['wallis']:
         if args.aWallis is None:
             print("Expansion coefficient not specified using defaut 1")
             print("Use the -h option to see usage information")
             aWallis = 1
  
         else:
             aWallis = args.aWallis
             if float(aWallis)<0 or float(aWallis)>1:
                 print("Unknown expansion coefficient, using default 1")
                 print("Use the -h option to see usage information")
                 aWallis = 1

         if args.bWallis is None:
             print("Luminance coefficient not specified using defaut 1")
             print("Use the -h option to see usage information")
             bWallis = 1
    
         else:
             bWallis = args.bWallis
             if float(bWallis)<0 or float(bWallis)>1:
                 print("Unknown luminance coefficient, using default 1")
                 print("Use the -h option to see usage information")
                 bWallis = 1

    # Add noise(mean, variance)
    rows, cols = input_image.shape
    # skimage.util.random_noise(input_image, mode='gaussian', mean=0, var=50, seed=None, clip=True)
    if noise_type == 'gaussian':
        noise_gaussian = np.random.normal(0, 10, (rows, cols))
        input_image.astype("float")
        noise_gaussian.astype("float")
        input_image = input_image + noise_gaussian
        input_image = np.uint8(np.where(input_image < 0, 0, np.where(input_image > 255, 255, input_image)))

    elif noise_type == 'salt':
        noise_salt = np.random.randint(0, 256, (rows, cols))
        prob = 0.2
        noise_salt = np.where(noise_salt < prob * 256, 255, 0)
        input_image.astype("float")
        noise_salt.astype("float")
        input_image = input_image + noise_salt
        input_image = np.uint8(np.where(input_image > 255, 255, input_image))

    elif noise_type == 'pepper':
        noise_pepper = np.random.randint(0, 256, (rows, cols))
        prob = 0.1
        noise_pepper = np.where(noise_pepper < prob * 256, -255, 0)
        input_image.astype("float")
        noise_pepper.astype("float")
        input_image = input_image + noise_pepper
        input_image = np.uint8(np.where(input_image < 0, 0, input_image))

    elif noise_type == 'rayleigh':
        a = -19    # mean=a+sqrt(pi*b/4)=0, variance=b*(4-pi)/4=pow(20,2), a=-38, b=1864
        b = 466   # mean=0, variance=10, a=-19, b=466
        noise_rayleigh = a + np.power((-b * np.log(1 - np.random.rand(rows, cols))), 0.5)
        input_image = input_image + noise_rayleigh
        input_image = np.uint8(np.where(input_image < 0, 0, np.where(input_image > 255, 255, input_image)))

    output_dir = 'image_with_noise/'
    output_image_name = output_dir + image_name + '_' + noise_type + '_noise' + ".jpg"
    cv2.imwrite(output_image_name, input_image)

    output = None
    if adaptive_filter in ['reduction']:
        Filter_obj = adaptive_filtering(input_image, adaptive_filter, filter_h, filter_w)
        output = Filter_obj.filtering()
    elif adaptive_filter in ['Wallis']:
        Filter_obj = adaptive_filtering(input_image, adaptive_filter, filter_h, filter_w, aWallis, bWallis)
        output = Filter_obj.filtering()
    elif adaptive_filter in ['median']:
        Filter_obj = adaptive_filtering(input_image, adaptive_filter, filter_h, filter_w, sizeMax)
        output = Filter_obj.filtering()

    # Write output file
    output_dir = 'output/'

    output_image_name = output_dir+image_name+"_"+adaptive_filter+datetime.now().strftime("%m%d-%H%M%S")+".jpg"
    cv2.imwrite(output_image_name, output)


if __name__ == "__main__":
    main()

