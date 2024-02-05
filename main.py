p = [1, 2, 3, 4]
z = 0
for i in p:
    if z < 3:
        p.append(9)
        z += 1
    print(i)