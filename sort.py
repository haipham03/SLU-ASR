with open('process_trans_file.txt', 'r') as file:
    lines = file.readlines()

# Convert the lines to lowercase and then sort them by the lowercase WAV file names in ascending order
sorted_lines = sorted(lines, key=lambda line: line.split('/')[-1].lower())

# Write the sorted lines to a new text file
with open('process_trans_file.txt', 'w') as file:
    file.writelines(sorted_lines)