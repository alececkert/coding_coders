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

barplot1 <- ggplot(data= data_gr_per_ivy)+aes(x=almaMater,y=avg_networth, color=almaMater)+
  geom_col()+
  labs(
    title='Average Net Worth of Ivy League Alumni on Wikipedia',
    x= "Ivy League",
    y= "Average Net Worth in USD"
  )
print(barplot1)
#ggsave('barplot1.png')


##BAR 2: all ivy leagues into one ######

datacombined <- read_csv('combined.csv')
data_divided<- datacombined |> 
  summarise(meanivy_league == True) |> 
  summarise(avg_netw = mean(networth))


barplot2 <- ggplot(data= data_grouped_all)+
  aes(x= data_ivy, data_nonivy, y=average_networth)+
  geom_col()+
  labs(
    title='Average Net Worth of Ivy League Alumni on Wikipedia',
    x= "Ivy League Alumni",
    y= "Average Net Worth in USD"
  )
#print(barplot2)

