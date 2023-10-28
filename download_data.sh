data_path=$1

gdown 1_IuWVQRSPeZKPNBEePqkN6RP6Rsc9GoR
unzip -j background_augmented_data.zip -d $data_path
rm background_augmented_data.zip

gdown 13w0NZMRbW4cB6WWuNSLGQJSNKsQuTDWl
unzip -j background_augmented_data2.zip -d $data_path
rm background_augmented_data2.zip

gdown 14F7XIRYTLqVzYr8nygXWPDTUazgzzhlg
unzip -j augmented_data.zip -d $data_path
rm augmented_data.zip

gdown 1uv4KBHzeLs9kQgGiCCv9E8aidnolNliE
unzip -j clean_train.zip -d $data_path
rm clean_train.zip