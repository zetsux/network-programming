def checkPrime(n):
  if n == 1:
    return "Not Prime"

  i = 2
  while i*i <= n:
    if n % i == 0:
      return "Not Prime"
    i += 1

  return "Prime"

print(checkPrime(int(input())))