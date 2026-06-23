import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import pickle


df = pd.read_excel("trainable_dataset.xlsx", engine='openpyxl', dtype={'Risultato': str})
df['Risultato'] = df['Risultato'].replace('X', '3')
df.columns = df.columns.str.strip()


X = df.drop(columns=['Risultato', 'Home_ID', 'Away_ID']).fillna(0)
y = df['Risultato']



# stratify=y garantisce la stessa proporzione di valori target nei due set
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scaliamo sia test che train
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


print("Addestramento della Regressione Logistica in corso...")

log_reg = LogisticRegression(solver='lbfgs', max_iter=1000, random_state=42) # dovrebbe capire da solo che è multiclass
log_reg.fit(X_train_scaled, y_train)




probabilita = log_reg.predict_proba(X_test_scaled)
classi = log_reg.classes_ 

# Creiamo una bella tabella (DataFrame) per leggerle facilmente
df_prob = pd.DataFrame(probabilita, columns=[f"Prob_{c}" for c in classi])
df_prob['Risultato_Reale'] = y_test.values

print("\n--- PERCENTAGES OF THE FIRST 5 MATCHES ---")
print((df_prob.head() * 100).round(1)) 


# Apply the manual Threshold
threshold = 0.45
print(f"\n\n\nApply threshold at {threshold * 100:.2f}%")


nuove_previsioni = []
# alter the predictions
for riga in probabilita:
    prob_1 = riga[0] # Probabilità della classe '1'
    prob_2 = riga[1] # Probabilità della classe '2'
    prob_3 = riga[2] # Probabilità della classe '3'
    
    if prob_1 > threshold:
        nuove_previsioni.append('1')
    elif prob_2 > threshold:
        nuove_previsioni.append('2')
    else:
        # Se né la squadra di casa né quella in trasferta dominano... è X!
        nuove_previsioni.append('3')


nuove_previsioni = np.array(nuove_previsioni)


nuova_accuracy = accuracy_score(y_test, nuove_previsioni)
print(f"\n--- RESULTS WITH THRESHOLD ---")
print(f"Accuracy on Test Set: {nuova_accuracy * 100:.2f}%\n")

print("Detailed Report:")
print(classification_report(y_test, nuove_previsioni))



## salvataggio in pickle

dati_da_salvare = {
    'modello': log_reg,
    'scaler': scaler,
    'threshold': threshold,
    'features': list(X.columns)
}
pickle.dump(dati_da_salvare, open(r'.\logReg_model.pkl', 'wb'))