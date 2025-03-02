#! /usr/bin/env  bash

# install python dependencies
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi
if [ $? != 0 ]; then
    echo "Install python dependencies failed !!!"
    exit 1
fi

# install package libsndfile
python -c "import soundfile"
if [ $? != 0 ]; then
    echo "Install package libsndfile into default system path."
    cp packages/libsndfile-1.0.28.tar.gz .
    tar -zxvf libsndfile-1.0.28.tar.gz
    cd libsndfile-1.0.28
    ./configure > /dev/null && make > /dev/null && make install > /dev/null
    cd ..
    rm -rf libsndfile-1.0.28
    rm libsndfile-1.0.28.tar.gz
fi

cp packages/pa_stable_v190600_20161030.tgz .
tar -zxvf pa_stable_v190600_20161030.tgz
cd portaudio
./configure > /dev/null && make > /dev/null && make install > /dev/null
cd ..
rm -rf portaudio
rm pa_stable_v190600_20161030.tgz

# install decoders
python -c "import pkg_resources; pkg_resources.require(\"swig_decoders==1.1\")"
if [ $? != 0 ]; then
    cd decoders/swig > /dev/null
    sh setup.sh
    cd - > /dev/null
fi





echo "Install all dependencies successfully."
