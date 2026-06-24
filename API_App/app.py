from flask import Flask, request, jsonify, make_response, send_from_directory, render_template
import pickle # Usiamo joblib al posto di pickle
import pandas as pd
import os
import json

app = Flask(__name__)

# ==========================================
# 1. CARICAMENTO DATI DAL FILE .PKL
# ==========================================
# Carichiamo il dizionario che abbiamo salvato nello script precedente
with open(f'./logReg_model.pkl', 'rb') as file:
    dati_modello = pickle.load(file)

modello = dati_modello['modello']
scaler = dati_modello['scaler']
threshold = dati_modello['threshold']
features_cols = dati_modello['features']


# api endpoint
@app.route('/api', methods=['GET'])
def api():
    try:
        #recupero dati da request
        input_data = request.args.get('data')
        x_input = json.loads(input_data)
        
        
        x_input_df = pd.DataFrame([x_input], columns=features_cols)
    
        x_input_scaled = scaler.transform(x_input_df)
        
        probabilita = modello.predict_proba(x_input_scaled)[0]
        prob_1 = probabilita[0]
        prob_2 = probabilita[1]
        prob_3 = probabilita[2]
        
        if ((prob_1 > threshold)  and (prob_1 > prob_2)):
            esito = '1'
        elif ((prob_2 > threshold) and (prob_2 > prob_1)):
            esito = '2'
        else:
            esito = 'X'
            
        # restituisco anche le probabilità
        risposta = {
            'previsione': esito,
            'probabilita_1': round(prob_1 * 100, 2),
            'probabilita_2': round(prob_2 * 100, 2),
            'probabilita_X': round(prob_3 * 100, 2),
        }
        
        return make_response(jsonify(risposta), 200)

    except Exception as e: 
        print(str(e))
        return make_response(jsonify({'error': str(e)}), 500)


# homepage test
@app.route('/test')
def test():
    input_sample = [0.0] * len(features_cols)
    input_s = str(input_sample).replace(" ","")
    
    html = f"""<h1>API for Serie A Match Prediction</h1>
               <p>Test the API from here: <br>
               <a href='{request.base_url}api?data={input_s}'>
               {request.base_url}api?data={input_s}</a></p>
               <p>Input documentation (features required): {str(features_cols)}</p>"""
    return html



@app.route('/')
def home():
    return render_template('index.html')



# icona scheda
@app.route('/favicon.ico')
def favicon():
    # cerca il file 'favicon.ico' per icona sito
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)