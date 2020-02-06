#!/usr/bin/env python3"
# File Name: example_16-01.py
# Author: wkangk
# Mail: wangkangchn@163.com
# Created Time: 2020-01-30 13:19:45 中国标准时间
#
"""
    Example 16-1. Pyramid L-K optical flow
"""
import cv2 as cv

MAX_CORNERS = 1000

def help(args):
    print( "\nExample 16-1: Pyramid L-K optical flow example.\n" )
    print( "Call: " + args[0] + " [image1] [image2]\n" )
    print( "Example:\n" + args[0] + " ../example_16-01-imgA.png ../example_16-01-imgB.png\n" )
    print( "Demonstrates Pyramid Lucas-Kanade optical flow.\n" )

def _main(args):
    if len(args) != 3:
        help(args)
        sys.exit(0)

    # Initialize, load two images from the file system, and
    # allocate the images and other structures we will need for
    # results.
    #
    imgA = cv.imread(args[1], 0)
    imgB = cv.imread(args[2], 0)
    img_sz = imgA.shape[::-1]

    win_size = 10
    imgC = cv.imread(args[2], 0)

    # The first thing we need to do is get the features
    # we want to track.
    # 创建好的特征点进行追踪
    #
    MAX_CORNERS = 500
    cornersA = cv.goodFeaturesToTrack(
        imgA,                         # Image to track
        MAX_CORNERS,                  # Keep up to this many corners
        0.01,                         # Quality level (percent of maximum)
        5,                            # Min distance between corners
        blockSize=3,                  # Block size
        useHarrisDetector=False,                        # true: Harris, False: Shi-Tomasi
        k=0.04                          # method specific parameter
    )
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 50, 0.001)
    cornersA = cv.cornerSubPix(
        imgA,                           # Input image
        cornersA,                       # Vector of corners (input and output)
        (win_size, win_size),   # Half side length of search window
        (-1, -1),               # Half side length of dead zone (-1=none)
        criteria
    )

    # Call the Lucas Kanade algorithm
    #
    cornersB, features_found, _ = cv.calcOpticalFlowPyrLK(
        imgA,                         # Previous image
        imgB,                         # Next image
        cornersA,                     # Previous set of corners (from imgA)
        None,
        winSize=(win_size*2+1, win_size*2+1),  # Search window size
        maxLevel=5,                            # Maximum pyramid level to construct
        criteria=criteria
        )

    # Now make some image of what we are looking at:
    # Note that if you want to track cornersB further, i.e.
    # pass them as input to the next calcOpticalFlowPyrLK,
    # you would need to "compress" the vector, i.e., exclude points for which
    # features_found[i] == False.
    for i in range(len(cornersA)):
        if not features_found[i]:
            continue

        cv.line(
            imgC,                        # Draw onto this image
            tuple(cornersA[i][0]),                 # Starting here
            tuple(cornersB[i][0]),                 # Ending here
            (0, 255, 0),                # This color
            1,                           # This many pixels wide
            cv.LINE_AA                  # Draw line in this style
        )

    cv.imshow("ImageA", imgA)
    cv.imshow("ImageB", imgB)
    cv.imshow("LK Optical Flow Example", imgC)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(_main(sys.argv))
