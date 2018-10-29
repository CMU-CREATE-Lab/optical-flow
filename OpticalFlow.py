import cv2
import numpy as np

class OpticalFlow(object):
    
    # Use this function to initialize parameters 
    def __init__(self):
        # self.your_variable = []
        pass

    # Compute optical flow images from a batch of rgb images
    # Read rgb images and save the output hsv optical flow images to disk
    # For the output hsv image, optical direction and length are coded by hue and saturation respectively
    # Input: a 4D raw image array in rgb color (width, height, rgb channel, time)
    # Ouput: a 4D optical flow image array in hsv color (width, height, hsv channel, time)
    # IMPORTANT: you need to handle edge cases, such as only one input images
    def batchOpticalFlow(self, rgb_4d):
        # Process rgb_imgs into optical flow images
        # Return optical flow images
        pass
    
    # Process an encoded video (h.264 mp4 format) into a 4D rgb image array
    # Input: path to a video clip
    # Output: a 4D image array in rgb color (width, height, rgb channel, time)
    def vidToImgs(self, rgb_vid_path):
        # Read the video from rgb_vid_path
        # Process the video into a 4D rgb image aray
        # Return the 4D rgb image array
        pass

    # Read a video clip and save processed image arrays to disk
    # Input:
    # - path for reading the video clip
    # - path for saving the 4D rgb image array (raw images)
    # - path for saving the 4D hsv image array (optical flow)
    def step(self, rgb_vid_in_p, rgb_4d_out_p, op_4d_out_p):
        # rgb_4d = self.vidToImgs(rgb_vid_in_p)
        # op_4d = self.batchOpticalFlow(rgb_4d)
        # Save rgb_4d to path rgb_4d_out_p
        # Save op_4d to path op_4d_out_p
        pass
