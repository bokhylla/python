#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import wx
import imgcommon
import shutil

PATH_DESKTOP = os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH') + '\\Desktop'



class MyFrame(wx.Frame):
  def __init__(self, *args, **kwds):
    kwds['style'] = kwds.get('style', 0) | wx.DEFAULT_FRAME_STYLE
    wx.Frame.__init__(self, *args, **kwds)
    self.folder = ''
    self.SetSize((900, 300))

    self.choose_text = wx.TextCtrl(self, wx.ID_ANY, self.folder, size=(400, 12))
    self.button_choose = wx.Button(self, wx.ID_ANY, 'フォルダを選択')

    self.button_exec = wx.Button(self, wx.ID_ANY, '変換')

    self.__set_properties()
    self.__do_layout()

  def __set_properties(self):
    self.SetTitle('jpg一括変換')
    
    self.button_choose.Bind(wx.EVT_BUTTON, self.choose_folder)
    self.button_exec.Bind(wx.EVT_BUTTON, self.exec_convert)



  def __do_layout(self):
    sizer_main = wx.BoxSizer(wx.VERTICAL)
    sizer_buttons_area = wx.WrapSizer(wx.HORIZONTAL)
    sizer_dialog_area = wx.WrapSizer(wx.HORIZONTAL)
    sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)
    
    sizer_dialog_area.Add(self.choose_text, 0, wx.EXPAND)
    sizer_dialog_area.Add(self.button_choose, 0, wx.EXPAND | wx.LEFT, 10)
    sizer_main.Add(sizer_dialog_area, 2, wx.LEFT | wx.TOP | wx.FIXED_MINSIZE, 10)

    sizer_buttons.Add(self.button_exec, 0, wx.LEFT, 10)
    sizer_buttons_area.Add(sizer_buttons, 0, wx.EXPAND | wx.ALIGN_BOTTOM, 0)
    sizer_main.Add(sizer_buttons_area, 0, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.TOP | wx.BOTTOM | wx.RIGHT | wx.FIXED_MINSIZE, 20)
    self.SetSizer(sizer_main)
    self.Layout()
    self.SetBackgroundColour('#ccc')
  
  
  
  def choose_folder(self, event):
    folder = wx.DirDialog(self, defaultPath=PATH_DESKTOP, style=wx.DD_CHANGE_DIR, message='フォルダを選択')
    
    if folder.ShowModal() == wx.ID_OK:
      self.folder = folder.GetPath()
    folder.Destroy()
    self.choose_text.SetLabel(self.folder)



  def exec_convert(self, event):
    confirm = wx.MessageDialog(self, 'フォルダ内の画像をjpg形式に変換します。よろしいですか？', '確認', style=wx.OK | wx.CANCEL)
    
    if confirm.ShowModal() == wx.ID_OK:
      
      list_img = imgcommon.ImgsUtil(path=self.choose_text.GetValue(), type='PNG|BMP')
      os.makedirs('delete', exist_ok=True)
      num = list_img.len()
      
      dir_output = self.choose_text.GetValue()
      
      f_name = list_img.get_image(0).name.split('\\')[-1]
      dialog = wx.ProgressDialog('変換中', f_name, num - 1)
      dialog.ShowModal()
      
      for i in range(0, num):
        list_img.get_image(i).convert_jpg(dir_output)
        
        f_name = list_img.get_image(i).name.split('\\')[-1]
        dialog.Update(i, f_name)
          
        shutil.move(f_name, 'delete/')
      
      dialog.Destroy()
      
      finish = wx.MessageDialog(self, '画像の変換が完了しました。', '変換完了', style=wx.OK)
      finish.ShowModal()
      
      finish.Destroy()
      
    confirm.Destroy()



class MyApp(wx.App):
  def OnInit(self):
    self.frame = MyFrame(None, wx.ID_ANY, '')
    self.SetTopWindow(self.frame)
    self.frame.Show()
    return True



if __name__ == '__main__':
  app = MyApp(0)
  app.MainLoop()
