import sys
import os
import math

#You can run the script with `python disc.py <positive_samples> <negative_samples>` 

#The ORDER OF DIRS is important!!! Don't make the first argument negative_samples! 



BUFFERSIZE = 512 # The block size which can be changed ideally to a power of 2

#Main function
def main():
	#Opens files from the two arguments given by the user
	(positive_files, negative_files) = open_read_files(sys.argv[1], sys.argv[2])
	count = 0
	check_result = False 
	#First Checks the negative samples
	print("Checking positive samples")
	for i in positive_files:
		result = discriminator(i)
		#print(result)
		for j in result:
			# 7.5 is the entropy limit and 4 is the Ln count. 
			if j[0] >= 220 and j[1] >= 2 and check_result != True:
				print("File Number " + str(count) + " of size " +str(len(i)) + " IS a JPEG")	
				check_result = True
		if check_result == False:
			print("File Number " + str(count) + " of size " +str(len(i)) + " IS NOT a JPEG")
		else:
			check_result = False
		count += 1
	#Checks the positive samples
	print("Checking negative samples")
	for i in negative_files:
		result = discriminator(i)
		for j in result:
			if j[0] >= 220 and j[1] >= 2 and check_result != True:
				print("File Number " + str(count) + " of size " +str(len(i)) + " IS a JPEG")	
				check_result = True
		if check_result == False:
			print("File Number " + str(count) + " of size " +str(len(i)) + " IS NOT a JPEG")
		else:
			check_result = False
		count += 1

#Opens files reads the whole file into an array
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

#calculates the entropy of a given byte block
def calculate_block_entropy(block):
	if len(block) == 0:
		return 0
	freq_list = [0] * 256

	for i in range(256):
		counter = 0
		for byte in block:
			if byte == i:
				freq_list[i] += 1
	sum = 0
	for i in freq_list:
		if i != 0:
			sum += 1
	return sum

#Counts the number of LN's in a given block
def count_LN(block):
	i = 0
	count = 0
	while i < len(block)-1:
		if bytes([block[i]]) == b'\xFF' and bytes([block[i + 1]]) == b'\x00':
			count += 1
		i += 1
	return count

#Generates the entropy and LN count data and passes it to main
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