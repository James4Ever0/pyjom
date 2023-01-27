from ultralytics.yolo.utils.torch_utils import strip_optimizer

model_path = "general_ver1_with_optimizer.pt"

export_path = "general_ver1.pt"
strip_optimizer(f=model_path, s=export_path)
