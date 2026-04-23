ROWS=["`1234567890-=","QWERTYUIOP[]\\","ASDFGHJKL;'","ZXCVBNM,./"]
M={}
for row in ROWS:
    for i in range(1,len(row)):
        M[row[i]]=row[i-1]
        if row[i].isalpha():
            M[row[i].lower()]=row[i-1].lower()

def decode_line(line):
    return ''.join(M.get(ch,ch) for ch in line)

def solve_all(text):
    return '\n'.join(decode_line(x) for x in text.splitlines())

def main():
    import sys
    x=sys.stdin.read()
    if x:
        print(solve_all(x))

if __name__=='__main__':
    main()
