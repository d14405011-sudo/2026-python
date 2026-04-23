def solve_line(n,m):
    if n<1 or m<2:
        return 'Boring!'
    seq=[n]
    while n!=1:
        if n%m!=0:
            return 'Boring!'
        n//=m
        seq.append(n)
    return ' '.join(map(str,seq))

def solve_all(text):
    out=[]
    for line in text.splitlines():
        line=line.strip()
        if not line:
            continue
        n,m=map(int,line.split())
        out.append(solve_line(n,m))
    return '\n'.join(out)

def main():
    import sys
    x=sys.stdin.read()
    y=solve_all(x)
    if y:
        print(y)

if __name__=='__main__':
    main()
