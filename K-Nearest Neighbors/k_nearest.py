import sys

#
#   Trains algorithm by generating n dimensional vectors of features given a csv .txt file of 
#   data with the classification in the right most column
#
def train_data(file):  
  
    # Read the file, splitting by lines 
    f = open(file, 'r') 
    lines = f.read().splitlines() 

    data = {}
    iterator = True  
    # makes dictionary of classes
    for l in lines:
        arr = l.split(',')
        if (iterator):  
            iterator = False
            continue 
        trimmed_class = arr[len(arr) - 1].strip()
        data[trimmed_class] = []
    
    # load data to correct key as a tuple
    iterator = True
    for l in lines:
        arr = l.split(',')
        if (iterator): 
            iterator = False
            continue 
        trimmed_class = arr[len(arr) - 1].strip()
    
        for i in range(len(arr[:-1])):
            arr[i] = float(arr[i])    
        vector = tuple(arr[:-1])  
        data[trimmed_class].append(vector)
    f.close() 

    return data

#
#   Classifies the test data by calculating the euclidean distances from the data to the training data 
#   Then creates a frequency dictionary where keys are classes and values are frequency
#   Finally calculates the most frequent k nearest neighbors and returns the classification
# 
def classify(testpt, training_set, k=3):
    k_set = []
   
    # populates the k set with euclidean distances of the training data to the testpt
    for key, vector in training_set.items(): 
        for feature in vector: 
            ed = euclidean_distance(feature, testpt)
            k_set.append((key, list(feature), ed)) 

    # sorts the set by euclidean distance and gets the k closest neighbors of testpt
    k_set.sort(key=lambda x: x[2])
    k_set = k_set[:k] 
     
    # creates the frequency dictionary containing { class : frequency } 
    freq_set = {}
    for i in k_set:
        freq_set[i[0]] = 0 
    # if only one key exists it returns that class    
    if len(freq_set.keys()) == 1:
        return i[0]
    else:
        for i in k_set:
            freq_set[i[0]] += 1
     
    # iterates through the frequency dictionary to get the most frequent closest k class
    top_class = None
    for c0 in freq_set: 
        for c1 in freq_set: 
            if (freq_set[c0] > freq_set[c1]):
                top_class = c0
         
    return top_class 

# gets the euclidean distance based on n dimensions (the features dimensions)
def euclidean_distance(feature, testpt):
    sumation = 0
    for dim in range(len(feature)):
        sumation += ((feature[dim] - testpt[dim]) ** 2)
    return (sumation ** (1/2))
 

def getTestPoints(file):
    # Read the file, splitting by lines 
    f = open(file, 'r') 
    lines = f.read().splitlines() 
 
    # converts lines in file into array of tuples
    iterator = True
    data = []
    for l in lines: 
        if (iterator):  
            iterator = False
            continue 
        arr = l.split(',')  
        for i in range(len(arr)):
            arr[i] = float(arr[i])
        data.append(tuple(arr))  
    return data

# ends program if incorrect cmd line args
if len(sys.argv) < 3: 
    sys.exit()
 
train_file = sys.argv[1]
test_file = sys.argv[2] 

# runs program by loading training data then classifying
training_set = train_data(train_file) 
testing_data = getTestPoints(test_file)

# loops through test points and classifies them
for testpt in testing_data:
    classification = classify(testpt, training_set)
    print(testpt, "classified as", classification)  