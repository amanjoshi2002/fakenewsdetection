import warnings
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report

def aifunction(userinput):
    
    # Load first dataset
    warnings.filterwarnings("ignore", category=UserWarning)
    data1 = pd.read_csv("combined_Edited.csv")

    # Load second dataset
    data2 = pd.read_csv("news_data_Edited.csv")

    # Combine datasets
    combined_data = pd.concat([data1, data2], ignore_index=True)

    # Drop rows with missing values in 'title' or 'text' columns
    combined_data.dropna(subset=['title', 'text'], inplace=True)

    # Handle missing values in 'label' column
    combined_data.dropna(subset=['label'], inplace=True)

    # Convert 'label' column to string type
    combined_data['label'] = combined_data['label'].astype(str)

    # Feature Engineering
    combined_data['combined_text'] = combined_data['title'] + ' ' + combined_data['text']
    X = combined_data['combined_text']
    y = combined_data['label']

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Text Vectorization (TF-IDF)
    tfidf_vectorizer = TfidfVectorizer(max_features=5000)
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
    X_test_tfidf = tfidf_vectorizer.transform(X_test)

    # Model Selection and parameter Tuning
    models = [
        ('Logistic Regression', LogisticRegression(max_iter=1000)),
        ('Linear SVM', LinearSVC()),
        ('Random Forest', RandomForestClassifier())
    ]   

    # Train models
    trained_models = {}
    for name, model in models:
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000)),
            ('imputer', SimpleImputer(strategy='mean')),  # Impute missing values
            ('clf', model)
        ])
        pipeline.fit(X_train, y_train)
        trained_models[name] = pipeline

    # Predict label for the custom input
    predictions = {}
    for name, model in trained_models.items():
        y_pred = model.predict([userinput])
        predictions[name] = y_pred[0]

    return y_pred[0]
