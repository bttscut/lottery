# coding=gbk
#Boa:Frame:Frame
import os,sys
import wx
import logic

SLOW_LEVEL = 10

def create(parent):
    return Frame(parent)

[wxID_FRAME, wxID_FRAMEPANEL1, wxID_FRAMESTATICBITMAP1, 
] = [wx.NewId() for _init_ctrls in range(3)]

##		self.gridSizer1.Add(self.staticBitmap1,0,wx.ALIGN_CENTER_HORIZONTAL)

[wxID_FRAMEMENU2ITEMS0, wxID_FRAMEMENU2ITEMS1, 
] = [wx.NewId() for _init_coll_menu2_Items in range(2)]

[wxID_FRAMEMENU1ITEMS0, wxID_FRAMEMENU1ITEMS1, 
] = [wx.NewId() for _init_coll_menu1_Items in range(2)]

[wxID_FRAMEIMAGESWITCH] = [wx.NewId() for _init_utils in range(1)]

class Frame(wx.Frame):

	def _init_coll_menu1_Items(self, parent):

		parent.Append(help='', id=wxID_FRAMEMENU1ITEMS0, kind=wx.ITEM_NORMAL,
		      text='new')
		parent.Append(help='', id=wxID_FRAMEMENU1ITEMS1, kind=wx.ITEM_NORMAL,
		      text='undo')
		self.Bind(wx.EVT_MENU, self.OnMenu1Items0Menu, id=wxID_FRAMEMENU1ITEMS0)
		self.Bind(wx.EVT_MENU, self.OnMenu1Items1Menu, id=wxID_FRAMEMENU1ITEMS1)

	def _init_sizers(self):
		self.gridSizer1 = wx.GridSizer(cols=1, hgap=0, rows=1, vgap=0)

		self.panel1.SetSizer(self.gridSizer1)

	def _init_utils(self):
		self.ImageSwitch = wx.Timer(id=wxID_FRAMEIMAGESWITCH, owner=self)
		self.Bind(wx.EVT_TIMER, self.OnImageSwitchTimer, id=wxID_FRAMEIMAGESWITCH)

		self.menu1 = wx.Menu(title='')

		self.menuBar1 = wx.MenuBar()

		self._init_coll_menu1_Items(self.menu1)

	def _init_ctrls(self, prnt):
		wx.Frame.__init__(self, id=wxID_FRAME, name='Frame', parent=prnt,
		      pos=wx.Point(819, 272), size=wx.Size(499, 563),
		      style=wx.DEFAULT_FRAME_STYLE, title='lottery')
		self._init_utils()
		self.SetClientSize(wx.Size(483, 525))
		self.SetAutoLayout(False)
		self.SetToolTipString('lottery')
		self.Center(wx.BOTH)

		self.panel1 = wx.Panel(id=wxID_FRAMEPANEL1, name='panel1', parent=self,
		      pos=wx.Point(0, 0), size=wx.Size(483, 525), style=wx.TAB_TRAVERSAL)
		self.panel1.SetBackgroundColour(wx.Colour(0, 0, 0))
		self.panel1.SetAutoLayout(True)
		self.panel1.Bind(wx.EVT_KEY_UP, self.OnPanel1KeyUP)

		self.staticBitmap1 = wx.StaticBitmap(bitmap=wx.NullBitmap,
		      id=wxID_FRAMESTATICBITMAP1, name='staticBitmap1', parent=self.panel1,
		      pos=wx.Point(-270, -121), size=wx.Size(1024, 768), style=0)
		self.staticBitmap1.SetAutoLayout(True)
		self.staticBitmap1.CentreOnParent(wx.BOTH)
		self.staticBitmap1.Bind(wx.EVT_LEFT_DCLICK, self.OnStaticBitmap1LeftDclick)

		self._init_sizers()

	def __init__(self, parent):
		self.client = logic.PhotoLottery()
		self._init_ctrls(parent)
		self.menuBar1.Append(self.menu1,'opt')
		self.SetMenuBar(self.menuBar1)
		w,h = self.client.get_reso()
		self.staticBitmap1.SetInitialSize(wx.Size(w,h))
		self.gridSizer1.Add(self.staticBitmap1,0,wx.ALIGN_CENTER)
		self.show(self.client.get_cover())
		self.roll_flag = SLOW_LEVEL # 0代表正在随机 >0代表开始缓慢 SLOW_LEVEL(暂定)代表抽取成功
		
	def load_image(self):
		find_path = '.\\photo'
		file_list = os.listdir(find_path)
		print file_list
		for file in file_list:
			file_path = os.path.join(find_path,file)
			img = wx.Image(file_path,wx.BITMAP_TYPE_ANY)
			self.image_list.append(img.ConvertToBitmap())
			
	def show(self,bmp):
		self.staticBitmap1.SetBitmap(bmp)
		
	def enable_timer(self,flag):
		if self.ImageSwitch.IsRunning() == flag:
			return
		if flag:
			self.ImageSwitch.Start(self.client.get_interval())
			self.roll_flag = 0
		else:
			self.ImageSwitch.Stop()
			
	def is_rolling(self):
		return self.ImageSwitch.IsRunning()
			
	def OnImageSwitchTimer(self, event):
		#print 'timer excute'
	
		if self.roll_flag > 0:
			print 'timer reset',self.roll_flag,SLOW_LEVEL
			self.ImageSwitch.Stop()
			self.roll_flag += 1
			if self.roll_flag <= SLOW_LEVEL:
				self.show(self.client.rand())
				self.ImageSwitch.Start(self.client.get_interval()*(1.0+self.roll_flag*0.3))
				print 'timer restart',self.client.get_interval()*(1.0+self.roll_flag*10.0/100.0)
			else:
				self.show(self.client.hit())
		else:
			self.show(self.client.rand())
		event.Skip()

	def OnPanel1KeyUP(self, event):
		if event.GetKeyCode() == wx.WXK_SPACE:
			if self.is_rolling():
				if self.roll_flag == 0:
					self.roll_flag = 1
				#self.enable_timer(False)
				#self.show(self.client.hit())
			else:
				self.enable_timer(True)
		event.Skip()

	def OnStaticBitmap1LeftDclick(self, event):
		self.ShowFullScreen(not self.IsFullScreen())
		event.Skip()

	def OnMenu1Items0Menu(self, event):
		dlg = wx.MessageDialog(None,'Start new round?','Attention',wx.YES_NO|wx.ICON_QUESTION)
		ret = dlg.ShowModal()
		if ret == wx.ID_YES:	
			self.enable_timer(False)
			self.show(self.client.get_cover())
			self.client.reset()
			event.Skip()

	def OnMenu1Items1Menu(self, event):
		if self.is_rolling():
			return
		dlg = wx.MessageDialog(None,'Put this man back?','Attention',wx.YES_NO|wx.ICON_QUESTION)
		ret = dlg.ShowModal()
		if ret == wx.ID_YES:			
			self.client.undo()
		event.Skip()
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
