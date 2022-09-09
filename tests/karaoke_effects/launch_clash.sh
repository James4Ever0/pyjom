export http_proxy=""
export https_proxy=""
# env http_proxy="http://localhost:38457" https_proxy="http://localhost:38457" curl -O https://openit.ml/Clash.yaml
##########FETCHING LATEST YAML############
# env http_proxy="http://localhost:38457" https_proxy="http://localhost:38457" curl -O https://raw.githubusercontent.com/yu-steven/openit/main/Clash.yaml
# python3 get_clash_yaml.py
##########FETCHING LATEST YAML############

# refreshing can be ignored since it is not needed.
clash -f ClashBaseOpenIt.yaml