# CAPITOLO 5 ANALISI SEMANTICA
#5.1.1 ANALISI PRO-UCRAINA
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
import pandas as pd

# Funzione di pre-processing 
def preprocess(text):
    if not isinstance(text, str): #gestione di valori non stringa
      return ""
    new_text = []
    for t in text.split(): #split senza argomenti gestisce meglio gli spazi multipli
        if t.startswith('@') and len(t) > 1:
            t = '@user'
        elif t.startswith('http'):
            t = 'http'
        else:
            t = t 
        new_text.append(t)
    return " ".join(new_text)

MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

def get_sentiment(text):
    text = preprocess(text)
    if not text: #gestione di stringhe vuote dopo il preprocessing
      return "ERRORE", 0.0, 0.0, 0.0 #restituisce valori di default in caso di errore
    encoded_input = tokenizer(text, return_tensors='pt', truncation=True, padding=True) #aggiunti truncation e padding
    try:
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        ranking = np.argsort(scores)[::-1]
        results = {}
        for i in range(scores.shape[0]):
            l = config.id2label[ranking[i]]
            s = scores[ranking[i]]
            results[l] = float(s) #salvo i risultati in un dizionario
        return results["positive"], results["neutral"], results["negative"] #restituisco i valori in ordine
    except Exception as e:
        print(f"Errore nell'analisi del testo: {text}. Errore: {e}")
        return "ERRORE", 0.0, 0.0, 0.0


df = pd.read_csv("/content/Senza nome 3.csv", sep=";")

# ApplicO la funzione a ogni tweet
df['positive_score'], df['neutral_score'], df['negative_score'] = zip(*df['Content'].apply(get_sentiment))

# CalcolO il sentiment predominante
def get_predominant_sentiment(row):
    if row['positive_score'] > row['neutral_score'] and row['positive_score'] > row['negative_score']:
        return 'POSITIVO'
    elif row['negative_score'] > row['neutral_score'] and row['negative_score'] > row['positive_score']:
        return 'NEGATIVO'
    else:
        return 'NEUTRO'

df['sentiment'] = df.apply(get_predominant_sentiment, axis=1)

# Mostra i risultati
print(df[['Content', 'sentiment', 'positive_score', 'neutral_score', 'negative_score']])

# Salva il dataset con i risultati
df.to_csv("tweets_with_sentiment.csv", index=False)
#FUNZIONE PER RAPPRESENTARE IL GRAFICO
import pandas as pd

df = pd.read_csv("tweets_with_sentiment.csv")

# Conta i tweet per ogni categoria di sentiment
sentiment_counts = df['sentiment'].value_counts()

# Stampa i risultati
print("Tweet classificati per sentiment:")
print(sentiment_counts)

import matplotlib.pyplot as plt

sentiment_counts.plot(kind='bar', color=['green', 'blue', 'red'])
plt.title("Distribuzione dei Sentiment")
plt.xlabel("Sentiment")
plt.ylabel("Numero di Tweet")
plt.xticks
#CALCOLO MEDIA VARIANZA...
import pandas as pd
import numpy as np

def calculate_statistics(df, sentiment_label):
    sentiment_df = df[df['sentiment'] == sentiment_label]
    if sentiment_df.empty:
        return pd.Series({
            'media': np.nan, 'varianza': np.nan, 'mediana': np.nan, 'q1': np.nan, 'q3': np.nan
        })

    # Mappatura tra etichetta di sentiment e nome della colonna di punteggio
    score_column_map = {
        'POSITIVO': 'positive_score',
        'NEGATIVO': 'negative_score',
        'NEUTRO': 'neutral_score'
    }

    score_column = score_column_map.get(sentiment_label)

    if score_column is None:
        print(f"Attenzione: etichetta di sentiment non riconosciuta: {sentiment_label}")
        return pd.Series({
            'media': np.nan, 'varianza': np.nan, 'mediana': np.nan, 'q1': np.nan, 'q3': np.nan
        })

    # Calcolo le statistiche usando describe con percentili
    stats = sentiment_df[score_column].describe(percentiles=[0.25, 0.75])

    return pd.Series({
        'media': stats['mean'], 'varianza': sentiment_df[score_column].var(), 'mediana': stats['50%'], 'q1': stats['25%'], 'q3': stats['75%']
    })


try:
    df = pd.read_csv("tweets_with_sentiment.csv")
except FileNotFoundError:
    print("Errore: File 'tweets_with_sentiment.csv' non trovato.")
    exit()

# Calcolo le statistiche per ogni sentimento 
sentiment_stats = df.groupby('sentiment').apply(lambda x: calculate_statistics(x, x.name)).unstack('sentiment')
# Mostro le statistiche
print(sentiment_stats)

#CONTROLLI SUL DATASER REALE
import pandas as pd

df2 = pd.read_csv("/content/mio_dataset_ridotto.csv")

df3 = df2[df2['classification'] == 'Pro-Ucraina'].copy()
# Conto i tweet per ogni categoria di sentiment
sentiment_counts = df3['sentiment'].value_counts()

# Stampa i risultati
print("Tweet classificati per sentiment:")
print(sentiment_counts)

import matplotlib.pyplot as plt

sentiment_counts.plot(kind='bar', color=['green', 'blue', 'red'])
plt.title("Distribuzione dei Sentiment")
plt.xlabel("Sentiment")
plt.ylabel("Numero di Tweet")
plt.xticks(rotation=0)
plt.show()

import pandas as pd
import numpy as np

def calculate_statistics(df, sentiment_label):
    sentiment_df = df[df['sentiment'] == sentiment_label]
    if sentiment_df.empty:
        return pd.Series({
            'media': np.nan, 'varianza': np.nan, 'mediana': np.nan, 'q1': np.nan, 'q3': np.nan
        })

    score_column = 'score'  

    # Calcolo le statistiche usando describe con percentili
    stats = sentiment_df[score_column].describe(percentiles=[0.25, 0.75])

    return pd.Series({
        'media': stats['mean'], 'varianza': sentiment_df[score_column].var(), 'mediana': stats['50%'], 'q1': stats['25%'], 'q3': stats['75%']
    })

try:
    df = pd.read_csv("/content/mio_dataset_ridotto.csv")
except FileNotFoundError:
    print("Errore: File 'mio_dataset_ridotto.csv' non trovato.")
    exit()
df3 = df[df['classification'] == 'Pro-Ucraina'].copy()
# Calcolo le statistiche per ogni sentimento 
sentiment_stats = df3.groupby('sentiment').apply(lambda x: calculate_statistics(x, x.name)).unstack('sentiment')

# Mostro le statistiche
print(sentiment_stats)

#CONFRONTO TRA DATASET REALE E SINTETICO SUI SENTIMENT
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    df_reali = pd.read_csv('/content/tweets_pro_ucraina_with_sentiment.csv')
    df_sintetici = pd.read_csv('/content/tweets_with_sentiment.csv')
except FileNotFoundError as e:
    print(f"Errore: File non trovato: {e}")
    exit()

if 'sentiment' not in df_reali.columns or 'sentiment' not in df_sintetici.columns:
    print("Errore: La colonna 'sentiment' non è presente in uno dei file.")
    exit()

# Calcolo le percentuali per ogni sentimento
percentuali_reali = df_reali['sentiment'].value_counts(normalize=True) * 100
percentuali_sintetici = df_sintetici['sentiment'].value_counts(normalize=True) * 100

# Creo un DataFrame per il grafico
df_percentuali = pd.DataFrame({
    'Sentiment': percentuali_reali.index.tolist() + percentuali_sintetici.index.tolist(),
    'Percentuale': percentuali_reali.tolist() + percentuali_sintetici.tolist(),
    'Tipo': ['Reale'] * len(percentuali_reali) + ['Sintetico'] * len(percentuali_sintetici)
})

# Ordino il DataFrame per 'Sentiment' 
sentiment_order = ['NEGATIVO', 'NEUTRO', 'POSITIVO']
df_percentuali['Sentiment'] = pd.Categorical(df_percentuali['Sentiment'], categories=sentiment_order, ordered=True)
df_percentuali = df_percentuali.sort_values('Sentiment')

# Stampo le percentuali
print("Percentuali Sentiment Reale:")
print(percentuali_reali)
print("\nPercentuali Sentiment Sintetico:")
print(percentuali_sintetici)

# Creo il grafico a barre affiancate
plt.figure(figsize=(10, 6))
sns.barplot(x='Sentiment', y='Percentuale', hue='Tipo', data=df_percentuali, palette=["#3498db", "#e74c3c"])
plt.title('Confronto tra Percentuali di Sentiment Reale e Sintetico')
plt.xlabel('Sentiment')
plt.ylabel('Percentuale')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()