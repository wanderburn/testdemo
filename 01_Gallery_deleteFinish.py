# -*- coding: UTF-8 -*-
#*****************************************************************************
# Title:        Gallery delete picture success
# Precondition: 1.A devices connected
# Author:       wuqiang.zou
# Description:  Delete the  gallery picture
# Platform:     5.1
# Project:      PIXi4-4.5TMO
#*****************************************************************************

from uiautomator import device as device
import os
import logging

def createlogger():
    """Create a logger named specified name with the level set in config file.
    """   
    logger = logging.getLogger()
    logger.setLevel("DEBUG")
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d: [%(levelname)s] [%(name)s] [%(funcName)s] [%(lineno)d] %(message)s',
        '%y%m%d %H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def create_folder():
    logger=logging.getLogger()
    log_path='E:/resource'
    if log_path is None:
        log_path='E:/resource'
    if not os.path.exists(log_path):
        logger.debug("log_path not exsit")
        os.makedirs(log_path)
    if os.path.exists(log_path):
        return None
    return log_path
'''
def reset_gallery_watchers(device):
    if device(text="Allow Gallery to Access photos, media, and files on your device?").exists:
        device.delay(1)
        device(text="Allow").click()
        device.delay(1)
        if device(text="Allow Gallery to Access this device's location?").exists:
            device.delay(1)
            device(text="Allow").click()
        else:
            print ("There isn't gallery watchers")
'''
def reset_gallery_watchers(device):
    device.watcher("Allow Gallery to Access photos").when(text="Allow").click(text="Allow")
    device.watcher("Allow Gallery to Access location").when(text="Allow").click(text="Allow")

class count_pictures(object):
    def __init__(self):
        self._device=device
        self._logger=createlogger()
        self._log_path=create_folder()
    def count_delete(self):
        device.long_click(80,200)
        device.delay(1)
        device(description='More options').click()
        device.delay(1)
        device(text='Select all').click()
        c=device(resourceId='com.tct.gallery3d:id/action_mode_text').info.get('text')
        c=int(c)
        print 'The total %s pictures has been exsited'%c
        self._logger.debug("please input the deleted numbers of pictures ")
        h=raw_input(u'请输入要删除的图片的数量h:')
        h=int(h)
        device(description='More options').click()
        device(text='Deselect all').click()
        device.delay(1)
        g=c//12
        for y in range(g+1):
            device.swipe(240,180,240,820,steps=100)
        device(description='More options').click()
        device.delay(1)
        device(text='Select item').click()
        device.delay(1)
        if h>c:
            self._logger.debug("failed to delete pictures ")
        else:
            self._logger.debug("can start to delete pictures")
            if h>15:
                for b in range(5):
                    for a in range(3):
                        device.click(80+160*a,200+160*b)
                f=h-15
                j=f//3
                i=f%3
                x,y,t=0,0,0
                for x in range(j+1):
                    if f>0:
                        if y==0:
                            device.swipe(240,690,240,480,steps=50)
                        else:
                            device.swipe(240,689,240,530,steps=50)
                        y=y+1
                        device.delay(1)
                        if x<j:
                            for t in range(3):
                                device.click(80+160*t,774)
                        f=f-3
                    else:
                        pass
                for m in range(i):
                    device.click(80+160*m,774)
                device(description='Delete').click()
                device(text='OK').click()
                if device(description='More options').exists:
                    device(description='More options').click()
                    device.delay(1)
                    device(text='Select item').click()
                    device(description='More options').click()
                    device.delay(1)
                    device(text='Select all').click()
                    delc=device(resourceId='com.tct.gallery3d:id/action_mode_text').info.get('text')
                    delc=int(delc)
                    if delc<c:
                        print("%s pictures delete successful"%h)
                        self._logger.debug('delete pictures successful')
                        device(description='More options').click()
                        device(text='Deselect all').click()
                    else:
                        self._logger.debug("fail to delete pictures")
                else:
                    self._logger.debug("fail to delete pictures")

            elif h<=15:
                i=h%3
                j=h//3
                for b in range(j):
                    for a in range(3):
                        device.click(80+160*a,200+160*b)
                for t in range(i):
                    device.click(80+160*t,200+160*j)
                device(description='Delete').click()
                device(text='OK').click()
                if device(description='More options').exists:
                    device(description='More options').click()
                    device.delay(1)
                    device(text='Select item').click()
                    device(description='More options').click()
                    device.delay(1)
                    device(text='Select all').click()
                    delc=device(resourceId='com.tct.gallery3d:id/action_mode_text').info.get('text')
                    delc=int(delc)
                    if delc<c:
                        print("%s pictures delete successful"%h)
                        self._logger.debug('delete pictures successful')
                        device(description='More options').click()
                        device(text='Deselect all').click()

                    else:
                        self._logger.debug("fail to delete pictures")
                else:
                    self._logger.debug("fail to delete pictures")
            else:
                pass

class Gallery(object):
    def __init__(self):
        self._device=device
        self._logger=createlogger()
        self._log_path=create_folder()

    def enter_gallery(self):
        """Enter gallery app via activity
        """
        self._logger.debug('Begain to enter gallery app')
        device.press.home()
        device.delay(1)
        device(className="com.tct.launcher.Workspace",resourceId="com.tct.launcher:id/workspace").swipe.left(steps=50)
        device.delay(1)
        device.click(160,660)
        reset_gallery_watchers(device)
        if device(resourceId='com.tct.gallery3d:id/gallery_root').wait.exists(timeout=10000):
            self._logger.debug('Enter gallery app successful.')
        else:
            self._logger.debug("Fail to enter gallery app.")

    def gallery_delete(self):
        """Delete one pictures or some pictures or all pictures in gallery
        """
        self._logger.debug("Begin to delete pictures in gallery app.")
        if device(text='Camera roll',resourceId='com.tct.gallery3d:id/actionbar_title').exists:
            self._logger.debug("Now is in the  Camera roll,can select the item")
            device(description='Open navigation drawer').click()
            device.delay(1)    
            if device(text='Camera roll',resourceId='com.tct.gallery3d:id/tx').wait.exists(timeout=10000):
                self._logger.debug("Enter the item to select the Camera roll,Albums...")
                device(text='Camera roll',resourceId='com.tct.gallery3d:id/tx').click()
                device.delay(1)
                device.long_click(80,200)
                if device(description='Delete').wait.exists(timeout=10000):
                    self._logger.debug("Success enter to select the ablum,There is some pictures")
                    device.click(80,200)
                else:
                    self._logger.warning("There isn't pictures,please import some pictures")
            else:
                self._logger.debug("Fail to enter the item to select the Camera roll,Alums...")
        else:
            self._logger.debug("Fail enter to gallery interface")
if __name__=="__main__":
    Gallery().enter_gallery()
    Gallery().gallery_delete()
    count_pictures().count_delete()
        
