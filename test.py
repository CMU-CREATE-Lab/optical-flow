#This is a commit test ~ Sean
import sys
from OpticalFlow import OpticalFlow

def main(argv):
    flow = OpticalFlow()

    in_vid_dir = "/workspace/data/videos/"
    out_raw_img_dir = "/workspace/data/images/raw/"
    out_flow_img_dir = "/workspace/data/images/flow/"
    in_vid_name = "test"

    rgb_vid_in_p = in_vid_dir + in_vid_name + ".mp4"
    rgb_4d_out_p = out_raw_img_dir + in_vid_name + ".npy"
    flow_4d_out_p = out_flow_img_dir + in_vid_name + ".npy"
    
    flow.step(rgb_vid_in_p=rgb_vid_in_p, rgb_4d_out_p=rgb_4d_out_p, flow_4d_out_p=flow_4d_out_p)

if __name__ == "__main__":
    main(sys.argv) 
