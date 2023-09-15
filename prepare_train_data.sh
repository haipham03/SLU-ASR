wav_dir=$1
jsonfile=$2

python3 prepare_train_data.py -w $wav_dir -j $jsonfile

python3 pre_process.py

echo "Done"