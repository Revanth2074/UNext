#!/bin/bash

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "    Password Constraints Checker .sh"
echo "=========================================="
echo -n "Enter the password to check: "
read -s password
echo

# Define constraints
MIN_LENGTH=12
score=0

# 1. Check Length
length=${#password}
if [ "$length" -ge "$MIN_LENGTH" ]; then
    echo -e "${GREEN}[✔] Length: $length characters (Minimum is $MIN_LENGTH)${NC}"
    ((score++))
else
    echo -e "${RED}[✖] Length: $length characters (Must be at least $MIN_LENGTH)${NC}"
fi

# 2. Check for Uppercase Letter
if [[ "$password" =~ [A-Z] ]]; then
    echo -e "${GREEN}[✔] Uppercase letter found${NC}"
    ((score++))
else
    echo -e "${RED}[✖] Missing at least one uppercase letter (A-Z)${NC}"
fi

# 3. Check for Lowercase Letter
if [[ "$password" =~ [a-z] ]]; then
    echo -e "${GREEN}[✔] Lowercase letter found${NC}"
    ((score++))
else
    echo -e "${RED}[✖] Missing at least one lowercase letter (a-z)${NC}"
fi

# 4. Check for Numbers
if [[ "$password" =~ [0-9] ]]; then
    echo -e "${GREEN}[✔] Number found${NC}"
    ((score++))
else
    echo -e "${RED}[✖] Missing at least one number (0-9)${NC}"
fi

# 5. Check for Special Characters
if [[ "$password" =~ [[:punct:]] ]]; then
    echo -e "${GREEN}[✔] Special character found${NC}"
    ((score++))
else
    echo -e "${RED}[✖] Missing at least one special character (e.g., !@#$%^&*)${NC}"
fi

# Final Evaluation
echo "=========================================="
if [ "$score" -eq 5 ]; then
    echo -e "${GREEN}SUCCESS: Password meets all constraints!${NC}"
    exit 0
else
    echo -e "${YELLOW}WARNING: Password failed $((5 - score)) constraint(s).${NC}"
    exit 1
fi
