import random

class LotteryRandom:
	def __init__(self,num):
		self.total = num
		self.candidates = range(num)
		self.rand_list = []
		
	def rand(self):
		if len(self.rand_list) == 0:
			self.rand_list = self.candidates[:]
		ret = random.choice(self.rand_list)
		self.rand_list.remove(ret)
		return ret
		
	def hit(self):
		print self.candidates
		ret = random.choice(self.candidates)
		self.candidates.remove(ret)
		print 'hit:',ret
		print self.candidates
		self.rand_list = self.candidates[:]
		return ret
	
	def is_valid(self):
		return len(self.candidates) > 0
	
	def reset(self):
		self.candidates = range(self.total)
		
	def return_to_candi(self,idx):
		if idx in self.candidates:
			return
		self.candidates.append(idx)
		if idx not in self.rand_list:
			self.rand_list.append(idx)
		
	
	def remove_from_candi(self,idx):
		if idx not in self.candidates:
			return
		self.candidates.remove(idx)
		if idx in self.rand_list:
			self.rand_list.remove(idx)
		
	
def main():
	rand = LotteryRandom(40)
	while rand.is_valid():
		print rand.rand()
	
if __name__ == '__main__':
	main()
