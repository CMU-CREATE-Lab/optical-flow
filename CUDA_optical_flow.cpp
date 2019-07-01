#include "opencv2/opencv.hpp"
#include <stdio.h>
#include <stdlib.h>

using namespace cv;
using namespace cv::cuda;

extern "C" void calc_cuda_flow (int rows, int cols, uint8_t *previous, uint8_t *current, uint8_t *flow){
	Ptr<cv::cuda::OpticalFlowDual_TVL1> opt = cv::cuda::OpticalFlowDual_TVL1::create();
	
	cv::Mat previous_gray(rows, cols, CV_8UC1, (void*) previous);
	cv::cuda::GpuMat gpu_prev_gray;
	gpu_prev_gray.upload(previous_gray);
	
	cv::Mat current_gray(rows, cols, CV_8UC1, (void*) current);
	cv::cuda::GpuMat gpu_curr_gray;
	gpu_curr_gray.upload(current_gray);

	cv::Mat f(rows, cols, CV_8UC2, (void*) flow);
	cv::cuda::GpuMat gpu_flow;
	gpu_flow.upload(f);

	opt->calc(gpu_prev_gray, gpu_curr_gray, gpu_flow);
	cv::Mat cpu_flow(gpu_flow);
	uint8_t *data = cpu_flow.data;
	for(uint16_t i; i < rows*cols*2; i++){
		flow[i] = data[i];
	}
}

int main(int argc, char* argv[]){
	return 0;
}
