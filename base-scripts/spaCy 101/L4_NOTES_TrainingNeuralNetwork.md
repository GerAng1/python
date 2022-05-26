# Lesson 4: Training a Neural Network

## Why update the model?
- Better results on your specific domain
- Learn classification schemes specifically for your problem
- Essential for text classification
- Very useful for named entity recognition
- Less critical for part-of-speech tagging and dependency parsing

## How training works (1)

1. Initialize the model weights randomly
2. Predict a few examples with the current weights
3. Compare prediction with true labels
4. Calculate how to change weights to improve predictions
5. Update weights slightly
6. Go back to 2.
