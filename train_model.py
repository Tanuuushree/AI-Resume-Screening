# train_model.py

import pandas as pd
import re
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("C:\\Users\\ASUS\\OneDrive\\Desktop\\ai_resume_screening\\Resume.csv")

# Clean text function
def clean_text(text):
    text = re.sub(r'http\\S+', '', text)
    text = re.sub(r'[^A-Za-z ]', '', text)
    text = text.lower()
    return text

# Clean resume text
df['Resume'] = df['Resume_str'].apply(clean_text)

# Features and labels
X = df['Resume']
y = df['Category']

# Convert text into numbers
vectorizer = TfidfVectorizer(stop_words='english')

X_vectorized = vectorizer.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = LogisticRegression()

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)

# Save model
pickle.dump(model, open("model.pkl", "wb"))

# Save vectorizer
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model saved successfully!")