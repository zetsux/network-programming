dict = {}
n = int(input())
for i in range(n):
  key, val = input().split()
  dict[key] = val
print(dict[input()])