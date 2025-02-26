# CAPITOLO 5 ANALISI SINTATTICA
#CALCOLO DEI PARAMETRI SUL DATASER REALE
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import string
from statistics import mean, median, mode, variance, stdev

nltk.download('punkt')

# Funzione per contare le sillabe in una parola
def conta_sillabe(parola):
    vocali = "aeiouy"
    parola = parola.lower().strip(string.punctuation)
    sillabe = 0
    ultima_e = parola.endswith("e")

    for i, lettera in enumerate(parola):
        if lettera in vocali:
            if i == 0 or parola[i-1] not in vocali:
                sillabe += 1
    if ultima_e and sillabe > 1:
        sillabe -= 1
    return sillabe

# Funzione per calcolare il punteggio Flesch Reading Ease
def flesch_reading_ease(testo):
    parole = word_tokenize(testo)
    frasi = sent_tokenize(testo)
    num_parole = len(parole)
    num_frasi = len(frasi)
    num_sillabe = sum(conta_sillabe(parola) for parola in parole if parola.isalpha())

    if num_parole == 0 or num_frasi == 0:  # Evita divisioni per zero
        return 0

    return 206.835 - 1.015 * (num_parole / num_frasi) - 84.6 * (num_sillabe / num_parole)

# Funzione per analisi statistica del testo
def analisi_testo(testo):
    testo = testo.lower()  
    parole = word_tokenize(testo)  # Tokenizzazione del testo
    hashtag = [word for word in parole if word.startswith('#')]  # Individua gli hashtag
    num_parole = len(parole)
    num_hashtag = len(hashtag)
    diversita_lessicale = len(set(parole)) / num_parole if num_parole > 0 else 0
    leggibilita = flesch_reading_ease(testo)  # Calcolo del punteggio di leggibilità
    return {
        "numero_parole": num_parole,
        "numero_hashtag": num_hashtag,
        "diversita_lessicale": diversita_lessicale,
        "leggibilita": leggibilita,
        "lista_hashtag": hashtag
    }

# Funzione per calcolare statistiche descrittive
def calcola_statistiche(lista_valori):
    """Calcola statistiche descrittive per una lista di valori numerici."""
    return {
        "media": mean(lista_valori),
        "mediana": median(lista_valori),
        "moda": mode(lista_valori) if len(set(lista_valori)) > 1 else "No moda",
        "varianza": variance(lista_valori) if len(lista_valori) > 1 else 0,
        "deviazione_standard": stdev(lista_valori) if len(lista_valori) > 1 else 0
    }

# Funzione principale
def analizza_dataset(file_path):
    """Analizza un dataset CSV e calcola statistiche descrittive."""
    try:
        df = pd.read_csv(file_path, sep=";")
    except FileNotFoundError:
        print(f"Errore: File non trovato: {file_path}")
        return None
    except pd.errors.ParserError:
        print(f"Errore: File non parsabile. Assicurarsi che sia un CSV valido.")
        return None

    if 'text' not in df.columns:
        print("Errore: La colonna 'text' non è presente nel dataset.")
        return None

    # Analisi statistica del testo
    df['analisi_statistica'] = df['text'].apply(analisi_testo)

    # Estrazione dei valori calcolati
    valori_numero_parole = [stat['numero_parole'] for stat in df['analisi_statistica']]
    valori_numero_hashtag = [stat['numero_hashtag'] for stat in df['analisi_statistica']]
    valori_diversita_lessicale = [stat['diversita_lessicale'] for stat in df['analisi_statistica']]
    valori_leggibilita = [stat['leggibilita'] for stat in df['analisi_statistica']]

    # Calcolo statistiche descrittive
    statistiche = {
        "numero_parole": calcola_statistiche(valori_numero_parole),
        "numero_hashtag": calcola_statistiche(valori_numero_hashtag),
        "diversita_lessicale": calcola_statistiche(valori_diversita_lessicale),
        "leggibilita": calcola_statistiche(valori_leggibilita)
    }

    return df, statistiche


file_path = "/content/Sentiment_en_tweet_2023.csv"
df_risultati, statistiche_risultati = analizza_dataset(file_path)

if df_risultati is not None:
    print("Dataset analizzato con successo!")
    

    print("\nStatistiche descrittive:")
    for chiave, valori in statistiche_risultati.items():
        print(f"\n{chiave.capitalize()}:")
        for metrica, valore in valori.items():
            print(f"  {metrica.capitalize()}: {valore}")
else:
    print("Analisi non eseguita.")

#ANALISI DATASET SINTETICO
# CAPITOLO 5 ANALISI SINTATTICA
#CALCOLO DEI PARAMETRI SUL DATASER REALE
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import string
from statistics import mean, median, mode, variance, stdev

nltk.download('punkt')

# Funzione per contare le sillabe in una parola
def conta_sillabe(parola):
    vocali = "aeiouy"
    parola = parola.lower().strip(string.punctuation)
    sillabe = 0
    ultima_e = parola.endswith("e")

    for i, lettera in enumerate(parola):
        if lettera in vocali:
            if i == 0 or parola[i-1] not in vocali:
                sillabe += 1
    if ultima_e and sillabe > 1:
        sillabe -= 1
    return sillabe

# Funzione per calcolare il punteggio Flesch Reading Ease
def flesch_reading_ease(testo):
    parole = word_tokenize(testo)
    frasi = sent_tokenize(testo)
    num_parole = len(parole)
    num_frasi = len(frasi)
    num_sillabe = sum(conta_sillabe(parola) for parola in parole if parola.isalpha())

    if num_parole == 0 or num_frasi == 0:  # Evita divisioni per zero
        return 0

    return 206.835 - 1.015 * (num_parole / num_frasi) - 84.6 * (num_sillabe / num_parole)

# Funzione per analisi statistica del testo
def analisi_testo(testo):
    testo = testo.lower()  
    parole = word_tokenize(testo)  # Tokenizzazione del testo
    hashtag = [word for word in parole if word.startswith('#')]  # Individua gli hashtag
    num_parole = len(parole)
    num_hashtag = len(hashtag)
    diversita_lessicale = len(set(parole)) / num_parole if num_parole > 0 else 0
    leggibilita = flesch_reading_ease(testo)  # Calcolo del punteggio di leggibilità
    return {
        "numero_parole": num_parole,
        "numero_hashtag": num_hashtag,
        "diversita_lessicale": diversita_lessicale,
        "leggibilita": leggibilita,
        "lista_hashtag": hashtag
    }

# Funzione per calcolare statistiche descrittive
def calcola_statistiche(lista_valori):
    """Calcola statistiche descrittive per una lista di valori numerici."""
    return {
        "media": mean(lista_valori),
        "mediana": median(lista_valori),
        "moda": mode(lista_valori) if len(set(lista_valori)) > 1 else "No moda",
        "varianza": variance(lista_valori) if len(lista_valori) > 1 else 0,
        "deviazione_standard": stdev(lista_valori) if len(lista_valori) > 1 else 0
    }

# Funzione principale
def analizza_dataset(file_path):
    """Analizza un dataset CSV e calcola statistiche descrittive."""
    try:
        df = pd.read_csv(file_path, sep=";")
    except FileNotFoundError:
        print(f"Errore: File non trovato: {file_path}")
        return None
    except pd.errors.ParserError:
        print(f"Errore: File non parsabile. Assicurarsi che sia un CSV valido.")
        return None

    if 'text' not in df.columns:
        print("Errore: La colonna 'text' non è presente nel dataset.")
        return None

    # Analisi statistica del testo
    df['analisi_statistica'] = df['text'].apply(analisi_testo)

    # Estrazione dei valori calcolati
    valori_numero_parole = [stat['numero_parole'] for stat in df['analisi_statistica']]
    valori_numero_hashtag = [stat['numero_hashtag'] for stat in df['analisi_statistica']]
    valori_diversita_lessicale = [stat['diversita_lessicale'] for stat in df['analisi_statistica']]
    valori_leggibilita = [stat['leggibilita'] for stat in df['analisi_statistica']]

    # Calcolo statistiche descrittive
    statistiche = {
        "numero_parole": calcola_statistiche(valori_numero_parole),
        "numero_hashtag": calcola_statistiche(valori_numero_hashtag),
        "diversita_lessicale": calcola_statistiche(valori_diversita_lessicale),
        "leggibilita": calcola_statistiche(valori_leggibilita)
    }

    return df, statistiche


file_path = "/content/sintetico.csv"
df_risultati, statistiche_risultati = analizza_dataset(file_path)

if df_risultati is not None:
    print("Dataset analizzato con successo!")
    

    print("\nStatistiche descrittive:")
    for chiave, valori in statistiche_risultati.items():
        print(f"\n{chiave.capitalize()}:")
        for metrica, valore in valori.items():
            print(f"  {metrica.capitalize()}: {valore}")
else:
    print("Analisi non eseguita.")

