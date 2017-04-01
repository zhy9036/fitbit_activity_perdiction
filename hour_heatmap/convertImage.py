import os, base64, numpy, binascii
dir = '/home/leozhang/Desktop/fitbit/hour_heatmap'
if not os.path.exists('../image_vector_data'):
	os.makedirs('../image_vector_data')
os.chdir(dir)
for root, dirs, filenames in os.walk(dir):
	for filename in filenames:
		if filename.endswith(".png"):
			with open(filename, "rb") as imageFile:
				#s = base64.b64encode(imageFile.read())
				

				#img = cv2.imread(imageFile,0)
				#ret,thresh_img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
				data = imageFile.read()
				#print data
				hex_str = str(binascii.hexlify(data))
				# now create a list of 2-digit hexadecimals
				hex_list = []
				bin_list = []
				for ix in range(2, len(hex_str)-1, 2):
				    hex = hex_str[ix]+hex_str[ix+1]
				    hex_list.append(hex)
				    bin_list.append(bin(int(hex, 16))[2:])
				#print(bin_list)
				bin_str = "".join(bin_list)
				
				print(len(bin_str))
				print '\n'
