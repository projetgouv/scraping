import streamlit as st
import pandas as pd
import torch
from transformers import CamembertForSequenceClassification, CamembertTokenizer

# Load the saved model
model = CamembertForSequenceClassification.from_pretrained("camembert-base")
tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.load_state_dict(torch.load("./sentiments.pt"))
model.to(device)
model.eval()

# Set page title
st.title("Sentiment Analysis")

# Create file uploader
csv_file = st.file_uploader("Upload CSV file", type=["csv"])

# Create text input field
text_input = st.text_input("Enter text")

# Perform sentiment analysis on the uploaded CSV file
if csv_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Perform sentiment analysis on each review in the DataFrame
    sentiments = []
    for review in df['review_text']:
        encoded_review = tokenizer.encode_plus(
            review,
            add_special_tokens=True,
            max_length=128,
            padding="max_length",
            truncation=True,
            return_attention_mask=True,
            return_tensors="pt"
        )
        input_ids = encoded_review['input_ids'].to(device)
        attention_mask = encoded_review['attention_mask'].to(device)

        with torch.no_grad():
            outputs = model(input_ids, attention_mask)
            logits = outputs.logits

        prediction = torch.argmax(logits, dim=1).item()
        sentiments.append(prediction)

    # Add the predicted sentiments to the DataFrame
    df['Sentiment'] = sentiments

    # Display the DataFrame with predicted sentiments
    st.write("Uploaded CSV file with predicted sentiments:")
    st.dataframe(df)

# Perform sentiment analysis on the entered text
if text_input:
    encoded_text = tokenizer.encode_plus(
        text_input,
        add_special_tokens=True,
        max_length=128,
        padding="max_length",
        truncation=True,
        return_attention_mask=True,
        return_tensors="pt"
    )
    input_ids = encoded_text['input_ids'].to(device)
    attention_mask = encoded_text['attention_mask'].to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask)
        logits = outputs.logits

    prediction = torch.argmax(logits, dim=1).item()

    # Display the predicted sentiment for the entered text
    st.write("Predicted sentiment for entered text:")
    st.write(prediction)
