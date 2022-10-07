mkdir backup
yes | darknet detector train cfg/anime.data cfg/yolov3-spp-training.cfg backup/yolov3-spp-training_final.weights -gpus 0 
# darknet detector train cfg/anime.data cfg/yolov3-spp-training.cfg data/yolov3-spp_anime_as_human.weights -gpus 0