from snownlp import sentiment

sentiment.train('train/bad_review.txt', "train/praise.txt")
sentiment.save("train/sentiment.marshal")