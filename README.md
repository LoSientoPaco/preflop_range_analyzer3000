# preflop_range_analyzer3000
 Input the wanted ranges and hand history and see if you are playing the ranges you want to play!

pip install jsonstream -- required


Current Use:

In holdem manager (or your preferred tracker program) go to reports and choose positional reports for hero (you).

make sure to filter correctly for what you want to analyze. Want to analyze your cold calling range from the btn? This is where you filter for that

Select all the hands you want to analyze from that position and export the hands as a .ohh

save that file to /hands/ directory and update the config file. 

Make your range file like in the example. 

https://www.pokerhandrange.com/ is a resource that may prove useful. 

update the config file. 


run the program: python ./src/main.py

see the outputs in the ./outputs/ directory

Notes:
- if you want to look at your SB limping/Raising strat filter correctly in Holdem Manager. 

- does not account for you calling others limps, will just print that you called this hand preflop

- if you want to see how you play BTN vs CO as the BTN, filter in holdem manager for that situation then make the wanted range. 

LIMITATIONs/Future Updates:
- does not account for frequency plays > however you can see your frequencies from the stats given. 
- does not account for 4-bets
- does not account for getting 3-bet or your response to said 3 bet, aka if there is a raise then 3bet the hand will not be counted in 
  analysis. This can be updated in a future update. 
