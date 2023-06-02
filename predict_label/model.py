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
new_df = pd.read_csv('predict_label/data_exp_clean.csv', sep='\t', encoding='latin-1')
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

# Using logistic regression with one-vs-rest approach
LogReg_classifier = LogisticRegression(solver='sag', multi_class='ovr')

# Iterate over categories and train logistic regression models
for category in categories:
    print('Processing {} comments...'.format(category))
    
    # Training logistic regression model on train data
    LogReg_classifier.fit(x_train, train[category])
    
    # Calculating test accuracy
    prediction = LogReg_classifier.predict(x_test)
    accuracy = accuracy_score(test[category], prediction)
    print('Test accuracy for {} is {}'.format(category, accuracy))
    print("\n")

# Create a DataFrame to store the predicted values
predicted_df = pd.DataFrame(index=test.index)

# Read the positive DataFrame
data_pe = pd.read_csv('Cleaning_eda/all_data.csv')
data_pe = data_pe.dropna(subset=['cleaned_text'])
# Preprocess the text data
pos_text = data_pe['cleaned_text'].astype(str)



x_pos = vectorizer.transform(pos_text)

# Create a DataFrame to store the predicted values
df_pe = pd.DataFrame(index=data_pe.index)

# Iterate over categories and make predictions on positive data
for category in categories:
    # Train the logistic regression model on train data
    LogReg_classifier.fit(x_train, train[category])
    
    # Make predictions on positive data
    predictions_pos = LogReg_classifier.predict(x_pos)
    
    # Add the predicted column to the DataFrame
    df_pe[category + '_predicted'] = predictions_pos

# Concatenate the positive DataFrame (with original columns) and the predicted DataFrame
result_pos_df = pd.concat([data_pe, df_pe], axis=1)
#ajoute la colonne de l'adreesse
result_pos_df['address'] = data_pe['object_address']
# Save the result_pos_df as a csv file
result_pos_df.to_csv('predict_label/result_pos_df.csv', index=False)


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
