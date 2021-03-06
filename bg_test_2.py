# Delete existing screen
for session in $(sudo screen -ls | grep -o '[0-9]\{5\}.test_2')
do
  sudo screen -S "${session}" -X quit
  sleep 2
done

# Delete the log
sudo rm screenlog.0

# For python in conda env
sudo screen -dmSL "test_optical_flow" bash -c "export PATH='/opt/miniconda3/bin:$PATH'; . '/opt/miniconda3/etc/profile.d/conda.sh'; conda activate optical-flow; python test_2.py"

# List screens
sudo screen -ls
