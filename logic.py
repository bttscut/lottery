import os,sys
import lotteryrand
import wx
import ConfigParser

TIMER_INTERVAL = 200
PIC_SUFFIX = '.jpg'

def get_cur_path():
	path = sys.path[0] 
	if os.path.isdir(path):
		return path
	elif os.path.isfile(path):
		return os.path.dirname(path)

CONFIG_PATH = get_cur_path() + '\\config.ini'
SPE_CONFIG_PATH = get_cur_path() + '\\spe.ini'

class PhotoLottery:
	def __init__(self,dir = None):
		print 'cur path',CONFIG_PATH
		self._load_config()
		self.selected = 0
		self.name_idx_map = {}
		self.rand_imgs = []
		self.hit_imgs = []
		self._load_image()
		self.rand_gen = lotteryrand.LotteryRandom(len(self.rand_imgs))
		self.cheat_counter = 1
		

	def _load_config(self):
		self.reso_w = 1024
		self.reso_h = 768
		self.timer_interval = 100
		self.cover_path = ''
		self.cheat_num = 0
		self.cheat_map = {}
		try:
			conf = ConfigParser.ConfigParser()
			conf.read(CONFIG_PATH)
			self.reso_w = int(conf.get('resolution','width'))
			self.reso_h = int(conf.get('resolution','height'))
			self.pic_path = conf.get('dir','pic')
			self.cover_path = conf.get('dir','cover')
			self.timer_interval = int(conf.get('common','timer_interval'))
			self.already_cheat = int(conf.get('common','start'))
			if self.already_cheat == 0:
				ch_cfg = ConfigParser.ConfigParser()
				ch_cfg.read(SPE_CONFIG_PATH)
				self.cheat_num = int(ch_cfg.get('common','num'))
				print self.cheat_num
				for i in xrange(1,self.cheat_num+1):
					print str(i)
					self.cheat_map[i] = ch_cfg.get('list',str(i))

		except Exception, e:
			print "config error\n%s"%(str(e))

		
	def get_reso(self):
		return self.reso_w,self.reso_h

	def get_interval(self):
		return self.timer_interval
		
	def _load_image(self):
		cover_file = 'cover.jpg' if not len(self.cover_path) else self.cover_path+'\\cover.jpg'
		print cover_file
		self.cover_bmp = wx.Image(cover_file,wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		find_path = self.pic_path + '\\rand'
		file_list = os.listdir(find_path)
		print file_list
		counter = 0
		for file in file_list:
			if file.find(PIC_SUFFIX) == -1:
				continue
			self.name_idx_map[file.split('.')[0]] = counter
			counter += 1
			file_path = os.path.join(find_path,file)
			img = wx.Image(file_path,wx.BITMAP_TYPE_ANY)
			self.rand_imgs.append(img.ConvertToBitmap())
		print self.name_idx_map
			
		find_path = self.pic_path + '\\hit'

		if not os.path.exists(find_path):
			self.hit_imgs = self.rand_imgs
			return
		file_list = os.listdir(find_path)
		print file_list
		for file in file_list:
			if file.find(PIC_SUFFIX) == -1:
				continue
			file_path = os.path.join(find_path,file)
			img = wx.Image(file_path,wx.BITMAP_TYPE_ANY)
			self.hit_imgs.append(img.ConvertToBitmap())

		if len(self.rand_imgs) != len(self.hit_imgs) or len(self.rand_imgs) != len(self.name_idx_map):
			print 'pic data num error!'

			
			
	def get_cover(self):
		return self.cover_bmp
			
	def rand(self):
		if (not self.rand_gen.is_valid()):
			return wx.NullBitmap
		maybe_lucky = self.rand_gen.rand()
		return self.rand_imgs[maybe_lucky]
	
	def hit(self):
		if self.already_cheat == 0 and self.cheat_counter <= self.cheat_num and self.cheat_counter in self.cheat_map:
			unlucky = self.name_idx_map[self.cheat_map[self.cheat_counter]]
			print 'un',unlucky
			self.rand_gen.remove_from_candi(unlucky)
			self.selected = unlucky
			self.cheat_counter += 1
			if self.cheat_counter > self.cheat_num:
				conf = ConfigParser.ConfigParser()
				conf.read(CONFIG_PATH)
				#conf.set('common','start','1')
				conf.write(open(CONFIG_PATH,'r+'))
			return self.hit_imgs[unlucky]
		if (not self.rand_gen.is_valid()):
			return wx.NullBitmap
		lucky = self.rand_gen.hit()
		self.selected = lucky
		return self.hit_imgs[lucky]
	
	def undo(self):
		self.rand_gen.return_to_candi(self.selected)
	
	def reset(self):
		self.rand_gen.reset()
	
def main():
	l = PhotoLottery()
	l.hit()
	
if __name__ == '__main__':
	main()
