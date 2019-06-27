import os
import cv2 as cv
import numpy as np
import matplotlib
#matplotlib.use("PS") # a fix for Mac OS X error
from matplotlib import pyplot as plt

class OpticalFlow(object):
    # Use this function to initialize parameters
    # Input:
    #   rgb_vid_in_p (str):
    #       input path of rgb video
    #   rgb_4d_out_p (str):
    #       output path of the 4d rgb array
    #   flow_4d_out_p (str):
    #       output path of the 4d optical flow array
    #   save_img_dir (str):
    #       directory to save rgb and flow images
    #   flow_threshold (int):
    #       pixel threshold for optical flow array (range 0 to 255)
    #   sat_threshold (int):
    #       pixel threshold for saturation (range 0 to 255)
    #   frame_threshold (float):
    #       percentage of frame thresholded for acceptable smoke candidacy (range 0 to 1):
    #       e.g. if a frame is thresholdeded and 2% of the pixels are left on (set to 1)
    #       that would be a frame percentage of 0.02
    #   flow_type (int; 1 or 2):
    #       method for computing optical flow (1 = Farneback method, 2 = TVL1 method)
    #   desired_frames (float):
    #       percentage of frames to check when thresholding (range 0 to 1)
    #       e.g. if set to .3 checks the 30% of the frames that have the highest
    #       frame percentage for being higher than the frame_threshold value
    #   record_hsv (bool):
    #       convert flow frames to images for detection or not
    #       set this flag to False to increase speed
    def __init__(self, rgb_vid_in_p=None, rgb_4d_out_p=None, flow_4d_out_p=None,
                 save_img_dir=None, flow_threshold=255, sat_threshold=255,
                 frame_threshold=1, flow_type=1, desired_frames=1, record_hsv=False):
        self.rgb_vid_in_p = rgb_vid_in_p
        self.rgb_4d_out_p = rgb_4d_out_p
        self.check_and_create_dir(rgb_4d_out_p)
        self.flow_4d_out_p = flow_4d_out_p
        self.check_and_create_dir(flow_4d_out_p)
        self.save_img_dir = save_img_dir
        self.check_and_create_dir(save_img_dir)
        self.flow_threshold = flow_threshold
        self.sat_threshold = sat_threshold
        self.frame_threshold = frame_threshold
        self.flow_type = flow_type
        self.desired_frames = desired_frames
        self.record_hsv = record_hsv

        self.thresh_4d = None
        self.fin_hsv_array = None
        self.rgb_4d = None
        self.rgb_filtered = None

    # Compute optical flow frame from a 4d array of rgb frames
    # Input:
    #   a 4D numpy.array of rgb frames (range 0 to 255)
    #   dimensions: (time, height, width, channel)
    #   channel 0, 1, and 2 means R, G, and B respectively
    # Output:
    #   a 4D numpy.arrazy of optical flow frams (range 0 to 255)
    #   dimension: (time, height, width, channel)
    #   channel 0 and 1 means flow_x and flow_y respectively
    def rgb_to_flow(self, rgb_4d=None):
        length, height, width = rgb_4d.shape[0], rgb_4d.shape[1], rgb_4d.shape[2]
        rgb_4d = np.uint8(rgb_4d) # in the range of 0 to 255
        flow_4d = np.zeros((length, height, width, 2)) # need np.float64
        previous_frame = rgb_4d[0, :, :, :]
        previous_gray = cv.cvtColor(previous_frame, cv.COLOR_RGB2GRAY)
        count = 0
        if self.record_hsv or self.save_img_dir is not None:
            self.fin_hsv_array = np.zeros((length, height, width, 2)) # need np.float64
            hsv_img = np.zeros_like(previous_frame, dtype=np.float64) # need np.float64
            hsv_img[..., 1] = 1
        for current_frame in rgb_4d:
            current_gray = cv.cvtColor(current_frame, cv.COLOR_BGR2GRAY)
            if self.flow_type == 1:
                flow = cv.calcOpticalFlowFarneback(previous_gray, current_gray, None, 0.5, 3, 15, 3, 5, 1.2, 2)
            elif self.flow_type == 2:
                optical_flow = cv.optflow.DualTVL1OpticalFlow_create()
                flow = optical_flow.calc(previous_gray, current_gray, None)
            flow_x = self.clip_and_scale_flow(flow[..., 0])
            flow_y = self.clip_and_scale_flow(flow[..., 1])
            flow_4d[..., 0] = flow_x
            flow_4d[..., 1] = flow_y
            if self.record_hsv or self.save_img_dir is not None:
                magnitude, angle = cv.cartToPolar(flow_x / 255, flow_y / 255, angleInDegrees=True)
                hsv_img[..., 0] = angle # channel 0 represents direction
                hsv_img[..., 2] = magnitude # channel 2 represents magnitude
                self.fin_hsv_array[count, :, :, :] = hsv_img[:, :, [0, 2]]
                if self.save_img_dir is not None:
                    hsv_img = hsv_img.astype(np.float32)
                    cv.imwrite(self.save_img_dir + 'hsv-%d.jpg' % count, cv.cvtColor(hsv_img, cv.COLOR_HSV2RGB))
                    cv.imwrite(self.save_img_dir + 'rgb-%d.jpg' % count, current_frame)
            previous_frame = current_frame
            count += 1
        cv.destroyAllWindows()
        return flow_4d

    # Scale the input flow to range (0,1) with bi-bound
    # Input:
    #   raw_flow: input raw pixel value (not in 0-255)
    #   bound: upper and lower bound (-bound, bound)
    # Output:
    #   pixel value scale from 0 to 1
    def clip_and_scale_flow(self, raw_flow, bound=20):
        flow = raw_flow
        flow[flow > bound] = bound
        flow[flow < -bound] = -bound
        flow -= -bound
        flow *= 255 / float(2*bound)
        return flow

    # Process an encoded video (h.264 mp4 format) into a 4D array of rgb frames
    # Output:
    #   4D array in rgb format (time, height, width, channel)
    #   range 0 to 255
    def vid_to_frames(self):
        capture = cv.VideoCapture(self.rgb_vid_in_p)
        ret, previous_frame = capture.read()

        height = np.size(previous_frame, 0)
        width = np.size(previous_frame, 1)
        length = int(capture.get(cv.CAP_PROP_FRAME_COUNT))
        rgb_4d = np.zeros((length, height, width, 3))

        if length <= 1:
            return None

        for i in range(length):
            rgb_4d[i, :, :, :] = cv.cvtColor(previous_frame, cv.COLOR_BGR2RGB)
            ret, current_frame = capture.read()
            previous_frame = current_frame
        capture.release()

        return rgb_4d

    # Read a video clip and save processed frames to disk (range 0 to 255)
    # Saved:
    #   4d array of rgb frames in format (time, height, width, channel)
    #   4d array of optical flow frames in format (time, height, width, channel)
    def process(self):
        print("Process video from %s" % self.rgb_vid_in_p)
        if self.rgb_vid_in_p == None:
            return None
        rgb_4d = self.vid_to_frames()
        self.rgb_4d = np.copy(rgb_4d)
        self.rgb_filtered = np.copy(rgb_4d)
        flow_4d = self.rgb_to_flow(rgb_4d)

        # Save rgb_4d to path rgb_4d_out_p
        if self.rgb_4d_out_p != None:
            np.save(self.rgb_4d_out_p, np.uint8(rgb_4d))
            print("raw rgb frames saved to %s" % self.rgb_4d_out_p)

        # Save flow_4d to path flow_4d_out_p
        if self.flow_4d_out_p != None:
            np.save(self.flow_4d_out_p, np.uint8(flow_4d))
            print("raw flow frames saved to %s" % self.flow_4d_out_p)

    # Determine whether or not a particular video has significant movement using
    # Optical flow and saturation filtering methods
    # Input:
    #   flow_threshold (int): pixel threshold for optical flow array (range 0 to 255)
    #   saturation_threshold (int): pixel threshold for saturation (range 0 to 255)
    #   frame_threshold (float): percentage of frame thresholded for acceptable smoke candidacy (range 0 to 1):
    #   desired_frames (float): percentage of frames to check when thresholding (range 0 to 1)
    # Output:
    #   Boolean (True --> significant smoke movement; False --> no significant smoke movement)
    def threshold(self, flow_threshold, saturation_threshold, frame_threshold, desired_frames):
        # print("determining video threshold")
        if type(self.fin_hsv_array) != np.ndarray:
            return None
        num_frames = int(np.shape(self.fin_hsv_array)[0]*desired_frames)
        acceptable_per_frame = []
        self.thresh_4d = np.copy(self.fin_hsv_array)
        frame = 0
        for hsv in self.fin_hsv_array:
            bin_img = self.optical_flow_threshold(flow_threshold, frame, hsv)
            self.saturation_threshold(saturation_threshold, acceptable_per_frame, frame, bin_img)
            frame += 1
        if desired_frames < 1:
            acceptable_per_frame.sort()
            sub_s = acceptable_per_frame[-num_frames:]
            print(sub_s)
            for i in sub_s:
                if i > frame_threshold:
                    print("acceptable")
                    return True
            print("no smoke detected")
            return False
        for i in acceptable_per_frame:
            if i > frame_threshold:
                return True
        return False

    # Thresholds whether or not optical flow frame pixels are above threshold
    # Input:
    #   flow_threshold (int): pixel threshold for optical flow array (range 0 to 255)
    #   frame (int): frame (index) being considered in optical flow array
    #   hsv (numpy.array): optical flow video frame to be thresholded
    # Output:
    #   numpy array containing thresholded optical flow
    #   pixels above threshold == 1; pixels below threshold == 0
    def optical_flow_threshold(self, flow_threshold, frame, hsv):
        self.thresh_4d[frame,:,:,:] = np.copy(hsv[:, :, :])
        bin_img = 1.0 * (self.thresh_4d[frame,:,:,1] > flow_threshold)
        return bin_img

    # Thresholds whether or not rgb pixels are above saturation threshold
    #   NOTE: should usually be called after optical_flow_threshold)
    # Input:
    #   saturation_threshold (int): pixel threshold for saturation (range 0 to 255)
    #   acceptable_per_frame (list): list to be filled with percentages of each frame left on
    #       e.g. if a video had three frames and after being thresholded they were determined to
    #       have 30% acceptable movement, 25%, 10%, 18%, and 12%,
    #       acceptable_per_frame would be [.3, .25, .1, .18, .12] after execution
    #   frame (int): frame (index) being considered in rgb array
    #   bin_img (numpy.array): array containing thresholded optical flow pixels
    # Output:
    #   numpy array containing thresholded optical flow
    #   pixels above threshold == 1; pixels below threshold == 0
    def saturation_threshold(self, saturation_threshold, acceptable_per_frame, frame, bin_img):
        rgb = self.rgb_filtered[frame, :, :, :]
        hsv = np.copy(rgb).astype(np.uint8)
        hsv = cv.cvtColor(hsv, cv.COLOR_RGB2HSV)
        saturation = hsv[:, :, 1]
        saturation = 1.0 * np.where(saturation < saturation_threshold, 0, saturation)
        saturation = 1.0 * np.where(bin_img == 0, 0, saturation)
        zeros = np.zeros_like(saturation)

        bin_img = np.where(saturation == 0, 0, bin_img)

        bin_img_shape = np.shape(bin_img)
        acceptable_per_frame.append(np.sum(bin_img[:]) / (bin_img_shape[0] * bin_img_shape[1]))
        self.thresh_4d[frame, :, :, 1] = bin_img

        self.rgb_filtered[frame, :, :, 0] = zeros
        self.rgb_filtered[frame, :, :, 1] = saturation
        self.rgb_filtered[frame, :, :, 2] = zeros

    # Wrapper function for determining whether or not a given video is likely to
    # contain smoke based on constructor initilized values
    def contains_smoke(self):
        return self.threshold(self.flow_threshold, self.sat_threshold, self.frame_threshold, self.desired_frames)

    # Function to visualize smoke determination
    # Videos:
    #   thresh - video after optical flow and saturation thresholding
    #   hsv - optical flow computed before filtering
    #   rgb - original rgb video
    #   filt - video after saturation filtering and thresholding
    def show_flow(self):
        for i in range(np.shape(self.rgb_4d)[0]):
            plt.subplot(141), plt.imshow(self.thresh_4d[i,:,:,1]), plt.title('thresh')
            plt.subplot(142), plt.imshow(self.fin_hsv_array[i,:,:,1].astype(np.uint8)), plt.title('hsv')
            plt.subplot(143), plt.imshow(self.rgb_4d[i, ...].astype(np.uint8)), plt.title('rgb')
            plt.subplot(144), plt.imshow(self.rgb_filtered[i, ...].astype(np.uint8)), plt.title('filt')
            plt.figure()
            plt.draw()
            plt.pause(0.001)

    # Check if a directory exists, if not, create it
    def check_and_create_dir(self, path):
        if path is None: return
        dir_name = os.path.dirname(path)
        if dir_name != "" and not os.path.exists(dir_name):
            os.makedirs(dir_name)
