from OpticalFlow import *
import requests
import json


def main():
    frame_thresh_values = {}
    pixel_thresh_values = {}
    test = OpticalFlow()
    pixel_values_array = [70, 80, 90, 100, 110, 120, 130]
    frame_values_array = [0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
    for page in ['1', '2', '3', '4']:
        url = 'http://api.smoke.createlab.org/api/v1/get_pos_labels_by_researcher?&pageSize=1000'

        params = {'pageSize': '1000', 'pageNumber':page}

        response = requests.get(url=url, params=params)
        videos = json.loads(response.text)
        for pixel in pixel_values_array:
            for frame in frame_values_array:
                filtered = 0
                total = 0
                for i in videos["data"]:
                    test.step(i["url_root"] + i["url_part"])
                    if not test.threshold(pixel, frame, 0.3):
                        filtered += 1
                    total += 1
                    print("  " + str(i['id']))
                frame_thresh_values[frame] = (filtered, total, filtered / total * 100)
                print(frame, filtered / total * 100)
            pixel_thresh_values[pixel] = frame_thresh_values
            frame_thresh_values = {}
        print(pixel_thresh_values)


print(main())


