
# Funzione per caricare un file CSV
load_csv_file <- function(file_path) {
  # Controlla se il file esiste
  if (file.exists(file_path)) {
    cat("Il file è stato trovato:", file_path, "\n")
    
    # Prova a leggere il file CSV con il separatore ';'
    df_imported <- try(read.csv(file_path, sep = ";"))
    
    # Verifica se ci sono stati errori nel caricamento
    if (inherits(df_imported, "try-error")) {
      cat("Errore nel caricamento del file. Potrebbero esserci righe malformattate o vuote.\n")
      return(NULL)  # Restituisce NULL in caso di errore
    } else {
      cat("Contenuto del file CSV:\n")
      print(head(df_imported))  # Visualizza le prime righe del DataFrame
      return(df_imported)  # Restituisce l'intero dataset
    }
  } else {
    cat("Il file non è stato trovato:", file_path, "\n")
    return(NULL)  # Restituisce NULL se il file non è stato trovato
  }
}

# Funzione per calcolare la media e la deviazione standard di un vettore numerico
calculate_stats <- function(numbers) {
  # Verifica che l'input sia un vettore numerico
  if (!is.numeric(numbers)) {
    stop("L'input deve essere un vettore numerico.")
  }
  
  # Rimuovi i valori NA prima di calcolare la media e la deviazione standard
  numbers_clean <- na.omit(numbers)
  
  # Calcola la media e la deviazione standard
  mean_value <- mean(numbers_clean)
  sd_value <- sd(numbers_clean)
  
  # Restituisci i risultati come lista
  result <- list(mean = mean_value, sd = sd_value)
  
  # Stampa i risultati
  cat("Media:", mean_value, "\n")
  cat("Deviazione Standard:", sd_value, "\n")
  
  return(result)
}

# Funzione per calcolare e stampare gli indici di sintesi
sintesi_feature <- function(data, feature_name) {
  # Controlla se la colonna esiste
  if (!feature_name %in% colnames(data)) {
    stop("La colonna specificata non esiste nel dataframe.")
  }
  
  # Estrai la colonna
  feature <- data[[feature_name]]
  
  # Calcola gli indici di sintesi
  sintesi <- list(
    Minimo = min(feature, na.rm = TRUE),
    Massimo = max(feature, na.rm = TRUE),
    Media = mean(feature, na.rm = TRUE),
    Mediana = median(feature, na.rm = TRUE),
    Varianza = var(feature, na.rm = TRUE),
    Deviazione_Standard = sd(feature, na.rm = TRUE),
    Range = diff(range(feature, na.rm = TRUE)),
    Quartile_1 = quantile(feature, 0.25, na.rm = TRUE),
    Quartile_3 = quantile(feature, 0.75, na.rm = TRUE)
  )
  
  # Stampa gli indici in modo ordinato
  cat("\nIndici di sintesi per la colonna:", feature_name, "\n")
  cat("-----------------------------------\n")
  for (indice in names(sintesi)) {
    cat(indice, ":", sintesi[[indice]], "\n")
  }
}

# Funzione per mostrare la distribuzione di un valore
disegna_hist <- function(data, feature_name) {
  # Controlla se la colonna esiste
  if (!feature_name %in% colnames(data)) {
    stop("La colonna specificata non esiste nel dataframe.")
  }
  
  # Estrai la colonna
  feature <- data[[feature_name]]
  
  # Verifica che la colonna contenga dati numerici
  if (!is.numeric(feature)) {
    stop("La colonna specificata deve essere numerica.")
  }
  
  # Creazione del grafico
  hist(feature, 
       breaks = 10, 
       probability = TRUE, 
       main = paste("Distribuzione di", feature_name), 
       xlab = feature_name, 
       col = "skyblue", 
       border = "white")
  
  # Sovrapposizione della densità
  lines(density(feature, na.rm = TRUE), 
        col = "red", 
        lwd = 2)
  
  # Messaggio per confermare la generazione del grafico
  cat("Grafico della distribuzione generato per:", feature_name, "\n")
}

# Funzione per disegnare un Kernel Density Estimation (KDE)
disegna_kde <- function(data, feature_name) {
  # Controlla se la colonna esiste
  if (!feature_name %in% colnames(data)) {
    stop("La colonna specificata non esiste nel dataframe.")
  }
  
  # Estrai la colonna
  feature <- data[[feature_name]]
  
  # Verifica che la colonna contenga dati numerici
  if (!is.numeric(feature)) {
    stop("La colonna specificata deve essere numerica.")
  }
  
  # Creazione del grafico KDE
  plot(density(feature, na.rm = TRUE),
       main = paste("Kernel Density Estimation (KDE) per", feature_name),
       xlab = feature_name,
       ylab = "Densità",
       col = "blue", 
       lwd = 2)
  
  # Messaggio per confermare la generazione del grafico
  cat("Grafico KDE generato per:", feature_name, "\n")
}

# Funzione per disegnare un Boxplot
disegna_boxplot <- function(data, feature_name) {
  # Controlla se la colonna esiste
  if (!feature_name %in% colnames(data)) {
    stop("La colonna specificata non esiste nel dataframe.")
  }
  
  # Estrai la colonna
  feature <- data[[feature_name]]
  
  # Verifica che la colonna contenga dati numerici
  if (!is.numeric(feature)) {
    stop("La colonna specificata deve essere numerica.")
  }
  
  # Creazione del grafico Boxplot
  boxplot(feature, 
          main = paste("Boxplot Orizzontale per", feature_name),
          xlab = feature_name,
          col = "lightgreen", 
          border = "darkgreen",
          horizontal = TRUE)
  
  # Messaggio per confermare la generazione del grafico
  cat("Grafico Boxplot generato per:", feature_name, "\n")
}

# Funzione per disegnare un Boxplot della relazione tra first_column e second_column
disegna_boxplot_relazione <- function(data, first_column, second_column) {
  # Controlla se le colonne esistono
  if (!(first_column %in% colnames(data)) | !(second_column %in% colnames(data))) {
    stop("Una o entrambe le colonne non esistono nel dataframe.")
  }
  
  # Verifica se second_column è un fattore, se non lo è lo converte in fattore
  data[[second_column]] <- as.factor(data[[second_column]])
  
  # Creazione del boxplot
  boxplot(data[[first_column]] ~ data[[second_column]], 
          main = paste("Distribuzione di", first_column, "per", second_column),
          xlab = second_column,
          ylab = first_column,
          col = c("lightblue", "lightgreen", "lightcoral"), 
          border = "darkblue")
  
  # Messaggio per confermare la generazione del grafico
  cat("Boxplot generato per la relazione tra", first_column, "e", second_column, "\n")
}

cat("Funzioni caricate con successo")

