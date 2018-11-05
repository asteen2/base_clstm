import csv
import numpy as np	

input_filename = '../data/prokaryote_refseq_top_30_1500max.tsv'

output_dir = '/mnt/data/computervision/train80_val10_test10'
train_filename = output_dir + '/train.csv'
val_filename = output_dir + '/validation.csv'
test_filename = output_dir + '/test.csv'

label_filename = '../results/class_names.csv'

label_mapping = dict()
labels = []
split_data = dict()

with open(input_filename) as tsvfile:    
	reader = csv.reader(tsvfile, delimiter='\t')
	i = 0
	for row in reader:
		if i > 0: #ignore the first line
			x = row[3]
			label = row[2]
			if not label in label_mapping:
				label_mapping[label] = len(label_mapping)
				labels.append(label)
			y = label_mapping[label]
			if not y in split_data:
				split_data[y] = []
			split_data[y].append(x)
		i += 1
	print 'total examples: ', i-1

with open(label_filename, 'w') as label_file:
	w = csv.writer(label_file)
	for i in range(len(labels)):
		w.writerow([i, labels[i]])

print 'class sizes:'
for y in split_data:
	print len(split_data[y])

with open(train_filename, 'w') as train_file, open(val_filename, 'w') as val_file, open(test_filename, 'w') as test_file:
	train_writer = csv.writer(train_file)
	val_writer = csv.writer(val_file)
	test_writer = csv.writer(test_file)

	for y in split_data:
		arr = split_data[y]
		l = len(arr)
		for i in range(l):
			x = arr[i]
			#80% train, 10% val, 10% test
			if i < l * 8 / 10:
				train_writer.writerow([y, x])
			elif i < l * 9 / 10:
				val_writer.writerow([y, x])
			else:
				test_writer.writerow([y, x])
