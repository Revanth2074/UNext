#bookstore maintains its inventory in a text file named books.txt 
# view all books, search for a book, Count books that are out of stock, update the stock status, and calculate the total value of books in stock, Display books by category, find the constliest book in the inventory.

books_file="books.txt"

show_menu() {
    echo "\nBookstore Inventory Menu"
    echo "1) View all books"
    echo "2) Search for a book"
    echo "3) Count out-of-stock books"
    echo "4) Update book stock status"
    echo "5) Calculate total inventory value"
    echo "6) Display books by category"
    echo "7) Find the costliest book"
    echo "8) Exit"
}

view_all_books() {
    printf "%-5s %-30s %-15s %-12s %-8s\n" "ID" "Title" "Category" "Status" "Price"
    echo "--------------------------------------------------------------------------------"
    awk -F"," '{printf "%-5s %-30s %-15s %-12s %-8s\n", $1, $2, $3, $4, $5}' "$books_file"
}

search_book() {
    read -p "Enter book title or ID to search: " query
    awk -F"," -v q="$query" 'BEGIN {IGNORECASE = 1} $1 == q || index(tolower($2), tolower(q)) {
        printf "\nFound: %-5s %-30s %-15s %-12s %-8s\n", $1, $2, $3, $4, $5
    }' "$books_file"
}

count_out_of_stock() {
    count=$(awk -F"," 'tolower($4) == "outofstock" || tolower($4) == "out of stock" {count++} END {print count+0}' "$books_file")
    echo "\nOut-of-stock books: $count"
}

update_stock_status() {
    read -p "Enter book ID to update: " book_id
    if ! grep -qE "^$book_id," "$books_file"; then
        echo "Book ID $book_id not found."
        return
    fi
    read -p "Enter new status (Available / OutOfStock): " new_status
    if [[ ! "$new_status" =~ ^(Available|OutOfStock|Out\s*Of\s*Stock)$ ]]; then
        echo "Invalid status. Use Available or OutOfStock."
        return
    fi
    tmp_file=$(mktemp)
    awk -F"," -v id="$book_id" -v status="$new_status" 'BEGIN {OFS=FS} $1 == id {$4 = status} {print}' "$books_file" > "$tmp_file"
    mv "$tmp_file" "$books_file"
    echo "Book status updated for ID $book_id."
}

calculate_total_value() {
    total=$(awk -F"," 'tolower($4) == "available" {sum += $5} END {print sum+0}' "$books_file")
    echo "\nTotal value of books in stock: $total"
}

display_by_category() {
    read -p "Enter category: " category
    printf "\n%-5s %-30s %-15s %-12s %-8s\n" "ID" "Title" "Category" "Status" "Price"
    echo "--------------------------------------------------------------------------------"
    awk -F"," -v cat="${category,,}" 'BEGIN {IGNORECASE = 1} tolower($3) == cat {printf "%-5s %-30s %-15s %-12s %-8s\n", $1, $2, $3, $4, $5}' "$books_file"
}

find_costliest_book() {
    awk -F"," 'BEGIN {max=-1} {if ($5+0 > max) {max=$5+0; line=$0}} END {if (max >= 0) {split(line, a, ","); printf "\nCostliest book: %-5s %-30s %-15s %-12s %-8s\n", a[1], a[2], a[3], a[4], a[5]}}' "$books_file"
}

while true; do
    show_menu
    read -p "Choose an option [1-8]: " choice
    case "$choice" in
        1) view_all_books ;;
        2) search_book ;;
        3) count_out_of_stock ;;
        4) update_stock_status ;;
        5) calculate_total_value ;;
        6) display_by_category ;;
        7) find_costliest_book ;;
        8) echo "Exiting..."; break ;;
        *) echo "Invalid selection. Please choose 1-8." ;;
    esac
done


