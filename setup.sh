chmod +x ./tools/dex2jar/d2j-dex2jar.sh
chmod +x ./tools/dex2jar/d2j_invoke.sh
git submodule update --init --recursive
pip3 install -r requirement.txt
cd ./tools && git clone https://github.com/Nightbringer21/fridump.git