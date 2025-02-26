#CLUSTER PRO-UCRAINA
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer


nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Caricamento e selezione dei dati
try:
    df = pd.read_csv('/content/mio_dataset_classificato.csv')
except FileNotFoundError:
    print("Errore: File 'mio_dataset_classificato.csv' non trovato.")
    exit()

if 'text' not in df.columns or 'classification' not in df.columns:
    print("Errore: Colonne 'text' o 'classification' non trovate.")
    exit()

# Seleziona solo i tweet "PRO-UCRAINA"
df_ucraina = df[df['classification'] == 'Pro-Ucraina'].copy()

if df_ucraina.empty:
    print("Nessun tweet trovato con classificazione 'Pro-Ucrina'.")
    exit()

# Preprocessing del testo
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'http\S+', '', text)  # Rimuovi URL
    text = re.sub(r'@\S+', '', text)  # Rimuovi menzioni
    text = re.sub(r'#\S+', '', text)  # Rimuovi hashtag
    text = re.sub(r'[\d]', '', text)  # Rimuovi numeri
    text = re.sub(r'[\W_]+', ' ', text)  # Rimuovi caratteri speciali
    text = text.lower()
    words = text.split()
    words = [word for word in words if word not in stop_words]  # Rimuovi stopwords
    words = [lemmatizer.lemmatize(word) for word in words]  # Lemmatizzazione
    return " ".join(words)

df_ucraina['tweet_preprocessed'] = df_ucraina['text'].apply(preprocess_text)

# Rappresentazione vettoriale con Sentence-BERT
model = SentenceTransformer('all-MiniLM-L6-v2')
X = model.encode(df_ucraina['tweet_preprocessed'].tolist())

# Metodo del Gomito per determinare il numero ottimale di cluster
inertia = []
range_n_clusters = range(2, 10)  # Testa da 2 a 10 cluster
for n_clusters in range_n_clusters:
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)
    inertia.append(kmeans.inertia_)

# Grafico del metodo del gomito
plt.figure(figsize=(8, 5))
plt.plot(range_n_clusters, inertia, marker='o')
plt.title('Metodo del Gomito')
plt.xlabel('Numero di Cluster')
plt.ylabel('Inertia')
plt.show()


optimal_clusters = 7  # numero scelto in base al grafico del gomito
print(f"Numero ottimale di cluster scelto: {optimal_clusters}")

# Clustering con K-Means
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
kmeans.fit(X)
df_ucraina['cluster'] = kmeans.labels_

# Analisi dei cluster
for cluster_id in range(optimal_clusters):
    cluster_tweets = df_ucraina[df_ucraina['cluster'] == cluster_id]
    print(f"\nCluster {cluster_id} ({len(cluster_tweets)} tweet):")
    print(cluster_tweets['text'].head(5))

# Parole chiave per cluster
for cluster_id in range(optimal_clusters):
    cluster_tweets = df_ucraina[df_ucraina['cluster'] == cluster_id]['tweet_preprocessed']
    vectorizer = TfidfVectorizer(max_features=10)
    tfidf_matrix = vectorizer.fit_transform(cluster_tweets)
    print(f"\nCluster {cluster_id} - Parole chiave:", vectorizer.get_feature_names_out())

# Esportazione dei risultati
df_ucraina.to_csv('tweet_no_war_clustered.csv', index=False)