setwd("~/Documentos/Projetos Extras/Análise de sentimentos")

#library(rtweet)
library(wordcloud)
library(tm)
library(RColorBrewer)
library(cluster)   
library(fpc)
library(tidyverse)
library(dplyr)
library(ggplot2)
library(lubridate)
#------------------------------------------------------------------------------------------------------------

# EXTRACTED USING PYTHON (snscrape)


tweets_btc <- read.csv("bitcoin_tweets_old.csv") 
#tweets_btc <- read.csv("bitcoin_tweets_complete.csv") 
dim(tweets_btc)
names(tweets_btc)


# VIZUALISING THE FREQUENCY OF TWEETS 

tweets_btc$date_ymd_hms <- lubridate::ymd_hms(tweets_btc$date)
tweets_btc$date_formated <- as.Date(tweets_btc$date)

freq_tweets_by_date <- tweets_btc %>% 
  dplyr::group_by(date_formated) %>% 
  dplyr::count() 


freq_tweets_by_date <- as.data.frame(freq_tweets_by_date)
freq_tweets_by_date$date_formated = as.POSIXct(freq_tweets_by_date$date_formated)
freq_tweets_by_date <- freq_tweets_by_date %>%  dplyr::rename("Date"= date_formated)
freq_tweets_by_date <- freq_tweets_by_date %>%  dplyr::rename("Freq"= n) 

ggplot() +
  geom_line(data = freq_tweets_by_date, aes(Date, Freq), size = 0.125, color = 'blue') +
  scale_x_datetime(date_labels = "%b/%y") +

  labs(x = "Data", y = "Count", 
       title = 'Number of tweets by date') + theme_minimal()







#-----------------------------------------------------------------------------------------------

# WORKING ON THE TEXT MINING


tweets_text <- tweets_btc %>%  dplyr::filter(lang == 'en') %>%  select(content) # the text mining will work better in english

## First cleaning
tweets_text_corpus <- VCorpus(VectorSource(tweets_text)) #creating corpus

tweets_text_corpus <- tm_map(tweets_text_corpus,
                             content_transformer(function(x) iconv(x, to = 'UTF-8', sub = 'byte'))) #encoding all text to


tweets_text_corpus <- tm_map(tweets_text_corpus, content_transformer(tolower)) # making all text to be lowercased
tweets_text_corpus <- tm_map(tweets_text_corpus, removePunctuation) # removing punctuation from all tweets
tweets_text_corpus <- tm_map(tweets_text_corpus,removeWords, stopwords("english")) # removing english stop words

## Visualizing the text data
WC_colors <- brewer.pal(8,"Dark2")

Wordcloud_tweets <- wordcloud(tweets_text_corpus,min.freq = 2,max.words = 100, random.order = TRUE,colors = WC_colors)


# Cleaning with DocumentTermMatrix
tweets_dtm <- DocumentTermMatrix(tweets_text_corpus)   

tweets_freq <- colSums(as.matrix(tweets_dtm))

length(tweets_freq) 
tail(tweets_freq,10) # apparently it some tweets are in other language 
head(tweets_freq)

tweets_dtms <- removeSparseTerms(tweets_dtm, 0.98)  # removing low occurrence terms

tweets_dtms <- colSums(as.matrix(tweets_dtms))   
length(tweets_freq) 
# tweets_freq <- sort(colSums(as.matrix(tweets_dtms)), decreasing = T) 

#View(as.data.frame(tweets_freq))


## converting matrix to DataFrame with the porpose of ploting

tweets_plot <- data.frame(word = names(tweets_freq), freq = tweets_freq)  

dev.off() # I was getting the error Error in .Call.graphics(C_palette2, .Call(C_palette2, NULL)) : invalid graphics state

ggplot(subset(tweets_plot, tweets_freq > 1000), aes(x = reorder(word, -freq), y = freq)) +
  geom_bar(stat = "identity") + 
  theme(axis.text.x = element_text(angle = 45 , hjust = 1)) +
  ggtitle("Barplot with most frequent terms") +
  labs(y = "Frequency", x = "Terms")


## filtering by context 
tweets_text_corpus_v2 <- tm_map(tweets_text_corpus, removeWords, c("bitcoin","btc")) #removing obivious words


tweets_dtms_v2 <- removeSparseTerms(DocumentTermMatrix(tweets_text_corpus_v2) , 0.98) 


tweets_freq_v2 <- colSums(as.matrix(tweets_dtms_v2))   


tweets_plot_V2 <- data.frame(word=names(tweets_freq_v2), freq = tweets_freq_v2)  

tweets_plot_V2 <- tweets_plot_V2 %>%  dplyr::arrange(desc(freq))

ggplot(subset(tweets_plot_V2, tweets_freq > 1000), aes(x = reorder(word, -freq), y = freq)) +
  geom_bar(stat = "identity") + 
  theme(axis.text.x = element_text(angle = 45 , hjust = 1)) +
  ggtitle("Barplot with most frequent terms") +
  labs(y = "Frequency", x = "Terms")

new_tweets_wordcloud <- wordcloud(names(tweets_freq_v2), tweets_freq_v2, min.freq = 2, max.words = 100, random.order = T, colors = WC_colors)




#--------------------------------------------------------------------------------------------------------

# CLUSTER ANALYSIS

tweets_dtms_v3 <- removeSparseTerms(tweets_dtms_v2 , 0.80) 
dist <- dist(t(tweets_dtms_v3), method = "euclidian")   
dendogram <- hclust(d = dist, method = "complete")

plot(dendogram, hang = -1, main = "Dendograma Bitcoin tweets",
     xlab = "Distance",
     ylab = "High")  
#save(tweets_dtms_v3, file = "tweets_dtms_v3.RData")



