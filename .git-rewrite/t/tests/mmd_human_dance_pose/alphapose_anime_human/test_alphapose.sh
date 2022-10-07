# export PATH=$PATH:/usr/lib/python3.9/site-packages/
cd AlphaPose
set -x
# python3 -m alphapose
configpath="/media/root/help/pyjom/tests/mmd_human_dance_pose/alphapose_anime_human/AlphaPose/configs/halpe_26/resnet/256x192_res50_lr1e-3_1x.yaml"
checkpoint="/media/root/help/pyjom/tests/mmd_human_dance_pose/alphapose_anime_human/AlphaPose/pretrained_models/halpe26_fast_res50_256x192.pth"
# python3 trackers/PoseFlow/tracker-general.py
# aw         # is that the only thing we need to load?
rm -rf outputs
mkdir outputs

# it fails to detect shit. try openpose instead.
# unknown video webm. mp4 is better.
# !!!!!!!!!!!!!!!!!!the freaking pose is freaking tracked!!!!!!!!!!!!!!!!!!!
# bigger RAM bigger chance!

# output/vis/[NUM].jpg
# output/AlphaPose_ideal..mp4 <- what is this shit?

# what about EXPOSE tracking my freaking vtuber?
python3 ./demo_inference.py --cfg $configpath --checkpoint $checkpoint --video /root/Desktop/works/pyjom/samples/video/ideal.webm --outdir outputs --save_img --save_video --detbatch 1 --posebatch 1  # it chooses yolo as detector. we train this bitch.
# --detector efficientdet_d1  --save_img --save_video --detbatch 1 --posebatch 1
