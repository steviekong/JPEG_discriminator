import sys
import os
import math

BUFFERSIZE = 512

def main():
	(positive_files, negative_files) = open_read_files(sys.argv[1], sys.argv[2])
	count = 0
	check_result = False 
	print("Checking negative samples")
	for i in negative_files:
		result = discriminator(i)
		for j in result:
			if j[0] > 7.5 and j[1] > 4 and check_result != True:
				print("File Number " + str(count) + " of size " +str(len(i)) + " IS a JPEG")	
				check_result = True
		if check_result == False:
			print("File Number " + str(count) + " of size " +str(len(i)) + " IS NOT a JPEG")
		else:
			check_result = False
		count += 1
	print("Checking positive samples")
	for i in positive_files:
		result = discriminator(i)
		for j in result:
			if j[0] > 7.5 and j[1] > 4 and check_result != True:
				print("File Number " + str(count) + " of size " +str(len(i)) + " IS a JPEG")	
				check_result = True
		if check_result == False:
			print("File Number " + str(count) + " of size " +str(len(i)) + " IS NOT a JPEG")
		else:
			check_result = False
		count += 1

def open_read_files(positive_path, negative_path):
	positive_files = []
	negative_files = []
	for filename in os.listdir(positive_path):
		file = open(positive_path + "/" + filename, 'rb')
		byte_array = file.read();
		positive_files.append(byte_array)
		file.close()
	for filename in os.listdir(negative_path):
		file = open(negative_path + "/"+filename, 'rb')
		byte_array = file.read();
		negative_files.append(byte_array)
		file.close()
	return (positive_files, negative_files)

def calculate_block_entropy(block):
	if len(block) == 0:
		return 0
	freq_list = []
	for i in range(256):
		counter = 0
		for byte in block:
			if byte == i:
				counter += 1
		freq_list.append(float(counter)/len(block))
	entropy = 0.0
	for i in freq_list:
		if i > 0:
			entropy = entropy + i * math.log(i, 2)
	entropy = -entropy
	return entropy

def count_LN(block):
	is_ff = False
	count = 0 
	for i in block:
		if  i == 255:
			is_ff = True
		if  i == 0 and is_ff:
			count += 1
			is_ff = False
	return count

def discriminator(byte_array):
	ln_entropy_list = []
	num_blocks = len(byte_array)/BUFFERSIZE
	count = 0
	while count <= num_blocks:
		block = byte_array[count*BUFFERSIZE:(count+1)*BUFFERSIZE]
		entropy = calculate_block_entropy(block)
		ln_count = count_LN(block)
		ln_entropy_list.append((entropy, ln_count))
		count += 1
	return ln_entropy_list

if __name__ == '__main__':
	main()