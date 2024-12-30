train_dir=$1
train_jsonfile=$2
# val_dir=$3
# val_jsonfile=$4


# python3 prepare_train_data.py -tw $train_dir -t $train_jsonfile -vw $val_dir -v $val_jsonfile
python3 prepare_train_data.py -tw $train_dir -t $train_jsonfile

python3 pre_process.py

echo "Done"