# CLASSIFICAZIONE DEI TWEET IN BASE AGLI HASTAG
library(dplyr)
library(stringr)
mio_dataset<-read.csv(file.choose(), sep=";")
# Lista di hashtag per categoria
hashtags_pro_russia <- tolower(c("#IStandWithPutin", "#Novorossiya", "#RussianVictory", "#RussiaStrong", "#StopNATO", "#ZelenskiWarCriminal", "#ZOV", "#fukraine"))
hashtags_pro_ukraine <- tolower(c("#StandWithUkraine","#freeukraine", "#RussiaIsATerroristState", "#SlavaUkraini", "#StopRussia", "#UkraineWillWin", "#SupportUkraine", "#ArmUkraine", "#SaveUkraine"))
hashtags_no_war <- tolower(c("#NoWar", "#Peace", "#StopTheWar", "#EndTheWar", "#DiplomacyFirst", "#SayNoToWar"))


mio_dataset <- mio_dataset %>%
  mutate(text = tolower(text))  


count_hashtags <- function(text, hashtags) {
  sapply(hashtags, function(tag) str_count(text, fixed(tag)))
}

# Aggiunta delle colonne conteggio hashtag
mio_dataset <- mio_dataset %>%
  rowwise() %>%
  mutate(
    matched_no_war = sum(count_hashtags(text, hashtags_no_war)),
    matched_pro_russia = sum(count_hashtags(text, hashtags_pro_russia)),
    matched_pro_ukraine = sum(count_hashtags(text, hashtags_pro_ukraine))
  ) %>%
  ungroup()

# Classificazione dei tweet
mio_dataset <- mio_dataset %>%
  mutate(
    classification = case_when(
      matched_no_war > 0 ~ "No War",          # Priorità ai No War
      matched_pro_russia > 0 ~ "Pro-Russia",
      matched_pro_ukraine > 0 ~ "Pro-Ucraina",
      TRUE ~ "Non Classificato"
    )
  )

hashtags_da_escludere <- c("#tigraygenocide", "#justice4tigray")

# Filtrare i post che NON contengono gli hashtag specificati
mio_dataset <- mio_dataset %>%
  filter(!str_detect(tolower(text), paste(hashtags_da_escludere, collapse = "|")))


# Conteggio dei tweet per ciascuna classificazione
conteggio_classificazioni <- mio_dataset %>%
  group_by(classification) %>%
  summarise(count = n())

# Visualizzazione dei risultati
print(conteggio_classificazioni)
write.csv(mio_dataset, "mio_dataset_classificato.csv", row.names = FALSE)
