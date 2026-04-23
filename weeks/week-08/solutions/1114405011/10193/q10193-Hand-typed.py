import math

def solve_case(a_bin,b_bin,idx):
    a=int(a_bin,2)
    b=int(b_bin,2)
    if math.gcd(a,b)>1:
        return f'Pair #{idx}: All you need is love!'
    return f'Pair #{idx}: Love is not all you need!'

def solve_all(text):
    arr=[s.strip() for s in text.splitlines() if s.strip()]
    if not arr:
        return ''
    t=int(arr[0])
    out=[]
    j=1
    for i in range(1,t+1):
        out.append(solve_case(arr[j],arr[j+1],i))
        j+=2
    return '\n'.join(out)

def main():
    import sys
    x=sys.stdin.read()
    y=solve_all(x)
    if y:
        print(y)

if __name__=='__main__':
    main()
