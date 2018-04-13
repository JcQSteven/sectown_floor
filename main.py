#coding:utf-8
from tkinter import *
from tkinter import messagebox
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import threading
class Automan(Frame):
    def __init__(self,master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.username_var= StringVar(self,'')
        self.password_var=StringVar(self,'')
        self.login_url_var=StringVar(self,'http://www.sectown.cn/login')
        self.auto_url_var=StringVar(self,'https://www.sectown.cn/group/14/thread/')
        self.sleeptime_var=StringVar(self,'0.1')
        self.target_floor_var=StringVar(self,'0')
        self.con_var=StringVar(self,u'酷酷的我抢到了这一层！')
        self.info_var=StringVar(self,u'')
        self.hint_var=StringVar(self,u'不要多开该程序，需要重新抢楼的话请终止抢楼先。\n有问题就联系金成强。不要提奇奇怪怪的需求！\n')

        self.hint_label=Label(self)
        self.hint_label['textvariable']=self.hint_var
        self.hint_label.pack()

        self.username_label = Label(self)
        self.username_label['text']=u'账号'
        self.username_label.pack()

        self.username_entry=Entry(self)
        self.username_entry['textvariable']=self.username_var
        self.username_entry.pack()

        self.password_label=Label(self)
        self.password_label['text']=u'密码'
        self.password_label.pack()

        self.password_entry = Entry(self)
        self.password_entry['textvariable'] = self.password_var
        self.password_entry.pack()

        self.login_url_label=Label(self)
        self.login_url_label['text']=u'登录账号网址'
        self.login_url_label.pack()

        self.login_url_entry = Entry(self)
        self.login_url_entry['textvariable'] = self.login_url_var
        self.login_url_entry['width']=30
        self.login_url_entry.pack()

        self.auto_url_label=Label(self)
        self.auto_url_label['text']=u'抢楼网址'
        self.auto_url_label.pack()

        self.auto_url_entry = Entry(self)
        self.auto_url_entry['textvariable'] = self.auto_url_var
        self.auto_url_entry['width'] = 50
        self.auto_url_entry.pack()

        self.sleeptime_label=Label(self)
        self.sleeptime_label['text']=u'刷新等待时间'
        self.sleeptime_label.pack()

        self.sleeptime_entry = Entry(self)
        self.sleeptime_entry['textvariable'] = self.sleeptime_var
        self.sleeptime_entry.pack()

        self.target_floor_label=Label(self)
        self.target_floor_label['text']=u'目标楼层'
        self.target_floor_label.pack()

        self.target_floor_entry = Entry(self)
        self.target_floor_entry['textvariable'] = self.target_floor_var
        self.target_floor_entry.pack()

        self.con_label = Label(self)
        self.con_label['text']='Content'
        self.con_label.pack()

        self.con_entry = Entry(self)
        self.con_entry['textvariable'] = self.con_var
        self.con_entry.pack()

        self.botton1=Button(self)
        self.botton1['text']=u'开始抢楼'
        self.botton1['command']=self.thread_control
        self.botton1.pack()

        self.botton2 = Button(self)
        self.botton2['text'] = u'停止抢楼'
        self.botton2['command'] = self.quit_auto
        self.botton2.pack()

        self.info_label=Label(self)
        self.info_label['textvariable']=self.info_var
        self.info_label['bg']='red'
        self.info_label.pack()


        self.thread_flag=True
    def login(self):

        self.username=self.username_var.get()
        self.password=self.password_var.get()
        self.login_url=self.login_url_var.get()
        self.auto_url=self.auto_url_var.get()
        self.browser = webdriver.Chrome('./chromedriver')
        self.sleeptime=float(self.sleeptime_var.get())
        self.target_floor=int(self.target_floor_var.get())-1
        self.con=self.con_var.get()


        self.browser.get(self.login_url)
        user = self.browser.find_element_by_name('_username')
        pwd = self.browser.find_element_by_name('_password')
        user.send_keys(self.username)
        pwd.send_keys(self.password)
        pwd.send_keys(Keys.RETURN)
        self.auto_done()

    def auto_done(self):
        self.browser.execute_script('window.open("%s")'%self.auto_url)
        time.sleep(1)
        handles = self.browser.window_handles
        self.browser.switch_to_window(handles[-1])
        floor=self.browser.find_elements_by_xpath('//*[@class="floor"]')
        test_floor=floor[-1].text
        test_floor_num=int(test_floor[:-1])

        # last_page_ele = self.browser.find_element_by_xpath('//*[@class="pagination cd-pagination"]/li[last()]/a')
        # last_page = last_page_ele.get_attribute('href')
        last_page=self.auto_url_var.get()+'?page=99'
        self.browser.execute_script('window.open("%s")' % last_page)
        time.sleep(1)
        while 1:
            if self.thread_flag==False:
                #messagebox.showinfo(title=u'终止',message=u'您已终止程序')
                self.info_var.set(u'您已终止程序')
                self.browser.quit()
                break
            #print 'loop'
            if test_floor_num>31:
                last_page_ele_try = self.browser.find_element_by_xpath('//*[@class="pagination cd-pagination"]/li[last()]/a')
                last_page_try = last_page_ele_try.get_attribute('href')
                if last_page_try!=last_page:
                    last_page=last_page_try
                    self.browser.execute_script('window.open("%s")' % last_page)
                    time.sleep(1)
                else:
                    pass
            handles = self.browser.window_handles
            self.browser.switch_to_window(handles[-1])
            floor = self.browser.find_elements_by_xpath('//*[@class="floor"]')
            last_floor = floor[-1].text
            self.info_var.set(u'目前楼层数' + last_floor)
            last_floor_num=int(last_floor[:-1])

            if last_floor_num == self.target_floor:
                time.sleep(1)
                content = self.browser.find_element_by_tag_name('iframe')
                self.browser.switch_to_frame(content)
                p = self.browser.find_element_by_tag_name('body')
                p.send_keys(self.con)
                self.browser.switch_to_default_content()
                self.browser.find_element_by_id('post-thread-btn').click()
                self.browser.quit()
                self.info_var.set(u'恭喜抢楼成功，抢到楼层%d'%(self.target_floor+1))
                #messagebox.showinfo(title=u'抢楼成功', message='恭喜抢楼成功，抢到楼层%d'%self.target_floor)
                break
            else:
                if last_floor_num<self.target_floor:
                #print '[!]Current Floor:'+last_floor
                    self.browser.refresh()
                    time.sleep(self.sleeptime)
                    #print '[*]refresh'
                else:
                    self.browser.quit()
                    self.info_var.set(u'抱歉，您要抢的楼层已经不存在，重新调整楼层位置')
                    #messagebox.showwarning(title=u'失败',message=u'抱歉，您要抢的楼层已经不存在，重新调整楼层位置')
                    break
    def quit_auto(self):
        self.thread_flag=False
    def thread_control(self):
        self.thread_flag=True
        self.t=threading.Thread(target=self.login)
        self.t.setDaemon(True)
        self.t.start()

if __name__ == '__main__':
    root=Tk()
    root.title(u'安全通内部抢楼机器人')
    root.wm_attributes('-topmost', 1)
    root.geometry('400x500+30+30')
    auto_man=Automan(master=root)
    auto_man.mainloop()