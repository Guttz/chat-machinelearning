import pandas as pd
from sklearn.externals import joblib
import pickle

df_a = pd.read_csv(r"C:\Users\Aniruddh Goteti\Desktop\intellikwitt\data1.csv")
df_b = pd.read_csv(r"C:\Users\Aniruddh Goteti\Desktop\intellikwitt\data2.csv")
df_c = pd.read_csv(r"C:\Users\Aniruddh Goteti\Desktop\intellikwitt\data3.csv")

f = open('data1.pkl', 'wb')
pickle.dump(df_a, f, protocol=2)
f.close()
print("Model dumped!")        
fb = open('data2.pkl', 'wb')
pickle.dump(df_b, fb, protocol=2)
fb.close()
print("Model dumped!") 
fc = open('data3.pkl', 'wb')
pickle.dump(df_c, fc, protocol=2)
fc.close()
print("Model dumped!") 