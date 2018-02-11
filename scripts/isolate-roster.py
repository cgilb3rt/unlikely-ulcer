import argparse, re, sys

def read_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('roster')
	parser.add_argument('lines', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
	return parser.parse_args()

def read_roster(file):
	with open(file) as f:
		return [line.rstrip() for line in f]

def main():
	args = read_args()
	roster = read_roster(args.roster)

	i=0
	for line in sys.stdin.readlines():
		name = re.sub(r" [a-z0-9/\. ]+$", "", line.rstrip())
		name = re.sub(r"^ +", "", name)
		(first, last) = re.split(' ', name)

		# swap any names that happen to be "last, first"
		if len(first)>0:
			if first[len(first)-1] == ',':
				swap = first
				first = last
				last = swap[:len(swap)-1]
		print "%d: %s, %s" % (i, last, first)
		i=i+1

main()
