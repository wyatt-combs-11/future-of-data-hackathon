import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import joblib
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import Callback

# # Build pivot data
# data = pd.read_csv('obis_data_no_na.csv')
# pivot_data = data.pivot_table(index=['longitude', 'latitude'], columns='name', values='quantity', fill_value=0)
# pivot_data = np.log1p(pivot_data.clip(lower=1))
# max_quantity = pivot_data.max().max()
# pivot_data = pivot_data / max_quantity
# pivot_data = pivot_data.reset_index()
#
# # Create data sets with lots of noise, needed for how tight the spacial data is
# X = pivot_data[['longitude', 'latitude']].values
# y = pivot_data.drop(columns=['longitude', 'latitude']).values
# np.random.seed(42)
# noise = np.random.normal(scale=0.1, size=X.shape)
# X_noisy = X + noise
#
# # Split data
# scaler = MinMaxScaler()
# X_noisy = scaler.fit_transform(X_noisy)
# X_train, X_test, y_train, y_test = train_test_split(X_noisy, y, test_size=0.2, random_state=42)
#
# # Build model
# model = Sequential()
# model.add(Dense(128, input_dim=X_train.shape[1], activation='relu'))
# model.add(Dense(64, activation='relu'))
# model.add(Dense(32, activation='relu'))
# model.add(Dense(y_train.shape[1], activation='sigmoid'))
# model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
#
#
# # Nice visual for training and loss progression
# class TrainingProgress(Callback):
#     def on_epoch_end(self, epoch, logs=None):
#         print(f"Epoch {epoch + 1}: loss = {logs['loss']:.4f}, val_loss = {logs['val_loss']:.4f}")
#
#
# # Train the model, check model versions
# model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2, verbose=0, callbacks=[TrainingProgress()])
# model.save('best_fish_model_v5.h5')
# joblib.dump(scaler, 'scaler_v5.pkl')
#
# # Evaluate the model
# y_pred = model.predict(X_test)
# mse = mean_squared_error(y_test, y_pred)
# print(f"Mean Squared Error on Test Set: {mse}")
