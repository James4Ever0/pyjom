cd SiamMask
export SiamMask=$PWD
# cd $SiamMask/experiments/siammask_sharp
# cd $SiamMask/experiments/siammask_sharp
# export PYTHONPATH=$PWD:$PYTHONPATH
# which python3
python3 -m tools.demo --resume experiments/siammask_sharp/SiamMask_DAVIS.pth --config experiments/siammask_sharp/config_davis.json