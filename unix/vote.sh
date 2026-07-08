#!/bin/bash

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Legal voting age constraint
VOTING_AGE=18

echo "=========================================="
echo "    Voting Eligibility Calculator"
echo "=========================================="
echo -n "Enter your date of birth (YYYY-MM-DD): "
read dob_input

# Validate YYYY-MM-DD format regex
if [[ ! "$dob_input" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo -e "${RED}[✖] Error: Invalid format. Please use YYYY-MM-DD (e.g., 2005-04-12).${NC}"
    exit 1
fi

# Validate if it is a real date using the 'date' utility
if ! date -d "$dob_input" >/dev/null 2>&1; then
    echo -e "${RED}[✖] Error: The date provided does not exist.${NC}"
    exit 1
fi

# Convert dates to Unix timestamps for precision
current_time=$(date +%s)
birth_time=$(date -d "$dob_input" +%s)

# Prevent future dates
if [ "$birth_time" -gt "$current_time" ]; then
    echo -e "${RED}[✖] Error: Date of birth cannot be in the future.${NC}"
    exit 1
fi

# Calculate age in years
current_year=$(date +%Y)
current_month=$(date +%m)
current_day=$(date +%d)

birth_year=$(date -d "$dob_input" +%Y)
birth_month=$(date -d "$dob_input" +%m)
birth_day=$(date -d "$dob_input" +%d)

age=$((current_year - birth_year))

# Adjust age if birth month/day hasn't occurred yet this year
if [ "$current_month" -lt "$birth_month" ] || { [ "$current_month" -eq "$birth_month" ] && [ "$current_day" -lt "$birth_day" ]; }; then
    ((age--))
fi

echo "=========================================="
echo -e "Calculated Age: ${YELLOW}$age years old${NC}"

# Final Voting Eligibility Logic
if [ "$age" -le 0 ]; then
    # Scenario: User was born earlier this year
    years_left=$VOTING_AGE
    echo -e "${RED}[✖] STATUS: NOT ELIGIBLE TO VOTE.${NC}"
    echo -e "You are a newborn! You will be eligible to register in $years_left years."
    exit 1
elif [ "$age" -ge "$VOTING_AGE" ]; then
    echo -e "${GREEN}[✔] STATUS: ELIGIBLE TO VOTE!${NC}"
    echo -e "Please ensure you are registered on the official electoral roll to cast your ballot."
    exit 0
else
    years_left=$((VOTING_AGE - age))
    echo -e "${RED}[✖] STATUS: NOT ELIGIBLE TO VOTE.${NC}"
    echo -e "You are a minor. You will be eligible to register in $years_left year(s)."
    exit 1
fi
