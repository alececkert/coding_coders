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
#print(barplot1)
#ggsave('barplot1.png')


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
  aes(x= ivy_league, y=networth, fill= ivy_league)+
  geom_col()+
  labs(
    x= "Ivy League Alumni",
    y= "Average Net Worth in USD",
    fill = 'Education'
  )+
  theme_clean()
    
print(barplot2)
ggsave('barplot.pdf')

#### BAR 3: net worth in y, each person by birth year in x

datawithyears <- read_csv('not_rich_with_birth_year_after_1920.csv')|>
  mutate(
    networth = as.numeric(networth),
    birthYear= as.numeric(birthYear),
    ivy_league = ifelse(ivy_league, "Ivy league", "Non-Ivy league"))

averages <- datawithyears|>
  group_by(birthYear, ivy_league)|>
  summarise(avg_networth = mean(networth,na.rm= TRUE))|>
  ungroup()

barplot3 <- ggplot(data= datawithyears)+
  aes(x=birthYear, y=networth, color=ivy_league)+
  geom_point(size = 0.5)+
  geom_line(data = averages, aes(x= birthYear, y= avg_networth, color= ivy_league), size=1)+
  scale_y_log10()+
  labs(
    x= "Year of Birth",
    y= "Net Worth in USD", 
    color = 'Education'
  )+
  theme_clean()

print(barplot3)
ggsave('scatterlineplot.pdf')
