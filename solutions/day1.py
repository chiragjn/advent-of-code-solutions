def day_one_part_one(inp):
	ans = 0
	for c in inp:
		if c == '(':
			ans+=1
		elif c == ')':
			ans-=1

	return ans

def day_one_part_two(inp):
	ans = 0
	indx = 1
	for c in inp:
		if c == '(':
			ans+=1
		elif c == ')':
			ans-=1
		if ans == -1:
			break
		indx+=1

	return indx

def main():
	inp = raw_input()
	print "Answer to Part 1:"
	print day_one_part_one(inp)
	print "Answer to Part 2:"
	print day_one_part_two(inp)

if __name__ == '__main__':
	main()