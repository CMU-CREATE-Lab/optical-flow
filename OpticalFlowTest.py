from OpticalFlow import *
import json

read = open("optical-flow/Positive Labels.json").read()

positive_data = json.loads(read)


def main():
    frame_thresh_values = {}
    pixel_thresh_values = {}
    test = OpticalFlow()
    pixel_values_array = [70, 80, 90, 100, 110, 120, 130]
    frame_values_array = [0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
    for pixel in pixel_values_array:
        for frame in frame_values_array:
            filtered = 0
            total = 0
            for i in positive_data["data"]:
                test.step(i["url_root"] + i["url_part"])
                if not test.threshold(pixel, frame, 0.3):
                    filtered += 1
                total += 1
            frame_thresh_values[frame] = (
            filtered, total, filtered / total * 100)
            print(frame, filtered / total * 100)
            if filtered / total * 100 > 10:
                break
        pixel_thresh_values[pixel] = frame_thresh_values
        frame_thresh_values = {}
    print(pixel_thresh_values)


print(main())

# Positives = {70: {0.02: (0, 194, 0.0),
#                   0.03: (0, 194, 0.0),
#                   0.04: (0, 194, 0.0),
#                   0.05: (6, 194, 3.0927835051546393),
#                   0.06: (13, 194, 6.701030927835052),
#                   0.07: (23, 194, 11.855670103092782)},
#              80: {0.02: (0, 194, 0.0),
#                   0.03: (2, 194, 1.0309278350515463),
#                   0.04: (6, 194, 3.0927835051546393),
#                   0.05: (14, 194, 7.216494845360824),
#                   0.06: (25, 194, 12.886597938144329)},
#              90: {0.02: (1, 194, 0.5154639175257731),
#                   0.03: (3, 194, 1.5463917525773196),
#                   0.04: (12, 194, 6.185567010309279),
#                   0.05: (22, 194, 11.34020618556701)},
#              100: {0.02: (2, 194, 1.0309278350515463),
#                    0.03: (8, 194, 4.123711340206185),
#                    0.04: (22, 194, 11.34020618556701)},
#              110: {0.02: (3, 194, 1.5463917525773196),
#                    0.03: (17, 194, 8.762886597938143),
#                    0.04: (32, 194, 16.49484536082474)},
#              120: {0.02: (5, 194, 2.5773195876288657),
#                    0.03: (26, 194, 13.402061855670103)},
#              130: {0.02: (13, 194, 6.701030927835052),
#                    0.03: (35, 194, 18.04123711340206)}}
