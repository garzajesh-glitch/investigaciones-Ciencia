
library( dplyr)
library(ggplot2)

df <- read.csv("d3_aire01_49_1.csv")
df <- df[!is.na(df$NOx), ]

top10 <- df %>%
  group_by(Entidad) %>%
  summarise(NOx = sum(NOx), .groups = 'drop') %>%
  arrange(desc(NOx))%>%
  head(10)

ggplot(top10, aes(x = reorder(Entidad, NOx), y = NOx)) + geom_bar(stat = 'identity', fill = 'gray', color = 'black',linewidth = 0.8)+
  labs(x = 'Entidad Federativa', y = 'Emisiones de NOx (Toneladas)') +
  theme_minimal() +
  theme(panel.grid.minor = element_blank(), axis.text.x = element_text(angle = 45, hjust = 1))

