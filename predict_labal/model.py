from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.multiclass import OneVsRestClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

# Read the data
new_df = pd.read_csv('/Users/camille/repo/Hetic/projet_gouv/scraping/export-experiences_lem.csv', sep='\t', encoding='latin-1')
new_df = new_df.drop(columns=['Unnamed: 0'])

# Split the data into train and test sets
train, test = train_test_split(new_df, random_state=42, test_size=0.30, shuffle=True)

# Preprocess the text data
train_text = train['Description']
test_text = test['Description']

# Initialize the TfidfVectorizer
vectorizer = TfidfVectorizer(strip_accents='unicode', analyzer='word', ngram_range=(1,3), norm='l2')

# Fit the vectorizer on the train text
vectorizer.fit(train_text)

# Transform the train and test text data
x_train = vectorizer.transform(train_text)
x_test = vectorizer.transform(test_text)

# Prepare the target variables
y_train = train.drop(labels=['Description'], axis=1)
y_test = test.drop(labels=['Description'], axis=1)

# Get the list of categories
categories = list(new_df.columns.values)
categories = categories[:-1]

# Using pipeline for applying logistic regression and one vs rest classifier
LogReg_pipeline = Pipeline([
    ('clf', OneVsRestClassifier(LogisticRegression(solver='sag'), n_jobs=-1)),
])

# Iterate over categories and train logistic regression models
for category in categories:
    print('Processing {} comments...'.format(category))
    
    # Training logistic regression model on train data
    LogReg_pipeline.fit(x_train, train[category])
    
    # Calculating test accuracy
    prediction = LogReg_pipeline.predict(x_test)
    print('Test accuracy is {}'.format(accuracy_score(test[category], prediction)))
    print("\n")

# Create a DataFrame to store the predicted values
predicted_df = pd.DataFrame(index=test.index)

# Iterate over categories and make predictions
for category in categories:
    # Train the logistic regression model on train data
    LogReg_pipeline.fit(x_train, train[category])
    
    # Make predictions on test data
    predictions = LogReg_pipeline.predict(x_test)
    
    # Add the predicted column to the DataFrame
    predicted_df[category + '_predicted'] = predictions

# Concatenate the test DataFrame (with original columns) and the predicted DataFrame
result_df = pd.concat([test, predicted_df], axis=1)
result_df = pd.merge(result_df, new_df[['Description']], left_index=True, right_index=True)

"""for category in categories:
    printmd('**Processing {} comments...**'.format(category))
    
    # Training logistic regression model on train data
    LogReg_pipeline.fit(x_train, train[category])
    
    # Predict probabilities for positive class
    y_scores = LogReg_pipeline.predict_proba(x_test)[:, 1]
    
    # Calculate fpr, tpr, and thresholds
    fpr, tpr, thresholds = roc_curve(test[category], y_scores)
    
    # Calculate AUC
    roc_auc = auc(fpr, tpr)
    
    # Plot ROC curve
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label='ROC curve (AUC = {:.2f})'.format(roc_auc))
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve - Category: {}'.format(category))
    plt.legend(loc='lower right')
    plt.show()"""
