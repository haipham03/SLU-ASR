data_path=$1

# generated data
echo "Downloading Generated Data"
gdown 14F7XIRYTLqVzYr8nygXWPDTUazgzzhlg
unzip -j augmented_data.zip -d $data_path
rm augmented_data.zip

# denoised data
echo "Downloading Denoised Data"
gdown 16AcrEjo4LUq_ah5_dCM8fy0OhqF3Hdup
unzip -j train_denoised.zip -d $data_path
rm train_denoised.zip