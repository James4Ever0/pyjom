python train_subg.py --data_path data/inat2018_train_dedup_inter_intra.pkl --model_filename  checkpoint/inat.ckpt --knn_k 10,5,3 --levels 2,3,4 --faiss_gpu --hidden 512 --epochs 250 --lr 0.01 --batch_size 4096 --num_conv 1 --gat --balance
