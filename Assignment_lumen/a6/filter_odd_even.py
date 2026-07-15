player_ids = [101, 102, 103, 104, 105]

odd_ids = list(filter(lambda x: x % 2 != 0, player_ids))

print("Odd Player IDs:")
print(odd_ids)