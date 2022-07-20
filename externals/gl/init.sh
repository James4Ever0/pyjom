apt-get install -y build-essential libxi-dev libglu1-mesa-dev libglew-dev
git clone https://github.com/stackgl/headless-gl
cd headless-gl
git submodule init
git submodule update
export http_proxy=""
export https_proxy=""
npm install
npm run rebuild