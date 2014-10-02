import numpy as np

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

# Define winrate
# (Set as a range for illustrative purposes)
delta = 0.001
win_rate = np.arange(0,1+delta,delta)

# define entry fee (dollars)
entry_fee = 1.

# games per hour
gph = 7.

# Define prob of getting a prize
prob_prize  = np.zeros(6)
prob_prize[0] = 9./10
prob_prize[1] = (1-prob_prize[0])/1.8758
prob_prize[2] = (1-prob_prize[0])/(2.*1.8758)
prob_prize[3] = (1-prob_prize[0])/(4.*1.8758)
prob_prize[4] = (1-prob_prize[0])/(8.*1.8758)
prob_prize[5] = (1-prob_prize[0])/(1250.*1.8758)

# Check probabilites sum to one
if np.sum(prob_prize)!=1: print "error: sum prob != 1"

# Define Prize Structure
prize  = np.zeros(6)
prize[0] = 2.
prize[1] = 4.
prize[2] = 6.
prize[3] = 12.
prize[4] = 24.
prize[5] = 1200.

# calculate earnings per hour based on winrate
eph_vs_winrate=np.zeros(len(win_rate))
for i in range(len(win_rate)):
    eph_vs_winrate[i]=earnings_per_hour(prize,prob_prize,win_rate[i],entry_fee,gph)

# find break even point (i.e. where eph = 0.i for a given win rate)
import bisect
break_point= win_rate[bisect.bisect(eph_vs_winrate,0.)]

# find return at a given win rate (in this case 0.85)
# change the value to your win rate for a given prize structure to see you earnins per hour
spec_win_rate=1.
arg = np.argwhere(np.logical_and((win_rate > (spec_win_rate-delta)),(win_rate< spec_win_rate+delta)))
print arg
print win_rate[-1]
eph_val = eph_vs_winrate[arg]

# plotting section
import matplotlib.pyplot as plt
# plot graph
plt.plot(win_rate,eph_vs_winrate,label='earnings vs win rate')

#plot vertical line at brak even point
plt.plot( [break_point,break_point],[np.amin(eph_vs_winrate),0.],
        color='r',label='break even at win rate of '+str(break_point))

# plot horizontal line to show earnings per hour for a given win rate
plt.plot([spec_win_rate,spec_win_rate],[np.amin(eph_vs_winrate),eph_val],color='k')
plt.plot([0,spec_win_rate],[float(eph_val),eph_val],color='k'
        ,label=str(float(eph_val))+' $ at '+str(spec_win_rate)+' win rate')

# Graph labels and legend
plt.legend(loc=6,prop={'size':8})
plt.ylabel("earnings per hour")
plt.xlabel("win rate")
plt.show()
#plt.savefig("eph_vs_winrate_"+str(entry_fee)+"_dollar.pdf")
