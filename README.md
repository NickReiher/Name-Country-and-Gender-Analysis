# Name, Country, and Gender Analysis
Taking lists of names, country, and gender from various sources, then doing data analysis on them.

Chicago Marathon 2018:

My first project was looking at finishers data fromm the 2018 Chicago Marathon. I used pandas to do most of the heavy lifting and plotly to visualize the data in map form.

I had to scrape and clean the data myself, eventually ending up with a csv file that has the full name and country (using the Olympic country code) of each of the more than 44,000 finishers. You can find this csv file here: https://github.com/NickVance/NameCountryGenderAnalysis/blob/master/Chicago_Marathon_2018_Results_Clean.txt

Then I did some analysis - you can find my code here: https://github.com/NickVance/NameCountryGenderAnalysis/blob/master/Names%20and%20Country%20Analysis%20-%20Chicago%20Marathon%20-%20GitHub.py

Finishers and Countries:
I was able to get data on 44573 finishers (I used unoffical results posted on the Chicago Marathon website as of October 8 - the day after the race).
Here are the countries with the most representation:
    Country  Count  Percent
114     USA  29129     65.4
71      MEX   2025      4.5
20      CAN   1411      3.2
43      GBR   1395      3.1
23      CHN   1227      2.8

You can see a map with all of the countries and their number of participants here:
https://plot.ly/~NickVance/2/_2018-chicago-marathon-finishers-by-country/#/

There were 19 countries that had exactly one finisher, and here's a map of them:
https://plot.ly/~NickVance/4

There was some interesting data surrounding gender. Of countries with more than 50 finishers (44 countries), only one had more women than men. That was the US, with 52 percent of the finishers being female. On the other end of the spectrum, you had India (12 percent female) and Spain (15 percent female). Here's a map with all 44 of those countries:
https://plot.ly/~NickVance/0/_2018-chicago-marathon-percentage-of-female-runners-by-country/#/

Looking at names, the most commmon names were:
     First Name  Total  USA  Non-USA  Percent USA
5983    Michael    661  577       84     0.872920
1851      David    466  344      122     0.738197
4015       John    435  383       52     0.880460
3783   Jennifer    348  328       20     0.942529
1776     Daniel    297  212       85     0.713805


I'm really interested in gender-neutral names, so I also looked at names that aren't exclusive to one gender. Andrea was an interesting one. Take a look:
First Name  Gender Country  Last Name  Count
680     Andrea  female     ARG          2      2
681     Andrea  female     AUS          2      2
682     Andrea  female     AUT          1      1
683     Andrea  female     BRA          3      3
684     Andrea  female     CAN          5      5
685     Andrea  female     CHL          2      2
686     Andrea  female     COL         10     10
687     Andrea  female     CRI          3      3
688     Andrea  female     DEU          2      2
689     Andrea  female     ECU          1      1
690     Andrea  female     ESP          1      1
691     Andrea  female     GBR          2      2
692     Andrea  female     GTM          4      4
693     Andrea  female     HRV          1      1
694     Andrea  female     MEX         11     11
695     Andrea  female     PAN          1      1
696     Andrea  female     USA         72     72
697     Andrea    male     ITA         18     18

Among the finishers it was an exclusively female name for all countries except Italy, where it was an exclusively male name.

When looking at the data, I was interested in what names were the most American. What names don't really exist elsewhere in the world? Of course this isn't an exhaustive sample, but at least for the finishers of the Chicago Marathon, here were the names with the most finishers where ALL the finishers were from the US:
First Name  Total  USA  Non-USA
6560     Joshua     84   84        0
6533      Molly     60   60        0
6532    Kristen     58   58        0
6653    Brandon     56   56        0
6588      Jenna     52   52        0

Ideas for future analysis / projects -
1 - Create an algorithm that guesses the country of origin based on information like gender, name, etc.
2 - Look at the data based on finishing time / place. Could look at how the country distribution changes based on how fast the runners are.
3 - Look at the same data for other marathons. Especially with gender ratios. Is a certain gender more or less likely to travel to different places?
4 - Look at how the data changes over time for the same race.
5 - Examine people by the languages of their countries. What languages are the most common? 
6 - How to deal with double names? Look at the various double names and see what interesting stuff comes out.
7 - Create a visualization of the words / names used.

Issues with the Data - The country of origin is self-reporting. And I don't know if that is based on citizenship (and dual citizens exist), place of birth, residency, etc. For example, I am from the US but have German residency. Would I be listed under USA or Germany?

Issues with the code - One issue I ran into was the country codes not matching the ISO3 country codes (which plotly uses for their global maps). So I had to manually look at the country codes (about 1/3 of them) that were different. There might have been a faster way to do that.
