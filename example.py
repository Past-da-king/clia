def print_triangle(rows):
    for i in range(1, rows + 1):
        print(" " * (rows - i) + "/" + "  " * (i - 1) + "\\")
    print("/" + "__" * (rows - 1) + "\\")

print_triangle(5)
