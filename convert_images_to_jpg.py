#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import wx
import shutil
from PIL import Image
from pathlib import Path

PATH_DESKTOP = os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH') + '\\Desktop'



class MyFrame(wx.Frame):
  def __init__(self, *args, **kwds):
    kwds['style'] = kwds.get('style', 0) | wx.DEFAULT_FRAME_STYLE
    wx.Frame.__init__(self, *args, **kwds)
    
    self.folder = ''
    # フレームサイズの設定
    self.SetSize((900, 300))
    
    # テキスト蘭及びボタンの設定
    self.choose_folder = wx.TextCtrl(self, wx.ID_ANY, self.folder, size=(400, 12))
    self.button_choose = wx.Button(self, wx.ID_ANY, 'フォルダを選択')
    self.button_exec = wx.Button(self, wx.ID_ANY, '変換')
    
    # 画面のプロパティ及びレイアウトの設定
    self.__set_properties()
    self.__do_layout()
  
  
  
  def __set_properties(self):
    """
    フレームのプロパティ設定
    
    Args:
    
    Returns:
        None
    
    """
    
    self.SetTitle('jpg一括変換')
    
    # ボタンのイベント処理設定
    self.button_choose.Bind(wx.EVT_BUTTON, self.choose_folder)
    self.button_exec.Bind(wx.EVT_BUTTON, self.exec_convert)
  
  
  
  def __do_layout(self):
    """
    フレームのレイアウト設定
    
    Args:
    
    Returns:
        None
    
    """
    
    # メインsizer
    sizer_main = wx.BoxSizer(wx.VERTICAL)
    
    # 対象フォルダ設定箇所のsizer
    sizer_dialog_area = wx.WrapSizer(wx.HORIZONTAL)
    sizer_dialog_area.Add(self.choose_folder, 0, wx.EXPAND)
    sizer_dialog_area.Add(self.button_choose, 0, wx.EXPAND | wx.LEFT, 10)
    sizer_main.Add(sizer_dialog_area, 2, wx.LEFT | wx.TOP | wx.FIXED_MINSIZE, 10)
    
    # ボタン設定エリアのsizer(内枠)
    sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)
    sizer_buttons.Add(self.button_exec, 0, wx.LEFT, 10)
    
    # ボタン設定エリアのsizer(外枠)
    sizer_buttons_area = wx.WrapSizer(wx.HORIZONTAL)
    sizer_buttons_area.Add(sizer_buttons, 0, wx.EXPAND | wx.ALIGN_BOTTOM, 0)
    sizer_main.Add(sizer_buttons_area, 0, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.TOP | wx.BOTTOM | wx.RIGHT | wx.FIXED_MINSIZE, 20)
    
    self.SetSizer(sizer_main)
    self.Layout()
    self.SetBackgroundColour('#ccc')
  
  
  
  def choose_folder(self, event):
    """
    フォルダ選択ダイアログ処理
    
    Args:
        event : イベント
    
    Returns:
        None
    
    """
    
    folder = wx.DirDialog(self, defaultPath=PATH_DESKTOP, style=wx.DD_CHANGE_DIR, message='フォルダを選択')
    
    # フォルダ選択のModalを開く
    if folder.ShowModal() == wx.ID_OK:
      # フォルダ選択後、OK押下の場合はパスを取得
      self.folder = folder.GetPath()
    
    folder.Destroy()
    
    # 取得したパスをテキストボックスに設定
    self.choose_folder.SetLabel(self.folder)
  
  
  
  def exec_convert(self, event):
    """
    フォルダ内のjpg以外の画像を一括でjpgに変換
    
    Args:
        event: イベント
    
    Returns:
        None
    
    """
    
    confirm_dialog = wx.MessageDialog(self, 'フォルダ内の画像をjpg形式に変換します。よろしいですか？', '確認', style=wx.OK | wx.CANCEL)
    
    # 確認Modalを開く
    if confirm_dialog.ShowModal() == wx.ID_OK:
      
      # OK押下の場合は変換処理を実施
      path = self.choose_folder.GetValue()
      os.chdir(path)
      
      # 指定したフォルダ内の画像を取得
      list_img = self.get_imgs(path)
      
      # ファイルの変換後、元ファイルを移動させるフォルダの作成
      os.makedirs('delete', exist_ok=True)
      num = len(list_img)
      
      dir_output = path
      f_name = list_img[0].split('\\')[-1]
      
      # 変換中のプロセスバー表示
      convert_dialog = wx.ProgressDialog('変換中', f_name, num - 1)
      convert_dialog.ShowModal()
      
      for i in range(0, num):
        f_name = list_img[i].split('\\')[-1]
        #画像の変換処理
        self.convert_jpg(f_name, dir_output)
        
        # プロセスバーの更新
        convert_dialog.Update(i, f_name)
        
        # 変換したファイルを移動
        shutil.move(f_name, 'delete/')
      
      convert_dialog.Destroy()
      
      # 変換完了のModalを開く
      finish_dialog = wx.MessageDialog(self, '画像の変換が完了しました。', '変換完了', style=wx.OK)
      finish_dialog.ShowModal()
      
      finish_dialog.Destroy()
      
    confirm_dialog.Destroy()
  
  
  
  def get_imgs(self, path):
    """
    指定されたフォルダ内の返還対象となる画像一覧を取得
    
    Args:
        path: 対象フォルダ
    
    Returns:
        result: 画像のパスリスト
    
    """
    
    p_dir = Path(path)
    
    imgs_glob = []
    result = []
    
    imgs_glob += list(p_dir.glob('**/*.png'))
    imgs_glob += list(p_dir.glob('**/*.bmp'))
    
    for img in imgs_glob:
      result.append(str(img))
    
    return result
  
  
  
  def convert_jpg(self, img_name, output_path):
    """
    指定されたフォルダ内の返還対象となる画像一覧を取得
    
    Args:
        img_name: 画像ファイル名
        output_path: 出力パス
    
    Returns:
        None
    
    """
    
    basename = img_name.split('.')[0]
    
    img = Image.open(img_name)
    img.convert('RGB').save(basename + '.jpg', quality = 95)



class MyApp(wx.App):
  def OnInit(self):
    self.frame = MyFrame(None, wx.ID_ANY, '')
    self.SetTopWindow(self.frame)
    self.frame.Show()
    return True



if __name__ == '__main__':
  app = MyApp(0)
  app.MainLoop()
