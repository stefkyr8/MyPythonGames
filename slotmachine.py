import random

MAX_LINES=3
MAX_BET=1000
MIN_BET=1

ROWS=3
COLS=3

symbol_count={
   'A': 2,
   'B': 4,
   'C': 6,
   'D': 8,
}
symbol_values={
   'A': 5,
   'B': 4,
   'C': 3,
   'D': 2,
}

def check_winnings(colums,lines,bet,values):
    winnings=0
    winning_lines=[]
    for line in range(lines):
        symbol=colums[0][line]
        for colum in colums:
          symbol_to_check=colum[line]
          if symbol!= symbol_to_check:
             break
        else:
            winnings+=values[symbol]*bet
            winning_lines.append(line+1)
       
    return winnings,winning_lines

def get_slot_machine_spin(rows,cols,symblols):
   all_symbols=[]
   for symbol,symbol_count in symblols.items():
      for _ in range(symbol_count):
         all_symbols.append(symbol)
   
   colums=[] 
   for _ in range(cols):
      coloum=[]
      curent_symbols=all_symbols[:]
      for _ in range(rows):
         value=random.choice(curent_symbols)
         curent_symbols.remove(value)
         coloum.append(value)
      
      colums.append(coloum)
   
   return colums

def printt_slot_machine(colums):
   for row in range(len(colums[0])):
      for i,colum in enumerate(colums):
         if i != len(colums)-1: 
           print(colum[row] ,end=" | ")
         else:
            print(colum[row], end="" )  
      
      print()
    

def deposit():
    while True:
        amount= input("Give us a deposit: $ ")
        if amount.isdigit():
            amount=int(amount)
            if amount>0:
                break
            else: 
              print("infalid amount") 
        else:
         print("Enter a number")

    return amount

def get_number_of_lines(): 
    while True:
        lines= input("Enter a number of lines to bet on(1-"+ str(MAX_LINES)+') ')

        if lines.isdigit():
            lines=int(lines)
            if 1<=lines<= MAX_LINES:
                break
            else: 
              print("invalid number of lines") 
        else:
         print("Enter a number")

    return lines


def get_bet():
    while True:
        amount= input("What would you like to bet? ")
        if amount.isdigit():
            amount=int(amount)
            if MIN_BET<= amount<=MAX_BET:
                break
            else: 
              print(f"Amount must be between $ {MIN_BET} - $ {MAX_BET}") 
        else:
         print("Enter a number")

    return amount
   
def spin(balance):
    lines=get_number_of_lines()
    while True:
      bet=get_bet()
      total_bet=bet*lines
      if total_bet>balance:
         print(f"You don't have enough to bet that amount, your curent balance is {balance}")
      else:
         break   
    print(f"You are betting $ {bet} on {lines} lines. Total bet  = {total_bet} $")

    slots=get_slot_machine_spin(ROWS,COLS,symbol_count)
    printt_slot_machine(slots)

    winnings,winning_lines=check_winnings(slots,lines,bet,symbol_values)
    print(f"You won $ {winnings}")
    print(f"You won on lines:", *winning_lines)
    return winnings-total_bet


def main():
   balance=deposit()
   while True:
      print(f"Current balance is $ {balance}")
      answer=input("Press enter to play (q to quit) ")
      if answer=="q":
         break
      balance+=spin(balance)
   print(f"You left with $ {balance}") 

main()