#define DLLEXPORT extern "C" __declspec(dllexport)

#include "opencv2/opencv.hpp"
#include <opencv2/cudaoptflow.hpp>

using namespace cv;
using namespace cv::cuda;

DLLEXPORT uint8_t *calc_cuda_flow (int rows, int cols, uint8_t *previous, uint8_t *current, uint8_t *flow){
	// Ptr<cv::superres::DualTVL1OpticalFlow> opt = cv::superres::createOptFlow_DualTVL1_CUDA();
	Ptr<cv::cuda::OpticalFlowDual_TVL1> opt = cv::cuda::OpticalFlowDual_TVL1::create();
	cv::Mat previous_gray(rows, cols, CV_8UC1, (void*) previous);
	cv::Mat current_gray(rows, cols, CV_8UC1, (void*) current);
	cv::Mat f(rows, cols, CV_8UC1, (void*) flow);
	opt->calc(previous_gray, current_gray, f);
	return(f.data);
}

int main(int argc, char* argv[]){
	return 0;
}