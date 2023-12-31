pip install tensorflow numpy pandas matplotlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Define the stock symbol and time frame
stock_symbol = 'GOOGL'
start_date = '2010-01-01'
end_date = '2021-09-30'

# Fetch stock data using Yahoo Finance API
data = yf.download(stock_symbol, start=start_date, end=end_date)

# Extract the 'Close' prices and normalize the data
data = data['Close'].values.reshape(-1, 1)
scaler = MinMaxScaler()
data = scaler.fit_transform(data)

# Split the data into training and testing sets
train_size = int(0.8 * len(data))
train_data = data[:train_size]
test_data = data[train_size:]

# Function to create sequences for training the LSTM model
def create_sequences(data, seq_length):
    sequences = []
    target = []
    for i in range(len(data) - seq_length):
        sequences.append(data[i:i+seq_length])
        target.append(data[i+seq_length])
    return np.array(sequences), np.array(target)

# Define sequence length for training
sequence_length = 10

# Create sequences and targets for training
X_train, y_train = create_sequences(train_data, sequence_length)
X_test, y_test = create_sequences(test_data, sequence_length)

# Build the LSTM model
model = Sequential()
model.add(LSTM(units=100, activation='relu', input_shape=(sequence_length, 1)))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Evaluate the model
loss = model.evaluate(X_test, y_test, verbose=0)
print('Mean Squared Error on Test Data:', loss)

# Predict stock prices
predictions = model.predict(X_test)

# Plot the results
plt.figure(figsize=(12, 6))
plt.plot(y_test, label='True Prices')
plt.plot(predictions, label='Predicted Prices')
plt.legend()
plt.show()
