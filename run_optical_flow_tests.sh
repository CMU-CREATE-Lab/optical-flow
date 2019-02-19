sudo screen -x test_optical_flow
sudo rm screenlog.0

# For python in conda env
sudo screen -dmSL "test_optical_flow" bash -c "export PATH='/opt/miniconda3/bin:$PATH'; . '/opt/miniconda3/etc/profile.d/conda.sh'; conda activate optical-flow; python OpticalFlowTest.py"

sudo screen -ls