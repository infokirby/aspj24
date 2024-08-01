def main():   
    p = 86869
    q = 54133
    n = p * q
    r = (p-1)*(q-1)
    e = 53
    d = r/e
    count = 1

    while True:
        try:
            ans = d * count
            print(ans)
            if ((e*ans) % r) == 1:
                print(f"{int(ans)}")
                return 0

        except:
            count += 1

main()