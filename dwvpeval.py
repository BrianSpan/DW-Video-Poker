from dwdeal import * #functions for dealing
from dwclass import *
from dwnamehands import *
from dwmakehold import *

#variables
keep=[False]*5#which cards to hold. T=hold, F=discard
numberlist: list=[]
playerhand: list=[]

#######################################
# Main program
#######################################
rounds=(BANK//POT)
for round in range(rounds):
    
    dealing=True
    turns=0
    currpot=POT
    print("Starting Pot for this round: "+str(POT))  

    while dealing:
        turns+=1
        
        #get initial hand
        numberlist,playerhand=deal()
        handinfo=DWpokerinfo(playerhand)
   
        #display bet
        currpot-=BET
        sout="Round: {} Turn: {} Wagering: ${} New total: ${}"
        print(sout.format(round+1,turns,BET,currpot))
        #display hand
        displayhand=' '.join( ([rank+suit for rank,suit in display_card(playerhand)]))
        pay=PAYOUT[handinfo.handscore]*BET
        sout="{}\n{} - Payout:{}"
        print (sout.format(displayhand,NAMES[handinfo.handscore],str(pay)))

        if DEBUG:
            q.write(' '.join([rank+suit for rank,suit in playerhand])+" AC 2C 3C 4C 5C ") #fake cards to add extra hand
    
        #make swap 
        keep=makehold(handinfo)
        #print what we will be keeping
        print(' '.join(['HOLD' if _ else 'DROP' for _ in keep]))

        ########
        if DEBUG:
            q.write(str(keep) + "\n")
        ########
            
        #####
        #display second version of cards
        playerhand=makecards(swaphand(numberlist,keep))[0:5]
        handinfo=DWpokerinfo(playerhand)
        #precalc(playerhand)
    
        #payout
        pay=PAYOUT[handinfo.handscore]*BET
        
        sout=' '.join( ([rank+suit for rank,suit in display_card(playerhand)]))
        sout+=" "+NAMES[handinfo.handscore]
        sout+=" Payout:"+str(pay)
        currpot+=pay
        print (sout+"\nTotal Pot: "+str(currpot)+"\n")
 
        cond1=(handinfo.handscore>=STRAIGHTFLUSH)
        cond2=(turns>=MAXTURNS)
        cond3=(currpot<=LOSSLIMIT*POT)
        if any([cond1,cond2,cond3]):
            dealing=False
            results[round]=(turns,currpot)  

#Final results
totalrolls=0
total_pot=0
pot_number=1
for rolls,amount in results:
    print('Pot: ', str(pot_number),'. Number of rolls: ',str(rolls),'. Amount: $',str(amount))
    pot_number+=1
print('Total rolls: ',sum(rolls for rolls,amount in results))    
print('Total take: $',sum(amount for rolls,amount in results))     

if TESTMODE:
    d.close()
if DEBUG:
    q.close()
    