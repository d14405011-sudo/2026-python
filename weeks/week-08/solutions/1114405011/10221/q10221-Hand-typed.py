import math

def solve_line(s,a,unit):
    if unit=='min':
        a=a/60.0
    if a>180.0:
        a=360.0-a
    r=6440.0+s
    t=math.radians(a)
    arc=r*t
    chord=2.0*r*math.sin(t/2.0)
    return f'{arc:.6f} {chord:.6f}'

def solve_all(text):
    out=[]
    for line in text.splitlines():
        line=line.strip()
        if not line:
            continue
        s,a,u=line.split()
        out.append(solve_line(float(s),float(a),u))
    return '\n'.join(out)

def main():
    import sys
    x=sys.stdin.read()
    y=solve_all(x)
    if y:
        print(y)

if __name__=='__main__':
    main()
