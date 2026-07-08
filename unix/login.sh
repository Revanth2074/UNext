#!/bin/bash

correct_user="admin"
correct_pass="1234"

attempt=0
max_attempts=3

while [ $attempt -lt $max_attempts ]
do
    echo "Enter Username:"
    read user

    echo "Enter Password:"
    read pass

    if [ "$user" = "$correct_user" ] && [ "$pass" = "$correct_pass" ]; then
        echo "Login Successful!"
        exit 0
    else
        attempt=$((attempt + 1))
        remaining=$((max_attempts - attempt))
        echo "Invalid Username or Password!"
        
        if [ $remaining -gt 0 ]; then
            echo "Attempts left: $remaining"
        fi
    fi
done

echo "Account Locked! You entered wrong credentials 3 times."
