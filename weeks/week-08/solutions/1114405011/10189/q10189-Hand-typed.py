DIRS=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

def solve_field(grid):
    n=len(grid)
    m=len(grid[0]) if n else 0
    out=[]
    for r in range(n):
        row=[]
        for c in range(m):
            if grid[r][c]=='*':
                row.append('*')
            else:
                k=0
                for dr,dc in DIRS:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<n and 0<=nc<m and grid[nr][nc]=='*':
                        k+=1
                row.append(str(k))
        out.append(''.join(row))
    return out

def solve_all(text):
    lines=text.splitlines()
    i=0
    t=0
    blocks=[]
    while i<len(lines):
        s=lines[i].strip()
        i+=1
        if not s:
            continue
        n,m=map(int,s.split())
        if n==0 and m==0:
            break
        g=[lines[i+j] for j in range(n)]
        i+=n
        t+=1
        b=[f'Field #{t}:']
        b.extend(solve_field(g))
        blocks.append('\n'.join(b))
    return '\n\n'.join(blocks)

def main():
    import sys
    x=sys.stdin.read()
    y=solve_all(x)
    if y:
        print(y)

if __name__=='__main__':
    main()
