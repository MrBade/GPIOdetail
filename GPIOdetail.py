import sys
import RPi.GPIO as GPIO
import os


class GPIOs:
	def __init__(self):
		self.fGPIOlist = []
		self.GPIOlist = []
		
	def __getattribute__(self, name):
	# 重写__getattribute__()方法，使得在调用GPIOlist属性时，获取实时的GPIO状态
		if name == 'GPIOlist':
			self._scan()
			name = 'fGPIOlist'
			return super().__getattribute__(name)
		else:
			return super().__getattribute__(name)
	
	def _scan(self):
	# 扫描当前GPIO口的状态，并将之存入self.fGPIOlist
		list = os.popen("gpio readall").read().split("\n")[1:-3]
		firstline = list.pop(0).split('|')
		dic = {}
		for name in firstline:
			name = name.replace(' ', '')
			dic.update({name:''})
		del dic['']
		for line in list:
			line = line.split('|')
			del line[0]
			if line==[]:
				del line
			else:
				del line[-1]
				line1 ,line2 = line[:6], line[6:]
				if line2[0]=='':
					line2 = line2[1:]
				else:
					line1.append("Physical")
					line2.insert(0, "Physical")
				#print(line1, line2)
				line2 = line2[::-1]
				for lin in (line1, line2):
					dic.update({"BCM": lin[0],
								"wPi": lin[1],
								"Name": lin[2],
								"Mode": lin[3],
								"V": lin[4],
								"Physical": lin[5]})
					GPIOdet = GPIOdetail(**dic)
					self.fGPIOlist.append(GPIOdet)

		
	def find(self, value, attr='Name'):
	# 根据属性找到对应的GPIO，并返回一个存取所有符合属性的GPIO口细节列表
		Glist = []
		for GPIO in self.fGPIOlist:
			if GPIO[attr]==value:
				Glist.append(GPIO)
		
		return Glist
	
	def search(self, value, attr='BCM'):
	# 根据属性找到对应的GPIO， 并返回一个符合属性、值的GPIO
		for GPIO in self.fGPIOlist:
			if GPIO.detaildic[attr]==value:
				return GPIO

class GPIOdetail:
	# 这是一个用于显示GPIO属性字典的类
    def __init__(self, BCM='', Mode='', V='', wPi='', Physical='', Name=''):
        BCM = BCM.replace(' ', '')
        wPi = wPi.replace(' ', '')
        V = V.replace(' ', '')
        if (BCM, wPi, V) != ('', '', ''):
            self.BCM = eval(BCM)
            self.wPi = eval(wPi)
            self.V = eval(V)
        else:
            self.BCM = BCM
            self.wPi = wPi
            self.V = V
        self.Name = Name.replace(' ', '')
        self.Mode = Mode.replace(' ', '')
        self.Physical = eval(Physical.replace(' ',''))
        self.detaildic = {'BCM': self.BCM,
                     'Mode': self.Mode,
                     'V': self.V,
                     'wPi': self.wPi,
                     'Name': self.Name,
                     'Physical': self.Physical}
        
    def show(self):
        return detaildic

if __name__ == '__main__':
    g = GPIOs()
    for i in g.GPIOlist:
        print(i.show())
