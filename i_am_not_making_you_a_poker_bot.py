import numpy as np
import bisect
import matplotlib.pyplot as plt

# function to calculate earnings per hour given
# prizes, prob of each prize, entry fee ,win rate and number of games played per hour
def earnings_per_hour(prize,prob_prize,win_rate,entry,gph):

    # To calculate the expected prize if one wins
    # one takes the sum of each prize vs its corresponding probability
    e_v_win =  np.dot(prize,prob_prize)
    
    # Through multiplying by one's win rate one obtains 
    # expected return from one game 
    # i.e. if I played 100 games I would expect to win 100*win_rate of them
    # thus my payout is 100*win_rate*e_v_win
    e_v_exp = win_rate*e_v_win
    
    # one must also remember to minus entry fee
    # nothing in life is free etc..
    e_v_exp -= entry
    
    # then one multiplies by the number of games per hour
    #allowing one to obtain the expected earnings per hour
    eph = e_v_exp*gph
    
    return eph

""" Main code - calculates earnings per hour for a given win rate and prize structure"""
# read in spin_and_go data
path='spin_and_go_odds'
odds = np.loadtxt(path,unpack=True)

# normalise odds for each pay out
# ignore first column as prize factors
for i in range(1,len(odds)):odds[i]/=np.sum(odds[i])

# Define winrate
# (Set as a range for illustrative purposes)
delta = 0.001
win_rate = np.arange(0,1+delta,delta)

# define entry fee (dollars)
entry_fee = [1.,3.,7.,15.,30]

# games per hour
gph = 10.


for j in range(len(entry_fee)):
    prize = np.zeros(len(odds[0]))
    prize = odds[0]*entry_fee[j]

    # calculate earnings per hour based on winrate
    eph_vs_winrate=np.zeros(len(win_rate))
    for i in range(len(win_rate)):
        eph_vs_winrate[i]=earnings_per_hour(prize,odds[j+1],win_rate[i],entry_fee[j],gph)
    
    # find break even point (i.e. where eph = 0.0 for a given win rate)
    break_point= win_rate[bisect.bisect(eph_vs_winrate,0.)]
    
    # find return at a given win rate (in this case 0.85)
    # change the value to your win rate for a given prize structure to see you earnins per hour
    spec_win_rate=0.85
    arg = np.argwhere(np.logical_and((win_rate > (spec_win_rate-delta)),(win_rate< spec_win_rate+delta)))
    eph_val = eph_vs_winrate[arg]
    print "expected return with win rate of " +str(spec_win_rate)\
            +" at "+str(gph)+" games per hour = "+str(float(eph_val))+" $"
    # plotting section
    # plot graph
    plt.plot(win_rate,eph_vs_winrate,label='earnings vs win rate $'
            +str(entry_fee[j])+' entry')
    
    #plot vertical line at brak even point
    plt.plot( [break_point,break_point],[np.amin(eph_vs_winrate),0.],
            color='r',label='break even at win rate of '
            +str(break_point)+' $'+str(entry_fee[j])+' entry')
    
    # plot horizontal line to show earnings per hour for a given win rate
    plt.plot([spec_win_rate,spec_win_rate],[np.amin(eph_vs_winrate),eph_val],color='k')
    plt.plot([0,spec_win_rate],[float(eph_val),eph_val],color='k'
            ,label=str(float(eph_val))+' $ at '+str(spec_win_rate)+' win rate')
    
# Graph labels and legend
#plt.legend(loc=2,prop={'size':10})
plt.legend(loc=2)
plt.ylabel("earnings per hour")
plt.xlabel("win rate")
plt.show()
#plt.savefig("eph_vs_winrate_"+str(entry_fee)+"_dollar.pdf")
