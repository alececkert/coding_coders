#Script for plotting first results 

library(tidyverse)
library(scales)
library("ggthemes")

datafile <- read_csv('results.csv')

##BAR 1: Difference in Net Worth WITHIN Ivy League Alumni############
## Note: not included in report, was the first plot we did#

datafile <- read_csv('results.csv')
#Simply grouping by the Ivy (almaMater), then averaging net worth per Ivy 
data_gr_per_ivy<- datafile|>
  group_by(almaMater)|>
  summarise(avg_networth = mean(networth))
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


##BAR 2: Difference in the average net worth of Ivy and Non-Ivy Students #########

datacombined <- read_csv('not_rich_with_birth_year_after_1920.csv') 
sum(datacombined$ivy_league, na.rm = TRUE)/nrow(datacombined)*100

#This dataframe has "true/false" established for each person, 
#filtering if they have an Ivy League within their academic history in Wiki
data_divided<- datacombined |> 
  mutate(
    networth = as.numeric(networth),
    #Transforming the true/false to what it stands for
    ivy_league = ifelse(ivy_league, "Ivy league", "Non-Ivy league")
  )|>
  group_by(ivy_league)

data_divided_mean<- data_divided |> 
  #Getting the networth average per section of alumni, excluding N/A entries
  summarise(networth=mean(networth,na.rm=TRUE))
print(data_divided)

barplot2 <- ggplot(data= data_divided_mean)+
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

violinplot <- ggplot(data= data_divided)+
  aes(x= ivy_league, y=networth, fill= ivy_league)+
  geom_violin()+
  labs(
    x= "Ivy League Alumni",
    y= "Average Net Worth in USD",
    fill = 'Education'
  )+
  scale_y_log10()+
  theme_clean()

print(violinplot)
ggsave('violin.pdf')
  

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


#####OVER 5 YEARS??
datawith5years <- read_csv('not_rich_with_birth_year_after_1920.csv') |>
  mutate(
    networth = as.numeric(networth),
    birthYear = as.numeric(birthYear),
    ivy_league = ifelse(ivy_league, "Ivy league", "Non-Ivy league")
  )

datawith5years <- datawithyears |>
  mutate(
    birthYearGroup = (birthYear %/% 5) * 5
  )


#1987 %/% 5 = 397.4 *5 = 1985
#1988 %/% 5 = 397.6 *5= 1985
#1990 %/% 5 = 398 *5 = 1990
#1991 %/% 5 = 398.2 *5 = 1990


averages_5yr <- datawith5years |>
  group_by(birthYearGroup, ivy_league) |>
  summarise(avg_networth = mean(networth, na.rm = TRUE)) |>
  ungroup()

scatterplot5yrinterval <- ggplot(data = datawith5years) +
  aes(x = birthYearGroup, y = networth, color = ivy_league) +
  geom_point(size = 0.5)+
  geom_line(data = averages_5yr, aes(x = birthYearGroup, y = avg_networth, color = ivy_league), size = 1) +
  scale_y_log10() +
  labs(
    x = "Birth Year (Grouped by 5-Year Intervals)",
    y = "Net Worth in USD",
    color = "Education"
  ) +
  theme_clean()

print(scatterplot5yrinterval)
ggsave('scatterlineplot_5yr.pdf')
