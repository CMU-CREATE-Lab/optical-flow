import sys
from optical_flow import *

def main(argv):
    op = OpticalFlow(rgb_vid_in_p="v1.mp4", rgb_4d_out_p="data/rgb/v1.npy",
            flow_4d_out_p="data/flow/v1.npy", save_img_dir="data/img/v1/",
            flow_threshold=0.75, sat_threshold=0.75, frame_threshold=0.01, flow_type=1)

    op.process()
    op.contains_smoke()
    op.show_flow()

if __name__ == "__main__":
    main(sys.argv)
