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
    } else {
      cat("Contenuto del file CSV:\n")
      print(head(df_imported))  # Visualizza le prime righe del DataFrame
    }
  } else {
    cat("Il file non è stato trovato:", file_path, "\n")
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

cat("Funzioni caricate con successo")

