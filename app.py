import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import streamlit as st

# Load data
@st.cache_data  # Cache the data to improve performance
def load_data():
    data = pd.read_csv('creditcard.csv')
    return data

data = load_data()

# Separate legitimate and fraudulent transactions
legit = data[data['Class'] == 0]
fraud = data[data['Class'] == 1]

# Balance the dataset
legit_new = legit.sample(n=len(fraud), random_state=2)
new_df = pd.concat([legit_new, fraud], axis=0)

# Split the data into X and Y
X = new_df.drop('Class', axis=1)
Y = new_df['Class']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

# Train logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, Y_train)

# Check model performance
train_data_acc = accuracy_score(model.predict(X_train), Y_train)
test_data_acc = accuracy_score(model.predict(X_test), Y_test)

# Streamlit web app
st.title("Credit Card Fraud Detection Model")
st.write("""
This app predicts whether a credit card transaction is **legitimate** or **fraudulent** using a Logistic Regression model.
""")

# Add an image
st.image("fraud_detection.jpg", caption="Fraud Detection System", use_column_width=True)

# Display model accuracy
st.sidebar.header("Model Performance")
st.sidebar.write(f"Training Accuracy: **{train_data_acc:.2%}**")
st.sidebar.write(f"Test Accuracy: **{test_data_acc:.2%}**")

# Input fields for features
st.header("Enter Transaction Details")
st.write("Please provide the following features to make a prediction:")

# Create input fields for each feature
input_features = []
for i, column in enumerate(X.columns):
    input_features.append(st.number_input(f"{column}", value=0.0, step=0.01))

# Convert input to numpy array
input_data = np.array(input_features).reshape(1, -1)

# Submit button
if st.button("Predict"):
    # Make prediction
    prediction = model.predict(input_data)
    prediction_proba = model.predict_proba(input_data)

    # Display result
    st.subheader("Prediction Result")
    if prediction[0] == 0:
        st.success("✅ **Legitimate Transaction**")
    else:
        st.error("❌ **Fraudulent Transaction**")

    # Show prediction probability
    st.write(f"Probability of being legitimate: **{prediction_proba[0][0]:.2%}**")
    st.write(f"Probability of being fraudulent: **{prediction_proba[0][1]:.2%}**")


