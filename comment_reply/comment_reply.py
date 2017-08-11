#coding:utf-8
import os
import sys
import time
from selenium import webdriver
import ConfigParser
cfg=ConfigParser.ConfigParser()
scriptWorkDir=sys.path[0]
comment_ini=scriptWorkDir+os.sep+"comment.ini"
cfg.read(comment_ini)
driver=webdriver.Firefox()
username=cfg.get("Userinfo","username")
password=cfg.get("Userinfo","password")
def sign_taobao():
    driver.get("https://rate.taobao.com/myRate.htm?spm=a1z0b.3.a1zvx.d27.1103f4faqBm8qd&banner=1&mytmenu=pj")
    time.sleep(2)
    driver.find_element_by_xpath(".//*[@id='J_QRCodeLogin']/div[5]/a[1]").click()
    time.sleep(3)
    driver.find_element_by_xpath(".//*[@id='J_Form']/div[2]/span").send_keys(username)
    time.sleep(2)
    driver.find_element_by_xpath(".//*[@id='TPL_password_1']").send_keys(password)
    time.sleep(1)
    driver.find_element_by_xpath(".//*[@id='J_SubmitStatic']").click()
    time.sleep(5)
def commnet_manager():
    driver.find_element_by_xpath(".//*[@id='sidebar']/div[3]/ul/li[1]/ol/li[2]/a").click()
    time.sleep(2)
    driver.set_window_size('1920','1080')  #将电脑窗口最大化
    i=1
    m=2
    n=3
    for g in range(10):  #设置翻页的次数
        for q in range(41): #一页有40个回复在没有评价的情况下
            #找到评价管理中第一个回复按钮的位置
            try:
                xpath_id = ".//*[@id='J_RateList']/tbody/tr[" + str(m) + "]/td[5]/div/button"
                fisrt_reply = driver.find_element_by_xpath(xpath_id)
                break
            # 第一个不是回复按钮，它的xpath格式是/tbody/tr[" + str(m) + "]td[5]/button,自动抛出异常（如果是已评价/为空/被删除的评价）
            except Exception:
                #m+1 去寻找下一个回复按钮
                m = m + 1
        try:
            #拖动当前评价页面到第一个回复按钮，没有的回复按钮运行抛出异常代码直接进行翻页。
            for y in range(1,41):
                time.sleep(1)
                driver.execute_script("arguments[0].scrollIntoView();", fisrt_reply)
                text=fisrt_reply.text
                time.sleep(2)
                while text==u'回复':
                    time.sleep(2)
                    comment = "comment_" + str(i)
                    comment_i = cfg.get("Comment", comment).decode("gb2312")
                    time.sleep(2)
                    fisrt_reply.click()
                    driver.find_element_by_xpath(".//*[@id='reply-overlay']/div[1]/textarea").send_keys(comment_i)
                    time.sleep(1)
                    driver.find_element_by_xpath(".//*[@id='reply-overlay']/div[2]/button").click()
                    time.sleep(1)
                    i=i+1
                    #在配置文件中写好了15条评价，进行循环
                    if i==15:
                        i=1 #最后一条评价完又从第一条开始评价
                    m=m+1
                    for x in range(40):
                    #找到下一个回复按钮
                        try:
                            xpath_id = ".//*[@id='J_RateList']/tbody/tr[" + str(m) + "]/td[5]/div/button"
                            fisrt_reply = driver.find_element_by_xpath(xpath_id)
                            text = fisrt_reply.text
                            break
                        except Exception:
                            m = m+1
        #如果当前页面没有回复按钮，或者所有的已经都被回复了，运行抛出异常代码进行翻页。
        except Exception:
            page_bottom = driver.find_element_by_xpath(".//*[@id='J_SiteFooter']/div[1]/p/span[1]/a")
            driver.execute_script("arguments[0].scrollIntoView();", page_bottom)
        time.sleep(2)
        #翻到第9页的时候，需要减1定位正确进行定位。
        if n==9:
            page_number=".//*[@id='rateList']/div[1]/ul/li["+ str(n-1) + "]/a"
            n=n-1
        else:
            page_number=".//*[@id='rateList']/div[1]/ul/li["+ str(n) + "]/a"
        driver.find_element_by_xpath(page_number).click()
        time.sleep(2)
        n=n+1
        m=2

if __name__=='__main__':
    sign_taobao()
    commnet_manager()

