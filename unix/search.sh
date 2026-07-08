# search a word form text.txt file and print the line number and the line containing the word
#!/bin/bash
search_word(){
    file=$1
    word=$2
    if grep -q "$word" "$file"; then
        echo "The word '$word' is found in the file '$file'."
        grep -n "$word" "$file"
    else
        echo "The word '$word' is not found in the file '$file'."
    fi
}

#occurrence of the word in the file
echo "Occurrences of 'linux' in 'text.txt':"
count=$(grep -o "linux" text.txt | wc -l)
echo "The word 'linux' occurs $count times in the file 'text.txt'."


search_word text.txt linux

