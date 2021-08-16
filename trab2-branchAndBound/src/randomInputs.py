import sys
import random

def main(argv):
    n = int(argv[0])
    l = random.randint(1,2*n)
    m = random.randint(1,2**n)

    # Write on file
    f = open("n" + str(n) + ".txt","w+")
    f.write(f"{l} {m} {n}\n")

    # Iterates over actors
    for i in range(m):
        groups = []
        for j in range(l):
            groups.append(j+1)
        value = random.randint(0,100)
        len_sub = random.randint(1, l)

        f.write(f"{value} {len_sub}\n")
        for j in range(len_sub):
            group = random.choice(groups)
            groups.remove(group)
            f.write(f"{group}\n")

    f.close()
    

if __name__ == "__main__":
    main(sys.argv[1:])
