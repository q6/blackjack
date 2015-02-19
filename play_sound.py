import winsound

# for i in range(1, 6):
#     winsound.Beep(i*1000, 1000)


lst = [1, 2, 3, 3, 2, 1, 3, 2, 5, 5, 4, 3, 2, 1]
lst = [3, 3, 4, 5, 3, 2, 1]
lst = range(20, 40)
lst = [10, 15, 17, 16, 15, 3, 3, 3]

for i in lst:
    winsound.Beep(i*100, 100)

