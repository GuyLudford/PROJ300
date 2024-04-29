my_2d_list = [[1, 2, 3], [10, 20, 30]]

# Unpack the internal lists using zip()
for first_value, second_value in zip(*my_2d_list):
    print(f"First value: {first_value}, Second value: {second_value}")
