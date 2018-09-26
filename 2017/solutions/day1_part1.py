def main():
    s = str(input())
    n = len(s)
    s = s + s
    ans = 0
    for i in range(n):
        if s[i] == s[i + 1]:
            ans += int(s[i])
    print(ans)


if __name__ == '__main__':
    main()
