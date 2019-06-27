import sys
from optical_flow import *

def main(argv):
    op = OpticalFlow(rgb_vid_in_p="test.mp4", rgb_4d_out_p="data/rgb/test.npy",
            flow_4d_out_p="data/flow/test.npy", save_img_dir="data/img/")
    op.process()

if __name__ == "__main__":
    main(sys.argv)
