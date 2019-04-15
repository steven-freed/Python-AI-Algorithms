# K-Nearest Neighbors
KNN is a supervised learning algorithm, meaning that the answer we want is in our training data somewhere. KNN is also a lazy learning algorithm because the function is appoximated locally and computation is delayed until the last minute. In KNN we have an N dimensional space of N dimensional training data vectors. We then feed the algorithm our data (1 or more N dimensional vectors) we want to classify and it calculates the distance from each vector you give it to it's K nearest neighboring vectors (neighbors being training data vectors). It then gets the K nearest neighbors and classifies the vectors you give the algorithm based on frequency of it's neighbors classes.
 
### Important:
1. K should be odd.
(if you have 2 vectors of class A and 2 vectors of class B, how do we classify? We need a way to prevent ties)

2. We must pick a suitable K.  
(if we only have 4 vectors of training data and K = 3, the algorithm won't be very accurate if 3/4 of those training vectors are class A and 1/4 is class B)  

3. The more training data you give the algorithm, the more accurate it will be.
(more vectors in the N dimensional space)