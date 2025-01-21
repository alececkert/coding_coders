#Script for plotting first results 

library(tidyverse)
library(scales)
library("ggthemes")

datafile <- read_csv('results.csv')

##BAR 1: per ivy league############
data_gr_per_ivy<- datafile|>
  group_by(almaMater)|>
  summarise(avg_networth = mean(networth))
  #filter(almaMater = (-University))
print(data_gr_per_ivy)

barplot1 <- ggplot(data= data_gr_per_ivy)+aes(x=almaMater,y=avg_networth)+
  geom_col()+
  xlab(NULL)+
  labs(
    color= 'Ivy League School',
    title='Average Net Worth of Ivy League Alumni on Wikipedia',
    y= "Average Net Worth in USD"
  )
print(barplot1)
ggsave('barplot1.png')


##BAR 2: all ivy leagues into one ######

datacombined <- read_csv('combined.csv')
data_divided<- datacombined |> 
  mutate(
    networth = as.numeric(networth),
    ivy_league = ifelse(ivy_league, "Ivy league", "Non-Ivy league")
  )|>
  group_by(ivy_league)|>
  summarise(networth=mean(networth,na.rm=TRUE))
print(data_divided)

barplot2 <- ggplot(data= data_divided)+
  aes(x= ivy_league, y=networth)+
  
  geom_col()+
  labs(
    title='Average Net Worth of Ivy League vs. Non-Ivy League Alumni on Wikipedia',
    x= "Ivy League Alumni",
    y= "Average Net Worth in USD"
  )
#print(barplot2)
ggsave('barplot2.png')
