#!/bin/bash

balance=1000

while true
do
    echo "======================"
    echo "      ATM MENU"
    echo "======================"
    echo "1. Check Balance"
    echo "2. Deposit Money"
    echo "3. Withdraw Money"
    echo "4. Exit"
    echo "Enter your choice:"
    read choice

    case $choice in
        1)
            echo "Current Balance: Rs. $balance"
            ;;
        2)
            echo "Enter amount to deposit:"
            read deposit
            balance=$((balance + deposit))
            echo "Deposit Successful!"
            echo "Updated Balance: Rs. $balance"
            ;;
        3)
            echo "Enter amount to withdraw:"
            read withdraw

            if [ $withdraw -le $balance ]; then
                balance=$((balance - withdraw))
                echo "Withdrawal Successful!"
                echo "Remaining Balance: Rs. $balance"
            else
                echo "Insufficient Balance!"
            fi
            ;;
        4)
            echo "Thank You for Using ATM."
            break
            ;;
        *)
            echo "Invalid Choice! Please try again."
            ;;
    esac
done
