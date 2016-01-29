# -*- coding: utf-8 -*-
# THE ABOVE LINE IS REQUIRED TO ENABLE UTF-8 DISPLAY IN THE TEXT WIDGETS.            # 
######################################################################################
#                                                                                    #
PyEyeCryptVersion="v1.2"                                                             #
#                                                                                    #
######################################################################################
#                                                                                    #
#                                                                                    #
#    PyEyeCrypt (%s)    -    Copyright (C) 2015 "mi55 ing" <mi55ing@protonmail.ch>   #
#    Permission is hereby granted, free of charge, to any person obtaining a         #
#    copy of this software and associated documentation files (the "Software"),      #
#    to deal in the Software without restriction, including without limitation       #
#    the rights to use, copy, modify, merge, publish, distribute, sublicense,        # 
#    and/or sell copies of the Software, and to permit persons to whom the           #
#    Software is furnished to do so, subject to the following conditions:            #
#                                                                                    #
#    The above copyright notice and this permission notice shall be included in      #
#    all copies or substantial portions of the Software.                             #
#                                                                                    #
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      #
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,        #
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL         #
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER      #
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING         #
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER             #
#    DEALINGS IN THE SOFTWARE.                                                       #
#                                                                                    #
#                                                                                    #
######################################################################################
# Change Log                                                                         #
# ==========                                                                         #
#                                                                                    #
# v1.2:                                                                              #
#  o Auto-remove any extra Spaces or "Enter" [CR/LF] characters in the Encrypted     # 
#    Text window on Decrypt action.                                                  #
#  o Allow user to resize text in both main text windows and password (Font Size ±)  #
#  o Changed the font of Password/Salt/Key/IV/PBKDF2 to 'arial' with 30 chars.       #
#    -Also set Password font to ( "arial", bestpasswordfontsize), so it's            #
#     initially at least the same size as salt/IV/Key, but then increases in line    #
#     with the sizes of the other "resizable" fields, ClearText/EncryptedText.       #
#  o Fixed cosmetic bug in Decrypt function when PBKDF2 iterations=0                 #
#    (message said encrypt, when it should have said decrypt).                       #
#  o Commented out irritating messages for salt/IV/Key overwrite for Encrypt/Decrypt #
#  o Modified warning message about padding to remove confusing details              #
#  o Modified Font measurements to use "weight=tkFont.BOLD" in case that affects     #
#    the measured widths.                                                            #
#  o Added Font Size 13 into the list of available sizes to be tested                #
#                                                                                    #
# v1.1:                                                                              #
# o Added concept of "isBadOS" to enforce spying countermeasures like clickable      # 
#   keyboard.                                                                        #
#   - PyEyeCrypt can now run under what it considers to be 'bad' operating systems.  #
# o Added "Click-to-type" mode so users can select improved security of clickable    #
#   keyboards, even if the OS is not considered 'bad'.                               # 
# o Fixed a potential bug with PBKDF2iterations being '0'.                           #
# o Made Timestamps of keypresses in EntropyWindow visible.                          #
# o HexCheck() now checks EncryptedText regardless of "Hex Mode" checkbox status.    #
# o Decryption checks that a Password is present when a Key is not being 'kept'.     #
#                                                                                    #
# v1.0:                                                                              #
# Initial Release                                                                    # 
#                                                                                    #
#                                                                                    #
# Future Improvements                                                                #
# ===================                                                                #
# 1: Message Authentication                                                          #
# 2: Add MORE Win10 spying "Countermeasures";                                        #
#    -add option to randomise key positions on clickable keyboard                    #
#    -randomise the clickabe keyboard overall window position slightly +-30 pixels   #
# 3: Add a "characters to complete block" counter under/on top of Cleartext.         #
# 4: Place Clickable Keyboard higher up if it exceeds the screen boundaries.         #
# 5: Allow use of SHA3 to replace SHA2 in PBKDF2 key generation.                     #
# 6: Public Key Cryptography - PGP                                                   #
#                                                                                    #
#                                                                                    #
######################################################################################
# Import the packages Python needs                                                   #
######################################################################################
import os
import sys
import platform
import binascii
import tkMessageBox
import tkFont
import random
from time import time
from aes import AES
from pbkdf2 import PBKDF2
from hashlib import sha256 as SHA256
from idlelib import ToolTip
import _tkinter
from Tkinter import *

if getattr(sys, 'frozen', False):
   # we are running in a |PyInstaller| bundle
   basedir = sys._MEIPASS
else:
   # we are running in a normal Python environment
   basedir = os.getcwd()


######################################################################################
# Define the Class for the Main Window                                               #
######################################################################################
class MainWindowFrame(Frame):

   #####################################################
   # Create Widgets in the main gui window
   #####################################################
   def createWidgets(self):
       #Need the global variable isBadOS to decide whether to activate ClearText widget
       global isBadOS

       Label(self, text="Clear Text").grid(row=9, column=20, pady=(20,0), sticky=E)
       self.ClearTextScrollbar = Scrollbar(self, orient=VERTICAL);
       self.ClearText = Text(self, width=100, height=70, yscrollcommand=self.ClearTextScrollbar.set, background="black", foreground="green", insertbackground="green", highlightthickness=0, undo=True);
       self.ClearTextScrollbar.config(command=self.ClearText.yview);
       self.ClearTextScrollbar.grid(row=10, rowspan=10, column=22, pady=(0,0), sticky=W+N+S);
       self.ClearText.grid( row = 10, rowspan=10, column = 2,columnspan=20, padx=(10,0), pady =(0,0), sticky=N+S+E+W);       
       self.ClearText.config(font=( "Courier", bestfontsize, 'bold' ))
       self.columnconfigure(2, weight=1)
       self.columnconfigure(21, weight=1)
       self.rowconfigure(10, weight=1)
       self.rowconfigure(19, weight=1)
       if isBadOS==1:
          self.ClearText.config(state=DISABLED)
          # NOTE: You can do this at least two ways, possibly three. I chose option 1: 
          # 1: Binding ButtonRelease-1 on the mouse means that the INSERT cursor always 
          #    goes to the position specified in callbackFunctionClearTextClickableKeyboard (i.e. clicked mouse position) 
          # 2: Binding to Button-1, but having a "self.after" inside callbackFuctionClearTextClickableKeyboard, delaying 
          #    by 10ms means the INSERT position is correctly set to the CURRENT mouse pos.
          # 3: Modify the ClearText Widget <Button-1> binding to delay by 10ms.
          self.ClearText.bind("<ButtonRelease-1>", self.callbackFunctionClearTextClickableKeyboard)
       self.ClearTextKeyboardOpened=0

       self.DeleteClearTextButton = Button(self)
       self.DeleteClearTextButton["text"] = "Delete"
       self.DeleteClearTextButton["fg"] = "red"
       self.DeleteClearTextButton["command"] = self.DeleteClearText
       self.DeleteClearTextButton.grid(row=9,column=21, pady=(20,0),padx=(0,0), sticky=S+W)      

       Label(self, text="Encrypted Text").grid(row=9, column=34, pady=(20,0), sticky=E)
       self.EncryptedTextScrollbar = Scrollbar(self, orient=VERTICAL);
       self.EncryptedText = Text(self, width=100, height=70, yscrollcommand=self.EncryptedTextScrollbar.set, background="black", foreground="red", insertbackground="red", highlightthickness=0, undo=True);
       self.EncryptedTextScrollbar.config(command=self.EncryptedText.yview);
       self.EncryptedTextScrollbar.grid(row=10, rowspan=10, column =52, pady=(0,0), padx=(0,10),sticky=W+N+S);
       self.EncryptedText.grid(row=10, rowspan=10, column=32, columnspan=20, padx=(10,0), pady=(0,0), sticky=N+S+E+W);
       self.EncryptedText.config(font=( "Courier", bestfontsize, 'bold' ))
       self.columnconfigure(31, weight=1)
       self.columnconfigure(34, weight=1)
       self.columnconfigure(49, weight=1)
       self.rowconfigure(10, weight=1)
       self.rowconfigure(19, weight=1)

       self.DeleteEncryptedTextButton = Button(self)
       self.DeleteEncryptedTextButton["text"] = "Delete"
       self.DeleteEncryptedTextButton["fg"] = "red"
       self.DeleteEncryptedTextButton["command"] = self.DeleteEncryptedText
       self.DeleteEncryptedTextButton.grid(row=9,column=35, pady=(20,0),padx=(0,0), sticky=S+W)      

       self.ChosenEncryptMethod=StringVar()
       self.ChosenEncryptMethod.set("AES-128 CBC") #default value
       self.EncryptMethod = OptionMenu( self, self.ChosenEncryptMethod, "AES-128 CBC", "AES-128 ECB");
       self.EncryptMethod.grid(row=12,column=27,pady=(40,0),padx=10,sticky=S)
       ToolTip.ToolTip(self.EncryptMethod, 'Cipher Mode: CBC-mode is recommended.')
              
       self.Encrypt = Button(self)
       self.Encrypt["text"] = ">>ENCRYPT>>"
       self.Encrypt["fg"] = "red"
       self.Encrypt["command"] = self.ValidateEncryptText
       self.Encrypt.grid(row=13,column=27, pady=(0,0),padx=10, sticky=S+N)      
       
       self.Decrypt = Button(self)
       self.Decrypt["text"] = "<<DECRYPT<<"
       self.Decrypt["fg"] = "red"
       self.Decrypt["command"] = self.ValidateDecryptText
       self.Decrypt.grid(row=14,column=27, pady=(0,00),padx=10, sticky=N)      
        
       self.CheckBoxValueHexMode=IntVar()
       self.HexModeButton = Checkbutton(self)
       self.HexModeButton["text"] = "Hex Mode"
       self.HexModeButton["command"] = self.HexEnable
       self.HexModeButton["variable"] = self.CheckBoxValueHexMode
       self.HexModeButton.grid(row=15,column=27,padx=(80,60), pady=(0,0), sticky=N+W) 
       ToolTip.ToolTip(self.HexModeButton, 'Hex Mode: Used for trying out Known Answer Test (KAT) Vectors')       

       self.CheckBoxValueClickKeyMode=IntVar()
       self.ClickKeyModeButton = Checkbutton(self)
       self.ClickKeyModeButton["text"] = "Click-to-type"
       self.ClickKeyModeButton["command"] = self.ClickToTypeEnable
       self.ClickKeyModeButton["variable"] = self.CheckBoxValueClickKeyMode
       self.ClickKeyModeButton.grid(row=16,column=27,padx=(80,60), pady=(0,0), sticky=N+W) 
       self.ClickKeyModeButton.select()
       self.ClickKeyModeButton.config(state=DISABLED)
       ToolTip.ToolTip(self.ClickKeyModeButton, 'Click-to-type Mode: Improves user security with "Clickable Keyboards", if keylogging is suspected.')       
       if isBadOS==0:
          self.ClickKeyModeButton.config(state=NORMAL) 
          self.ClickKeyModeButton.deselect()
          #Disable the "click-to-type" button until after we prepare the application and display our message to the user regarding bad OSes.
          self.ClickKeyModeButton.config(state=DISABLED)

       self.CheckBoxValueDisplayEyes=IntVar()
       self.DisplayEyesButton = Checkbutton(self)
       self.DisplayEyesButton["text"] = "Eyes"
       self.DisplayEyesButton["command"] = self.DisplayEyes
       self.DisplayEyesButton["variable"] = self.CheckBoxValueDisplayEyes
       self.DisplayEyesButton.grid(row=17,column=27,padx=(80,60), pady=(0,0), sticky=N+W) 
       self.DisplayEyesButton.config(state=DISABLED)

       self.CheckBoxValueDisplayDonate=IntVar()
       self.DisplayDonateButton = Checkbutton(self)
       self.DisplayDonateButton["text"] = "Donate"
       self.DisplayDonateButton["command"] = self.DisplayDonate
       self.DisplayDonateButton["variable"] = self.CheckBoxValueDisplayDonate
       self.DisplayDonateButton.grid(row=18,column=27,padx=(80,60), pady=(0,10), sticky=N+W) 
       self.DisplayDonateButton.config(state=DISABLED)


       self.TextFontButtonLabel = Label(self, text="Font Size")
       self.TextFontButtonLabel.grid(row=19,column=27,padx=(0),sticky=N+E+W)
       
       self.TempFontOffset=0

       self.TextFontPlus = Button(self)
       self.TextFontPlus["text"] = "+"
       self.TextFontPlus["fg"] = "red"
       self.TextFontPlus["command"] = self.TextFontPlusTwo
       self.TextFontPlus.grid(row=19,column=27, pady=(0,0),padx=(100,0), sticky=N)      


       self.TextFontMinus = Button(self)
       self.TextFontMinus["text"] = "-"
       self.TextFontMinus["fg"] = "red"
       self.TextFontMinus["command"] = self.TextFontMinusTwo
       self.TextFontMinus.grid(row=19,column=27, pady=(0,0),padx=(0,100), sticky=N)      




       self.user_entry_password= self.makeentry(self, 30, show="*", background="black",foreground="yellow", insertbackground="yellow",highlightthickness=0, disabledforeground="yellow",disabledbackground="black",font=( 'arial', bestfontsize ));
       self.user_entry_password.grid( row= 29, column=27,columnspan=5,pady=(80,0), sticky=W+S)
       Label(self, text="Password (Secret!):").grid(row=29, column=21, padx=(10,0),pady=(80,0), sticky=E+S)
       if isBadOS==1:
          self.user_entry_password.config(state=DISABLED)
          # NOTE: ENTRY WIDGETS behave differently to Text widgets. 
          # Firstly, they dont accept 'tags' so mycurs / mycurslinehi won't work.
          # (these user tags were the reason i used ButtonRelease-1 for the callback in the text widget, as they updated the cursor position properly when using ButtonRelease-1)
          # Next, if we trigger on ButtonRelease-1, the widget appears to become active again on Button-1 (despite being DISABLED direcly above here!).
          # This, I think, is wholly different to the text widget behaviour; which stays disabled if we trigger on ButtonRelease-1.
          # So, we trigger on Button-1 and immediately DISABLE the widget in the callback.
          self.user_entry_password.bind("<Button-1>", self.callbackFunctionPasswordClickableKeyboard)
       self.PasswordKeyboardOpened=0

       self.CheckBoxValueDisplayPassword=IntVar()
       self.DisplayPasswordButton = Checkbutton(self)
       self.DisplayPasswordButton["text"] = "Reveal"
       self.DisplayPasswordButton["command"] = self.ShowHidePass 
       self.DisplayPasswordButton["variable"] = self.CheckBoxValueDisplayPassword
       self.DisplayPasswordButton.grid(row=29,column=32,padx=(0,0), pady=(80,0), sticky=W) 

       self.user_entry_salt= self.makeentry(self, 30, background="black",foreground="yellow", insertbackground="yellow",highlightthickness=0, disabledforeground="gray50",disabledbackground="gray81", font='arial');
       self.user_entry_salt.grid( row= 30, column=27,pady=(0,0), sticky=W+N+S)
       self.user_entry_salt_label=Label(self, fg="gray50" ,text="Password Salt:")
       self.user_entry_salt_label.grid(row=30, column=21, padx=(10,0),pady=(0,0), sticky=E)
       self.user_entry_salt.config(state=DISABLED)
       ToolTip.ToolTip(self.user_entry_salt, "Salt: Generated at random for each encryption, combined with 'Password' to make 'Key'. NEVER re-use a 'Salt'.")       
       self.CheckBoxValueEnableSaltEntry=IntVar()
       self.EnableSaltEntryButton = Checkbutton(self)
       self.EnableSaltEntryButton["text"] = "Enable"
       self.EnableSaltEntryButton["command"] = self.EnableSaltEntry
       self.EnableSaltEntryButton["variable"] = self.CheckBoxValueEnableSaltEntry
       self.EnableSaltEntryButton.grid(row=30,column=33,padx=(0,0), pady=(0,0), sticky=W) 

       self.CheckBoxValueEnableSaltOverride=IntVar()
       self.EnableSaltOverrideButton = Checkbutton(self)
       self.EnableSaltOverrideButton["text"] = "Keep"
       self.EnableSaltOverrideButton["command"] = self.EnableSaltOverride
       self.EnableSaltOverrideButton["variable"] = self.CheckBoxValueEnableSaltOverride
       self.EnableSaltOverrideButton.grid(row=30,column=34,padx=(0,0), pady=(0,0), sticky=W) 

       self.user_entry_key= self.makeentry(self, 30, show="*", background="black",foreground="yellow", insertbackground="yellow",highlightthickness=0, disabledforeground="gray50",disabledbackground="gray81", font='arial');
       self.user_entry_key.grid( row= 31, column=27,pady=(0,0), sticky=W+N+S)
       self.user_entry_key_label=Label(self, fg="gray50", text="Key (Secret!):")
       self.user_entry_key_label.grid(row=31, column=21, padx=(10,0),pady=(0,0), sticky=E+N)
       self.user_entry_key.config(state=DISABLED)
       ToolTip.ToolTip(self.user_entry_key, "Key: Generated from the 'Password' and 'Salt' for each encryption action.")       

       self.CheckBoxValueDisplayKey=IntVar()
       self.DisplayKeyButton = Checkbutton(self)
       self.DisplayKeyButton["text"] = "Reveal"
       self.DisplayKeyButton["command"] = self.ShowHideKey
       self.DisplayKeyButton["variable"] = self.CheckBoxValueDisplayKey
       self.DisplayKeyButton.grid(row=31,column=32,padx=(0,0), pady=(0,0), sticky=W+N) 

       self.CheckBoxValueEnableKeyEntry=IntVar()
       self.EnableKeyEntryButton = Checkbutton(self)
       self.EnableKeyEntryButton["text"] = "Enable"
       self.EnableKeyEntryButton["command"] = self.EnableKeyEntry
       self.EnableKeyEntryButton["variable"] = self.CheckBoxValueEnableKeyEntry
       self.EnableKeyEntryButton.grid(row=31,column=33,padx=(0,0), pady=(0,0), sticky=W+N) 

       self.CheckBoxValueEnableKeyOverride=IntVar()
       self.EnableKeyOverrideButton = Checkbutton(self)
       self.EnableKeyOverrideButton["text"] = "Keep"
       self.EnableKeyOverrideButton["command"] = self.EnableKeyOverride
       self.EnableKeyOverrideButton["variable"] = self.CheckBoxValueEnableKeyOverride
       self.EnableKeyOverrideButton.grid(row=31,column=34,padx=(0,0), pady=(0,0), sticky=W+N) 

       self.user_entry_iv= self.makeentry(self, 30, background="black",foreground="yellow", insertbackground="yellow",highlightthickness=0, disabledforeground="gray50",disabledbackground="gray81",font='arial');
       self.user_entry_iv.grid( row= 32, column=27,pady=(0,0), sticky=W+N+S)
       self.user_entry_iv_label=Label(self, fg="gray50", text="IV:")
       self.user_entry_iv_label.grid(row=32, column=21, padx=(10,0),pady=(0,0), sticky=E+N)
       self.user_entry_iv.config(state=DISABLED)
       ToolTip.ToolTip(self.user_entry_iv, 'IV: Initialisation Vector, generated randomly for each message in certain modes (e.g. CBC). NEVER re-use an IV.')  

       self.CheckBoxValueEnableIvEntry=IntVar()
       self.EnableIvEntryButton = Checkbutton(self)
       self.EnableIvEntryButton["text"] = "Enable"
       self.EnableIvEntryButton["command"] = self.EnableIvEntry
       self.EnableIvEntryButton["variable"] = self.CheckBoxValueEnableIvEntry
       self.EnableIvEntryButton.grid(row=32,column=33,padx=(0,0), pady=(0,0), sticky=W+N) 

       self.CheckBoxValueEnableIvOverride=IntVar()
       self.EnableIvOverrideButton = Checkbutton(self)
       self.EnableIvOverrideButton["text"] = "Keep"
       self.EnableIvOverrideButton["command"] = self.EnableIvOverride
       self.EnableIvOverrideButton["variable"] = self.CheckBoxValueEnableIvOverride
       self.EnableIvOverrideButton.grid(row=32,column=34,padx=(0,0), pady=(0,0), sticky=W+N) 

       self.user_entry_pbkdf2_iter= self.makeentry(self, 30, show="", background="black",foreground="yellow", insertbackground="yellow",highlightthickness=0, disabledforeground="gray50",disabledbackground="gray81",font='arial');
       self.user_entry_pbkdf2_iter.grid( row= 33, column=27,pady=(0,20),padx=(0,0), sticky=W+N)
       self.user_entry_pbkdf2_iter_label=Label(self, fg="gray50", text="PBKDF2 iterations")
       self.user_entry_pbkdf2_iter_label.grid(row=33, column=21, padx=(10,0),pady=(0,20), sticky=E+N)
       self.user_entry_pbkdf2_iter.insert(0,"16384")
       self.user_entry_pbkdf2_iter.config(state=DISABLED)
       ToolTip.ToolTip(self.user_entry_pbkdf2_iter, 'PBKDF2 iterations: The number of cycles used in Key derivation. If you change this, you must agree it with the recipient.')       

       self.CheckBoxValueEnablePBKDF2Entry=IntVar()
       self.EnablePBKDF2EntryButton = Checkbutton(self)
       self.EnablePBKDF2EntryButton["text"] = "Enable"
       self.EnablePBKDF2EntryButton["command"] = self.EnablePBKDF2Entry
       self.EnablePBKDF2EntryButton["variable"] = self.CheckBoxValueEnablePBKDF2Entry
       self.EnablePBKDF2EntryButton.grid(row=33,column=33,padx=(0,0), pady=(0,20), sticky=W+N) 

       self.HELP = Button(self)
       self.HELP["text"] = "HELP"
       self.HELP["fg"] = "red"
       self.HELP["command"] = self.HelpWindow
       self.HELP.grid(row=33,column=50, pady=(0,20),padx=(10,0), sticky=E+N)      

       self.QUIT = Button(self)
       self.QUIT["text"] = "QUIT"
       self.QUIT["fg"] = "red"
       self.QUIT["command"] = sys.exit
       self.QUIT.grid(row=33,column=51, pady=(0,20),padx=(0,10), sticky=E+N)      


   #####################################################
   # Functions called by the buttons/widgets
   #####################################################
   def ShowHidePass(self):
       if self.CheckBoxValueDisplayPassword.get()==1:
          self.user_entry_password.configure(show="")
       else:
          self.user_entry_password.configure(show="*")
       # If a Clickable Keyboard exists, raise it to the front. Users hate the keyboard disappearing
       # when they try to reveal/hide the password..
       if self.PasswordKeyboardOpened==1:
          self.PasswordClickable.parentwidgetKeyboardWin.focus_force() #<-This appears to help in linux; providing immediate keyboard focus on raise.
          self.PasswordClickable.parentwidgetKeyboardWin.lift()
   
   def ShowHideKey(self):
       if self.CheckBoxValueDisplayKey.get()==1:
          self.user_entry_key.configure(show="")
       else:
          self.user_entry_key.configure(show="*")

   def makeentry(self,parent, width=None, **options):
       entry = Entry(parent, **options)
       if width:
           entry.config(width=width)
       return entry

   def HexEnable(self):
       validate=""
       validate=self.HexCheck()
       # open a new window to explain the error; in hex mode we can ONLY use 0-9&a/A,b/B,c/C,d/D,e/E,f/F       
       if validate!="":     
          # only need to complain to the user if we are entering (not leaving) hex mode. 
          if self.CheckBoxValueHexMode.get()==1:
             self.HexModeButton.deselect()           
             tkMessageBox.showwarning("Invalid Characters in HEX mode", "%s has invalid characters. \n\nIn HEX mode, only characters \n[0..9, a..f, A..F] are allowed.\n\n--NO SPACES, or CR/LF's!--" % validate )

   def EnableKeyEntry(self):
      if self.CheckBoxValueEnableKeyEntry.get()==1:
         self.user_entry_key.config(state=NORMAL)
         self.user_entry_key_label.configure(fg="black")
      else:
         self.user_entry_key_label.configure(fg="gray50")
         self.user_entry_key.config(state=DISABLED)

   def EnableSaltEntry(self):
      if self.CheckBoxValueEnableSaltEntry.get()==1:
         self.user_entry_salt.config(state=NORMAL)
         self.user_entry_salt_label.configure(fg="black")
      else:
         self.user_entry_salt_label.configure(fg="gray50")
         self.user_entry_salt.config(state=DISABLED)

   def EnableIvEntry(self):
      if self.CheckBoxValueEnableIvEntry.get()==1:
         self.user_entry_iv.config(state=NORMAL)
         self.user_entry_iv_label.configure(fg="black")
      else:
         self.user_entry_iv_label.configure(fg="gray50")
         self.user_entry_iv.config(state=DISABLED)

   def EnablePBKDF2Entry(self):
      if self.CheckBoxValueEnablePBKDF2Entry.get()==1:
         tkMessageBox.showwarning("Warning", "Changing PBKDF2 iterations: \n\nIf you change this value, you MUST tell your intended recipient, otherwise they will not be able to generate the Key \n-even if they have the correct password!" )
         self.user_entry_pbkdf2_iter.config(state=NORMAL)
         self.user_entry_pbkdf2_iter_label.configure(fg="black")
      else:
         self.user_entry_pbkdf2_iter_label.configure(fg="gray50")
         self.user_entry_pbkdf2_iter.config(state=DISABLED)
      
   def EnableSaltOverride(self):
      if self.CheckBoxValueEnableSaltOverride.get()==1:
         tkMessageBox.showwarning("Encryption Warning", "Keeping 'Salt': This should only ever be used for testing purposes. \n\nNEVER re-use a salt for an encrypted message." )

   def EnableKeyOverride(self):
      if self.CheckBoxValueEnableKeyOverride.get()==1:
         tkMessageBox.showwarning("Encryption Warning", "Keeping 'Key': This should only ever be used for testing purposes. \n\nNEVER re-use a key for an encrypted message." )

   def EnableIvOverride(self):
      if self.CheckBoxValueEnableIvOverride.get()==1:
         tkMessageBox.showwarning("Encryption Warning", "Keeping 'IV': This should only ever be used for testing purposes. \n\nNEVER re-use an IV for an encrypted message." )
       
   def TextFontPlusTwo(self):
      self.TempFontOffset=self.TempFontOffset+2
      self.ClearText.config(font=( "Courier", bestfontsize+self.TempFontOffset, 'bold' ))       
      self.EncryptedText.config(font=( "Courier", bestfontsize+self.TempFontOffset, 'bold' ))       
      self.user_entry_password.config(font=("arial",root.bestpasswordfontsize+self.TempFontOffset))

   def TextFontMinusTwo(self):
      self.TempFontOffset=self.TempFontOffset-2
      self.ClearText.config(font=( "Courier", bestfontsize+self.TempFontOffset, 'bold' ))       
      self.EncryptedText.config(font=( "Courier", bestfontsize+self.TempFontOffset, 'bold' ))       
      self.user_entry_password.config(font=("arial",root.bestpasswordfontsize+self.TempFontOffset))



   #####################################################
   # Function to handle the "Click-to-type" button
   #####################################################
   def ClickToTypeEnable(self):
      if self.CheckBoxValueClickKeyMode.get()==0:
         # We are disabling the "Click-to-type" mode.
         # Kill all clickable keyboards.
         # Set cleartext and password widget status to 'normal'.
         # Delete the custom tags for cursor/highlight
         # Unbind the ButtonRelease-1 or Button-1 for the two previously disabled widgets.
         #   - Note: ButtonRelease-1 for text widget, Button-1 for Entry widget (due to cursor).
         # Try to restore focus to the widget which should have focus.
         self.ClearText.config(state=NORMAL)
         self.user_entry_password.config(state=NORMAL)
         self.ClearText.tag_remove('mycurs', 1.0, 'end')
         self.ClearText.tag_remove('mycurslinehi', 1.0, 'end')
         self.ClearText.unbind("<ButtonRelease-1>")
         self.user_entry_password.unbind("<Button-1>")
         if self.PasswordKeyboardOpened==1:
            self.PasswordClickable.on_closing_parentwidgetKeyboardWin()
         if self.ClearTextKeyboardOpened==1:
            self.ClearTextClickable.on_closing_parentwidgetKeyboardWin()
         # EXPLICITY tell the code here to focus on something.
         self.predisabledfocussedwidget.focus_force()
      else:
         # We are enabling "Click-to-type" mode.
         # Bind the ButtonRelease-1 or Button-1 for the two previously enabled widgets.
         #   - Note: ButtonRelease-1 for text widget, Button-1 for Entry widget (due to cursor).
         # Make sure we deactivate the cleartext and password widgets.
         # If current focus is on ClearText widget, open a clickable keyboard (use a dummy event parameter).
         # If current focus is on Password widget, open a clickable keyboard (use a dummy event parameter).
         self.predisabledfocussedwidget=self.focus_get()
         self.ClearText.bind("<ButtonRelease-1>", self.callbackFunctionClearTextClickableKeyboard)
         self.user_entry_password.bind("<Button-1>", self.callbackFunctionPasswordClickableKeyboard)
         self.ClearText.config(state=DISABLED)
         self.user_entry_password.config(state=DISABLED)
         if self.focus_get() == self.ClearText:
            self.EncryptedText.focus_force()
            self.callbackFunctionClearTextClickableKeyboard("dummy")
         if self.focus_get() == self.user_entry_password:
            self.callbackFunctionPasswordClickableKeyboard("dummy")


   #####################################################
   # When in Click-to-type mode, This function is called 
   # by the Event Handler when the parent-window "ClearText" 
   # widget is clicked. 
   # It has to be a function; the eventhandler requires 
   # it to be so, and to expect the "event" argument.
   #####################################################
   def callbackFunctionClearTextClickableKeyboard(self,event):
      # Place the focus back in ClearText if "Click-to-type" is deselected. 
      self.predisabledfocussedwidget=self.ClearText

      # Configure a tag called "mycurs" (the insert position) and "mycurslinehi" (the line is highlighted slightly)
      # After Clearing any previous "mycurs" cursor, set the "cursor" to the correct position.
      # Then clear out any "mycurslinehi" highlights, and re-add at the current line.
      # Since we KNOW the mouse was clicked in order to get here, set the INSERT point to "CURRENT" (mouse-click position).
      # I bound the call to this Class/Function (e.g from the ClearText Widget) to the <Button-Release-1> event, 
      self.ClearText.tag_configure("mycurs", background="gray40")
      self.ClearText.tag_remove('mycurs', 1.0, 'end')
      self.ClearText.mark_set('insert' , 'current')
      self.ClearText.tag_add("mycurs", INSERT+'-0c', INSERT+'+1c')
      self.ClearText.see(INSERT)
      
      # This tag sets the rest of the line to a slightly more visible grey 
      # if the cursor is at the end of the text.
      self.ClearText.tag_configure("mycurslinehi", background="grey20")
      self.ClearText.tag_remove('mycurslinehi', 1.0, 'end')
      self.ClearText.tag_add("mycurslinehi", 'insert lineend', 'insert lineend'+'+1c')

      # If We have an already existing ClearText Clickable Keyboard,  
      # we "lift()" instead of force_focus and grab_set.
      if self.ClearTextKeyboardOpened==1:
         self.ClearTextClickable.parentwidgetKeyboardWin.focus_force() #<-This appears to help in linux; providing immediate keyboard focus on raise.
         self.ClearTextClickable.parentwidgetKeyboardWin.lift()
         
         # Get the parent Window's x,y position so we can use it together with the ClearText widget's size/offset
         # to correctly position the Clickable Keyboard.
         MainWindowOffsetX=self.winfo_rootx()
         MainWindowOffsetY=self.winfo_rooty()
         
         # Get the ClearText widget's position, height & width so we can position the offset of the Clickable Keyboard
         ClearTextGeometry=self.ClearText.winfo_geometry()
         ClearTextWidth  = ClearTextGeometry.split('+')[0].split('x')[0]
         ClearTextHeight = ClearTextGeometry.split('+')[0].split('x')[1]
         ClearTextOffsetX= ClearTextGeometry.split('+')[1]
         ClearTextOffsetY= ClearTextGeometry.split('+')[2]

         # Get the position to put the Ckickable Keyboard
         KeyboardOffsetX= int(MainWindowOffsetX) + int(ClearTextOffsetX) 
         KeyboardOffsetY= int(MainWindowOffsetY) + int(ClearTextOffsetY) + int(ClearTextHeight)
         self.ClearTextClickable.parentwidgetKeyboardWin.geometry("%dx%d+%d+%d" % ((self.ClearTextClickable.parentwidgetKeyboardWin.winfo_width(),self.ClearTextClickable.parentwidgetKeyboardWin.winfo_height()) + (KeyboardOffsetX,KeyboardOffsetY)))
         return
      else:
         # We don't have a ClickableKeyboard instance yet, so create
         # one named "self.ClearTextClickable", and set the class
         # variable "ClearTextKeyboardOpened".
         self.ClearTextClickable=ClickableKeyboard(self,self.ClearText)
         self.ClearTextKeyboardOpened=1         


   #####################################################
   # When in Click-to-type mode, This function is called 
   # by the Event Handler when the parent-window "Password" 
   # widget is clicked. 
   # It has to be a function; the eventhandler requires 
   # it to be so, and to expect the "event" argument.
   #####################################################
   def callbackFunctionPasswordClickableKeyboard(self,event):
      # Place the focus back in user_entry_password if "Click-to-type" is deselected. 
      self.predisabledfocussedwidget=self.user_entry_password

      # The Password widget becomes ACTIVE/NORMAL again after pressing "BKSP" and getting a "bad entry index", and then clicking on the Password widget.
      # Could be safer to have it here, as insurance against a TclError allowing manual entry. 
      self.user_entry_password.config(state=DISABLED)

      # If We have an already existing Password Clickable Keyboard,  
      # we "lift()" instead of force_focus and grab_set.
      if self.PasswordKeyboardOpened==1:
         self.PasswordClickable.parentwidgetKeyboardWin.focus_force() #<-This appears to help in linux; providing immediate keyboard focus on raise.
         self.PasswordClickable.parentwidgetKeyboardWin.lift()
         
         # Get the parent Window's x,y position so we can use it together with the ClearText widget's size/offset
         # to correctly position the Clickable Keyboard.
         MainWindowOffsetX=self.winfo_rootx()
         MainWindowOffsetY=self.winfo_rooty()
         
         # Get the Password widget's position, height & width so we can position the offset of the Clickable Keyboard
         PasswordGeometry=self.user_entry_password.winfo_geometry()
         PasswordWidth  = PasswordGeometry.split('+')[0].split('x')[0]
         PasswordHeight = PasswordGeometry.split('+')[0].split('x')[1]
         PasswordOffsetX= PasswordGeometry.split('+')[1]
         PasswordOffsetY= PasswordGeometry.split('+')[2]

         # Get the position to put the Ckickable Keyboard
         KeyboardOffsetX= int(MainWindowOffsetX) + int(PasswordOffsetX) 
         KeyboardOffsetY= int(MainWindowOffsetY) + int(PasswordOffsetY) + int(PasswordHeight)

         # Windows has an annoying habit of masking a little of the Password Entry widget with the Password Clickable Keyboard Window.
         # so I add 5px to the y-value.
         global theOS
         if theOS=="Windows":
            KeyboardOffsetY=KeyboardOffsetY+5
            
         self.PasswordClickable.parentwidgetKeyboardWin.geometry("%dx%d+%d+%d" % ((self.PasswordClickable.parentwidgetKeyboardWin.winfo_width(),self.PasswordClickable.parentwidgetKeyboardWin.winfo_height()) + (KeyboardOffsetX,KeyboardOffsetY)))
         return
      else:
         # We don't have a ClickableKeyboard instance yet, so create
         # one named "self.PasswordClickable", and set the class
         # variable "PasswordKeyboardOpened".
         self.PasswordClickable=ClickableKeyboard(self,self.user_entry_password)
         self.PasswordKeyboardOpened=1         


   #####################################################
   # Functions to clean the windows
   #####################################################
   def DeleteClearText(self):
       if self.CheckBoxValueClickKeyMode.get()==1:
          self.ClearText.config(state=NORMAL)
       self.ClearText.delete(1.0,END) 
       if self.CheckBoxValueClickKeyMode.get()==1:
          self.ClearText.config(state=DISABLED)

   def DeleteEncryptedText(self):
       self.EncryptedText.delete(1.0,END)

   def CleanStart(self):
       self.DeleteClearText()
       self.DeleteEncryptedText()

   def CleanStartFirstEyesDonate(self):
       self.DisplayEyesButton.config(state=NORMAL)
       self.DisplayDonateButton.config(state=NORMAL)

       # Clear the windows.
       self.CleanStart()

       # Warn the user that they'll have to use the Clickable Keyboard if a "bad" OS
       # has been detected.
       if self.CheckBoxValueClickKeyMode.get()==1:
          # Both print and showwarning...
          print "==============================================================="
          print "==============================================================="
          print "==============================================================="
          print ""
          print "               'Naughty' Operating System Detected!"
          print ""
          print "==============================================================="
          print "==============================================================="
          print "==============================================================="
          print ""
          print "Click-to-type mode:"
          print "-------------------"
          print "PyEyeCrypt will still run, but ClearText and Passwords MUST be "
          print "entered using the on-screen 'clickable' keyboards."
          print ""
          print "e.g. The new Windows 10 Privacy Statement includes the words:"
          print "'Your typed and handwritten words are collected'"
          print ""
          print "This behaviour is akin to a keylogging virus."
          print "Win 7 & 8 are also being updated by MS in a fashion which could"
          print "compromise your encryption. Amongst others, Ubuntu sends data"
          print "to 'Cannonical'"
          print ""
          print "This means that passwords typed by a single recipient using"
          print "Win10 or Ubuntu could, *unknown to the sender*, expose the"
          print "sender's password and (possibly) text!"
          print ""
          tkMessageBox.showwarning("WARNING", "'Naughty' Operating System Detected! \n\nClick-to-type mode: \n----------------\nPyEyeCrypt will still run, but ClearText and Passwords MUST be entered using the on-screen 'clickable' keyboards. \n\ne.g. The new Windows 10 Privacy Statement includes the words:\n'Your typed and handwritten words are collected.' \n\nThis behaviour is akin to a keylogging virus. Win 7 & 8 are also being updated in a fashion which could compromise your encryption. Amongst others, Ubuntu sends data to 'Cannonical'. \n\nThis means, for example, that passwords typed by a single recipient using Win10 or Ubuntu could, *unknown to the sender*, expose the sender's password and (possibly) text! ")
       # Now, and only now, can we enable the "Click-to-type' checkbox
       # We must only enable it if it is unchecked (indicating a good OS)
       else:    
         self.ClickKeyModeButton.config(state=NORMAL)


   #####################################################
   # Function to supply "numberofbytes" of random hex
   # Add as many other sources of randomness as possible, 
   # XOR'd with some non-truly random, but hard-to-guess numbers.
   #####################################################
   def getrandombytes(self, numberofbytes):
      randombytes=0

      # The output of "binascii.hexlify(urandombytes)"
      # will be a hex number having one hex digit for each 4 bits (i.e. 2 hex digits for each byte)
      # Important: if the leading digit is 0, this WILL be included.
      urandombytes = os.urandom(numberofbytes)

      # The output of "random.getrandbits(numberofbits)"
      # will not necessarily have leading 0's. 
      # This is ok, but we must be careful in the XOR
      # not to lose digits!
      # It is important to note that we seeded "random.seed()" with
      # the values from user keyboard strokes (timings) in EntropyWindow;
      # which should be moderately random.
      numberofbits=numberofbytes*8
      PRNG1randombits=random.getrandbits(numberofbits)

      # Here, we XOR the previous "os.urandom" value with 
      # the output of random.getrandbits().
      #    - Randomness is preserved by a bit-wise XOR (^) operation.
      #    - A random bit XORed with a non-random bit will result in a random bit.
      #    - Multiple sources of potentially random data can be combined using XOR,
      #      and the unpredictability of the output is guaranteed to be
      #      at least as good as the best individual source.
      inturandombytes=int(urandombytes.encode("hex"),16)
      intxorrandombytes=inturandombytes ^ PRNG1randombits
      randombytes= "%x" % intxorrandombytes

      # We return Hex digits in "randombytesfilled", 
      # which means 4 bits per hex character of "randombytesfilled".
      # Hence, the zfill needs to occupy "numberofbytes*2" hex chars (at 8 bits per byte).
      randombytesfilled=randombytes.zfill(numberofbytes*2)
      return randombytesfilled


   #####################################################
   # Function to check the content of user-entered fields 
   # for non-Hex characters.
   # Use of this function should ALWAYS be error-trapped
   # to check for a return value of "errorTripped".
   #####################################################
   def HexCheck(self):
       allowed = "abcdefABCDEF0123456789"
       errorTripped=""

       #The Key, Salt & IV should always be in hex; check these regardless.
       for hexchar in self.user_entry_key.get():
          if hexchar not in allowed:
              #Trip the ERROR variable so we know there's a char in the text which is not allowed for HEX mode.
              errorTripped="Key"
       for hexchar in self.user_entry_salt.get():
          if hexchar not in allowed:
              #Trip the ERROR variable so we know there's a char in the text which is not allowed for HEX mode.
              errorTripped="Salt"
       for hexchar in self.user_entry_iv.get():
          if hexchar not in allowed:
             #Trip the ERROR variable so we know there's a char in the text which is not allowed for HEX mode. 
             errorTripped="IV"

       EncryptedTextContent=self.EncryptedText.get("1.0",END)
       if EncryptedTextContent[-1:] == '\n':
          EncryptedTextContent = EncryptedTextContent[:-1]
       for hexchar in EncryptedTextContent:
          if hexchar not in allowed:
             #Trip the ERROR variable so we know there's a char in the text which is not allowed for HEX mode.
             errorTripped="Encrypted Text Window"                              
             
       # Do the following extra checks on ClearText, if we are in hex mode:      
       if self.CheckBoxValueHexMode.get()==1:
          #get the contents of cleartext, key and encrypted text and see if only 0-9&a/A,b/B,c/C,d/D,e/E,f/F
          ClearTextContent=self.ClearText.get("1.0",END)
          if ClearTextContent[-1:] == '\n':
             ClearTextContent = ClearTextContent[:-1]
          for hexchar in ClearTextContent:
             if hexchar not in allowed:
                #Trip the ERROR variable so we know there's a char in the text which is not allowed for HEX mode.
                errorTripped="Clear Text Window"

       # Finally, return the value in "errorTripped" to the calling function         
       return errorTripped


   #####################################################
   # Function to clean the content of user-entered fields 
   # for Spaces and CF/LF (ENTER) characters. 
   #
   # It is common for cut/pastes into the EncryptedText field 
   # to have extra spaces /enter characters.
   #
   # Use of this function should ALWAYS be error-trapped
   # to check for a return value of "errorTripped".
   #####################################################
   def HexCleanup(self, widgetToClean):
       errorTripped=""
       spaceTripped=0
       enterTripped=0
       # NB: If widgetToClean is not "editable" except via clickable keyboard, need to make it editable..
       # NB: Not a problem for EncryptedText, as this is always editable/cut-pasteable for all OS's
       
       # Remove any errant SPACEs in the widget contents...
       idx='1.0'
       while 1:
          # find next occurrence of SPACE (" "), exit loop if no more
          idx = widgetToClean.search(" ", idx, nocase=1, stopindex=END)
          if not idx: break
          widgetToClean.delete(idx)
          spaceTripped=1

       # Remove any errant ENTER characters in the widget contents...
       idx='1.0'
       while 1:
          # find next occurrence of ENTER ("\n"), exit loop if no more
          # and rememeber, the last char in a text widget is a \n, so we leave that one for later..
          idx = widgetToClean.search("\n", idx, nocase=1, stopindex="end - 1 chars")
          if not idx: break
          widgetToClean.delete(idx)
          enterTripped=1

       if spaceTripped==1:
          errorTripped=errorTripped+"--Automatically deleted SPACES..\n"
       if enterTripped==1:
          errorTripped=errorTripped+" --Automatically deleted ENTER characters..\n"
          
       # Finally, return the value in "errorTripped" to the calling function         
       return errorTripped




   #####################################################
   # Function to provide random HEX padding, when given a 
   # current number of bits and a desired number of bits
   # (lengthOfHexlifiedContentInBits and BlockSizeInBits 
   # respectively).
   # Use of this function should ALWAYS be error-trapped
   # to check for a return value of "PaddingError".
   #####################################################
   def PadTo128Bits(self,lengthOfHexlifiedContentInBits,BlockSizeInBits):
      hexpadding=""

      # We *should* have already done this before calling the function, 
      # but just to make sure, check that we do actually need to pad.
      if ( lengthOfHexlifiedContentInBits % BlockSizeInBits ) !=0:
         # Get the actual missing number of bits:
         missingbitcalc=lengthOfHexlifiedContentInBits
         while (missingbitcalc > BlockSizeInBits):
            missingbitcalc=missingbitcalc-BlockSizeInBits
         finalmissingbits=BlockSizeInBits-missingbitcalc

         # Asking for "randombytes=(float(finalmissingbits)/float(8)) +0.5" will force it to round up. 
         numberofbytesrequired=int(float(finalmissingbits)/float(8) +0.5)
         randombytes=self.getrandombytes( numberofbytesrequired )
             
         # Now, we have "randombytes" which is a HEX string (4 bits per char) of length "numberofbytesrequired" bytes.
         # We've converted the Text to HEX, so each missing hex digit is 4 bits.
         # i.e. one byte of randombytes equates to two HEX characters.
         # The number of HEX digits we append is "finalmissingbits/4", which should be an integer.
         hexdigitsrequired=finalmissingbits/4

         #This IF statement should ALWAYS be fulfilled, I just put it here for safety.
         if ( hexdigitsrequired <=  (numberofbytesrequired*2)  ):
            hexpadding=randombytes[-hexdigitsrequired:]
         else:
            tkMessageBox.showwarning("Padding Text", "PadTo128Bits(): Error in calculating HEX Digits required. Padding FAILED." )
            return "PaddingError"         

         # Warn the user their Clear Text is being padded.
         tkMessageBox.showwarning("Padding Text", "Text (%s bits) is not a multiple of %s bits. Padding..  \n\nNOTE: When this text is DEcrypted, it will have spurious extra characters at the end of the message. \n\nEither lengthen the message yourself, or warn the recipient." % (lengthOfHexlifiedContentInBits,BlockSizeInBits))
         return hexpadding
      else:
         tkMessageBox.showwarning("Padding Cleartext", "PadTo128Bits(): Error - Padding not required, yet PadTo128Bits() was called. Padding FAILED." )
         return "PaddingError"       

         
   #####################################################
   # VALIDATE ENCRYPT section
   #####################################################
   def ValidateEncryptText(self):
       # Function MUST NOT do anything IF "Eyes" or "Donate" buttons checked.
       if self.CheckBoxValueDisplayDonate.get()==1:
          tkMessageBox.showwarning("'Donate' Checkbox is Active", "'Donate' Checkbox must be deactivated to encrypt" )
          return 1
       if self.CheckBoxValueDisplayEyes.get()==1:
          tkMessageBox.showwarning("'Eyes' Checkbox is Active", "'Eyes' Checkbox must be deactivated to encrypt" )
          return 2

       # Function MUST NOT do anything IF "EncryptedText" has data.
       # Unfortunately, the get() adds a newline to the text widget contents.
       # So, we must strip the trailing newline
       EncryptedTextContent=self.EncryptedText.get("1.0",END)
       if EncryptedTextContent[-1:] == '\n':
          EncryptedTextContent = EncryptedTextContent[:-1]
       if EncryptedTextContent!="":
          tkMessageBox.showwarning("Encrypt Not Possible", "Encrypted Text area must be empty to encrypt" )
          return 3

       # Function MUST NOT do anything IF "ClearText" is empty.
       # Unfortunately, the get() adds a newline to the text widget contents.
       # So, we must strip the trailing newline
       ClearTextContent=self.ClearText.get("1.0",END)
       if ClearTextContent[-1:] == '\n':
          ClearTextContent = ClearTextContent[:-1]
       if ClearTextContent=="":
          tkMessageBox.showwarning("Encrypt Not Possible", "Clear Text area is empty." )
          return 4

       # CHECK the PBKDF2 Iterations is a positive integer (allowed=01234567890) and NOT EMPTY
       # Do this whether 'ENABLE' is set or not (user could have disabled after changing it).
       PBKDF2iterations=self.user_entry_pbkdf2_iter.get()
       if PBKDF2iterations == "":
          #Trip an ERROR
          tkMessageBox.showwarning("Encrypt Not Possible", "PBKDF2 iterations is empty. \n\nIt must be a positive integer to generate a Key, preferably in the tens of thousands, larger being more secure.")
          return 5
       posintallowed="0123456789"
       for numericposintchar in PBKDF2iterations:
          if numericposintchar not in posintallowed:
             #Trip the ERROR
             tkMessageBox.showwarning("Encrypt Not Possible", "PBKDF2 iterations must be a positive integer." )
             return 6
       if int(PBKDF2iterations) == 0:
          #Trip an ERROR
          tkMessageBox.showwarning("Encrypt Not Possible", "PBKDF2 iterations is zero. \n\nIt must be a positive integer to generate a Key, preferably in the tens of thousands, larger being more secure.")
          return 7

       # Blocksize, Keysize, ivsize, saltsize hold the number of bits for each of these variables.
       # Set initial values for blocksize, keysize, ivsize, saltsize to -1. 
       # --(A nonsense value designed to protect us in the case that somehow we go to encryption without setting the proper values.)
       # Then set values based on type of encryption selected.
       blocksize=-1
       keysize=-1
       ivsize=-1
       saltsize=-1
       if self.ChosenEncryptMethod.get()=="AES-128 CBC":
          blocksize=128
          keysize=128
          ivsize=128
          saltsize=128
       if self.ChosenEncryptMethod.get()=="AES-128 ECB":
          blocksize=128
          keysize=128
          ivsize=0
          saltsize=128

       # CALL GenerateSaltKeyIv here, with ivsize, keysize, saltsize.
       # Error-trap the call.
       resultOfSaltKeyIvGen=self.GenerateSaltKeyIv(keysize,ivsize,saltsize)
       if resultOfSaltKeyIvGen !="Success":
          # We probaby don' t need this 'showwarning' because every return code from self.GenerateSaltKeyIv() already has a 'showwarning' message anyway.
          # tkMessageBox.showwarning("Key Generation Failed", "Key generation has failed with error code %s. \n\nSorry, but it is not possible to proceed, until we can generate a Key for encryption." % resultOfSaltKeyIvGen )
          return 8

       # Check that salt is present/ right length.
       salt_text=self.user_entry_salt.get()
       if (len(salt_text)*4) != saltsize:
          tkMessageBox.showwarning("Encrypt Not Possible", "Can not produce encrypted text. \n\n'Salt' length is wrong number of bits. Should be %s bits." % saltsize  )
          return 9

       # Check that the Key is present
       if self.user_entry_key.get()=="":  
          tkMessageBox.showwarning("Encrypt Not Possible", "'Key' is empty." )
          return 10          

       # See if the Key is the right length -take each HEX digit as 4 bytes, so multiply by 4.
       key_text=self.user_entry_key.get()
       if (len(key_text)*4) != keysize:
          tkMessageBox.showwarning("Encrypt Not Possible", "'Key' length is wrong number of bits. Should be %s bits." % keysize  )
          return 11

       # See if the IV is the right size. This one CAN be empty in ECB mode, for example.
       iv_text=self.user_entry_iv.get()
       if (len(iv_text)*4) != ivsize:
          tkMessageBox.showwarning("Encrypt Not Possible", "'IV' is wrong length (%s bytes) . Should be %s bytes." % (len(iv_text)*4,ivsize)  )
          return 12

       # Check that Salt, Key, IV only contain HEX digits; regardless of whether we're in hex mode this should be true.
       validate=""
       validate=self.HexCheck()
       if validate!="":
          tkMessageBox.showwarning("Invalid Characters", "%s has invalid characters. \n\nOnly characters \n[0..9, a..f, A..F] are allowed.\n\n--NO SPACES, or CR/LF's!--" % validate )
          return 13   

       # Hexlify the Clear Text content (if needed), ready for padding.
       HexlifiedClearTextContent=""
       if self.CheckBoxValueHexMode.get()==1:
          #In HEX mode so ClearTextContent is ALREADY "Hexlified".
          HexlifiedClearTextContent=ClearTextContent
       else:
          #We are NOT in HEX mode
          # Convert the Clear Text to HEX.
          HexlifiedClearTextContent=binascii.hexlify(ClearTextContent.encode('utf8','strict'))

       #For AES, I require text to be a muliple of 128 bits. If it is not, I pad it with random hex.
       trailingpadding=""
       if ((len(HexlifiedClearTextContent)*4) % blocksize ) !=0:
          trailingpadding=self.PadTo128Bits( len(HexlifiedClearTextContent)*4, blocksize )
          #Error Trapping - should only consist of hex digits so we will never falsely detect an error if we look for "PaddingError"!
          if (trailingpadding=="PaddingError"):
             tkMessageBox.showwarning("Padding Cleartext", "Error in PadTo128Bits() Function. Padding FAILED." )
             return 14
       PaddedClearTextContent=HexlifiedClearTextContent+trailingpadding
       self.EncryptValidatedClearText(PaddedClearTextContent, key_text, ivsize, iv_text, blocksize, saltsize, salt_text)


   #####################################################
   # Function to Generate a Key, Salt and IV (if needed).
   # Will return non-zero if there is any hiccup
   # NB: The return value should ALWAYS be error-checked!
   # Start by ensuring a password is present, and that Key, 
   # Salt & IV are blank (if not, and keep is not flagged, blank them) 
   # --ready to accept computed values
   ######################################################
   def GenerateSaltKeyIv(self, keylengthinbits,ivlengthinbits, saltlengthinbits):
       # Firstly, the key, iv and salt must have the correct length for the encryption algo
       # This function generates a Key, using Salt, but also also generates an "IV" if needed. 
       # NB: we DON'T generate keys/salt or an IV when 'keep' checkbox is ticked, because it's assumed the 
       # user is trying out a Known Answer Test (KAT), where they want to enter manual values.

       # Reset the variables used to generate the key..
       passwordtext=""
       salttext=""
       
       # Check the password has some content.
       if self.user_entry_password.get()=="":  
          # We Don't necessarily need a password in HEX mode, because it is assumed the user will enter a HEX Key / IV.
          if self.CheckBoxValueHexMode.get()==0:
             tkMessageBox.showwarning("Key Generation Not Possible", "'Password' is empty." )
             return 1     
          else:
             # If "Key Keep" isnt checked OR "Key" has no entry, return an error, otherwise proceed.
             # NB length of key is checked after this function anyway.
             if self.CheckBoxValueEnableKeyOverride.get()==0 or self.user_entry_key.get()=="":
                tkMessageBox.showwarning("Key Generation Not Possible", "In HEX mode but 'Password' is empty. \n\nYou must manually enter a 'Key', and check the 'Keep' box." )
                return 2
       passwordtext=self.user_entry_password.get()      

       # If any of the 'Keep' flags are checked, we could have user content
       # which may or may not be hex, and may or may not be the correct length.
       # If none of the keep flags are checked, Salt, Key and IV should be blank.
       # for now, I will not force a check on the Salt length, since it can be useful to check 

       # Check the key is empty, unless 'Keep' is flagged.
       if self.user_entry_key.get()!="":  
          if self.CheckBoxValueEnableKeyOverride.get()==1:
             self.EnableKeyOverride()
          else:
             # CAREFUL: if Key field is not enabled, this insert will not work!
             keywasenableda=0
             if (self.CheckBoxValueEnableKeyEntry.get()==1):
                keywasenableda=1
             self.user_entry_key.config(state=NORMAL)   
             self.user_entry_key.delete(0,END)
             if (keywasenableda==0):
                # Set Key back to DISABLED!
                self.user_entry_key.config(state=DISABLED)
             
       # Check the IV is empty, unless 'Keep' is flagged.
       if self.user_entry_iv.get()!="":  
          if self.CheckBoxValueEnableIvOverride.get()==1:
             self.EnableIvOverride()
          else:
             # CAREFUL: if IV field is not enabled, this insert will not work!
             ivwasenableda=0
             if (self.CheckBoxValueEnableIvEntry.get()==1):
                ivwasenableda=1
             self.user_entry_iv.config(state=NORMAL)   
             self.user_entry_iv.delete(0,END)
             if (ivwasenableda==0):
                # Set IV back to DISABLED!
                self.user_entry_iv.config(state=DISABLED)

       # Check the Salt is empty, unless 'Keep' is flagged, in which case we only check if we have an even number of chars, 
       # otherwise we will crash Key generation
       if self.CheckBoxValueEnableSaltOverride.get()==1:
          self.EnableSaltOverride()
          if len(self.user_entry_salt.get()) != 0:
             if (len(self.user_entry_salt.get()) % 2) != 0:
                tkMessageBox.showwarning("Salt Not Usable Length", "'Salt' field is being 'Kept', but has an odd number of characters." )
                return 3
       else:
          if self.user_entry_salt.get()!="":
             # CAREFUL: if Salt field is not enabled, this insert will not work!
             saltwasenableda=0
             if (self.CheckBoxValueEnableSaltEntry.get()==1):
                saltwasenableda=1
             self.user_entry_salt.config(state=NORMAL)   
             self.user_entry_salt.delete(0,END)
             if (saltwasenableda==0):
                # Set Salt back to DISABLED!
                self.user_entry_salt.config(state=DISABLED)

       # If any of the 'Keep' Flags are checked, do a HexCheck() to make sure only Hex characters present.
       # NB I will NOT check the length of Salt, Key, or IV here if 'Keep' is flagged, since it can still be useful
       #    to generate keys from user-entered salts for PBKDF2 checking purposes (even if we don't intend to encrypt a message, just cross-check the key)
       #    (The Salt, Key ad IV lengths will be checked after we return to the calling function anyqway)    
       if self.CheckBoxValueEnableSaltOverride.get()==1 or self.CheckBoxValueEnableIvOverride.get()==1 or self.CheckBoxValueEnableKeyOverride.get()==1:
          validate=""
          validate=self.HexCheck()
          if validate !="":
             tkMessageBox.showwarning("Invalid Characters", "%s has invalid characters. \n\nOnly characters \n[0..9, a..f, A..F] are allowed.\n\n--NO SPACES, or CR/LF's!--" % validate )
             return 4

       # SALT   
       # Check the desired Salt Length is greater than 0, and divisible by 8.
       # This means we can ask for a salt having an integer number of bytes.
       if self.CheckBoxValueEnableSaltOverride.get()==0:    
          if saltlengthinbits > 0:             
             if (saltlengthinbits % 8 ) !=0:
                tkMessageBox.showwarning("Encrypt Not Possible", "Salt Length required (in bits, %s) is not divisible by 8" % saltlengthinbits )
                return 5
             else:
                # Basically, the rule is this: 
                #   if user_entry_salt is filled with hex chars, then you 'unhexlify' them in the PBKDF2 call
                #   (then 73616c74 does the same as user_entry_salt = "salt", verifiably for the 4096 iterations, for example.) 
                # IF USING THIS YOU HAVE TO HAVE THE 2 CALLs TO PBKDF2 WITH UNHEXLIFY:
                # 1: encrypt:  keyvalue = PBKDF2(passwordtext, binascii.unhexlify(salttext) ,64000).read(keylengthinbytes) 
                # 2: decrypt:  keyvalue = PBKDF2(self.user_entry_password.get(), binascii.unhexlify(salt_text) ,64000).read(keylengthinbytes)

                # Below, we will create randomSaltBytes of hex-chars, and these will 
                # be 'unhexlified' in the call to PBKDF2. 
                # It has been checked that using 73616c74 produces the result for 'salt' with 4096 iterations. 
                # getrandombytes returns hex, at 4 bits per character. So, to get one byte we need two hex chars.
                saltlengthinbytes=saltlengthinbits/8
                randomSaltBytes=self.getrandombytes( saltlengthinbytes )
                
                # CAREFUL: if Salt field is not enabled, this insert will not work!
                saltwasenabled=0
                if (self.CheckBoxValueEnableSaltEntry.get()==1):
                   saltwasenabled=1
                self.user_entry_salt.config(state=NORMAL)   
                self.user_entry_salt.insert(0,randomSaltBytes)
                if (saltwasenabled==0):
                   # Set Salt back to DISABLED!
                   self.user_entry_salt.config(state=DISABLED)
       salttext=self.user_entry_salt.get()      

       # KEY         
       # This uses DLitz's PBKDF2 implementation.
       # Check the desired Key Length is greater than 0, and divisible by 8.
       # This means we can ask for a key having an integer number of bytes.
       if self.CheckBoxValueEnableKeyOverride.get()==0:    
          if keylengthinbits > 0:             
             if (keylengthinbits % 8 ) !=0:
                tkMessageBox.showwarning("Encrypt Not Possible", "Key Length required (in bits, %s) is not divisible by 8" % keylengthinbits )
                return 6
             else:
                # Check passwordtext and salttext have some content..
                # We are about to use them to generate a key.
                if passwordtext=="" or salttext=="":
                   tkMessageBox.showwarning("Encrypt Not Possible", "Either 'Password' or 'Salt' are empty!" )
                   return 7
                keylengthinbytes=keylengthinbits/8

                # The "iterations" are user-alterable. The user's CPU might not be great.
                # Note: salttext is a string of hex doublets. The PBKDF2 requires salt to be a string or unicode, so we unhexlify(salttext) to pass it. 
                keyvalue = PBKDF2(passwordtext, binascii.unhexlify(salttext) ,int(self.user_entry_pbkdf2_iter.get()), SHA256).read(keylengthinbytes)
                keyHex=binascii.hexlify(keyvalue)
                                
                # CAREFUL: if Key field is not enabled, this insert will not work!
                keywasenabled=0
                if (self.CheckBoxValueEnableKeyEntry.get()==1):
                   keywasenabled=1
                self.user_entry_key.config(state=NORMAL)   
                self.user_entry_key.insert(0,keyHex)
                if (keywasenabled==0):
                   # Set Key back to DISABLED!
                   self.user_entry_key.config(state=DISABLED)
                
       # IV  
       # Check the desired IV Length is greater than 0 (otherwise, do nothing) and
       # also check that the desired IV length is divisible by 8 to get an integer number of bytes.
       if self.CheckBoxValueEnableIvOverride.get()==0:    
          if ivlengthinbits > 0:
             if  (ivlengthinbits % 8 ) !=0 :
                tkMessageBox.showwarning("Encrypt Not Possible", "IV Length required (in bits, %s) is not divisible by 8" % ivlengthinbits )
                return 8
             else:             
                ivlengthinbytes=ivlengthinbits/8
                randomIVBytes=self.getrandombytes( ivlengthinbytes )

                # CAREFUL: if IV field is not enabled, this insert will not work!
                ivwasenabled=0
                if (self.CheckBoxValueEnableIvEntry.get()==1):
                   ivwasenabled=1
                self.user_entry_iv.config(state=NORMAL)   
                self.user_entry_iv.insert(0,randomIVBytes)
                if (ivwasenabled==0):
                   # Set IV back to DISABLED!
                   self.user_entry_iv.config(state=DISABLED)

       # We previously checked Key, IV, Salt were empty OR Overriden. Either way, now they should be filled, if all went well..       
       # We check these three anyway after we return from the GenerateSaltKeyIv Function, so if we got this far, return "Success".
       return "Success"
       

   #####################################################
   # Do the encryption on a validated, 
   # padded clear text with the key in key_text
   # and the needed info on IVSize, IV, BlockSize. 
   #####################################################
   def EncryptValidatedClearText(self,TextForEncryption, EncryptionKey, EncryptionMethodIVSize, IV, EncryptionBlockSize, EncryptionMethodSaltSize, SaltValue):
       key_text_hexed=int(EncryptionKey,16) 
       AESct = AES(key_text_hexed)
       ClearTextContentForChopping=TextForEncryption
       if EncryptionMethodSaltSize>0:
          # INSERT the Salt in the beginning of the EncryptedText; it will be used in Decryption and does *not* need to be kept secret.
          self.EncryptedText.insert(END,SaltValue)
       TempIV=0
       if EncryptionMethodIVSize>0:
          TempIv=int(IV,16)
          # INSERT the IV in the EncryptedText; it will be used in Decryption and does *not* need to be kept secret.
          self.EncryptedText.insert(END,IV)
       while ClearTextContentForChopping:
          textblock=ClearTextContentForChopping[:EncryptionBlockSize/4]
          ClearTextContentForChopping=ClearTextContentForChopping[EncryptionBlockSize/4:]             
          plaintext_hexed=int(textblock,16)
          if EncryptionMethodIVSize>0:
             plaintext_hexed=plaintext_hexed ^ TempIv                             
          encrypted = AESct.encrypt(plaintext_hexed)
          stripped_encrypted="%x" % encrypted

          # add in leading zeroes, if they were removed:
          # e.g. try bbc0bce12a459991e134741a7f9e1989 encrypted with key 2b7e151628aed2a6abf7158809cf4f3c 
          #                                        gives only 31 digits:  26d3c15298e0f6037ffb64355387078
          #                                                   should be: 026d3c15298e0f6037ffb64355387078
          stripped_encrypted_filled=stripped_encrypted.zfill(EncryptionBlockSize/4)             

          if EncryptionMethodIVSize>0:
             TempIv=encrypted
          self.EncryptedText.insert(END,stripped_encrypted_filled)
   

   #####################################################
   # VALIDATE DECRYPT section
   #####################################################
   def ValidateDecryptText(self):
       # Function MUST NOT do anything IF "Eyes" or "Donate" buttons checked.
       if self.CheckBoxValueDisplayDonate.get()==1:
          tkMessageBox.showwarning("'Donate' Checkbox is Active", "'Donate' Checkbox must be deactivated to decrypt" )
          return 1
       if self.CheckBoxValueDisplayEyes.get()==1:
          tkMessageBox.showwarning("'Eyes' Checkbox is Active", "'Eyes' Checkbox must be deactivated to decrypt" )
          return 2

       # Function MUST NOT do anything IF "ClearText" has data.
       # Unfortunately, the get() adds a newline to the text widget contents.
       # So, we must strip the trailing newline
       ClearTextContent=self.ClearText.get("1.0",END)
       if ClearTextContent[-1:] == '\n':
          ClearTextContent = ClearTextContent[:-1]
       if ClearTextContent!="":
          tkMessageBox.showwarning("Decrypt Not Possible", "Clear Text area must be empty to decrypt" )
          return 3

       # For AES, whether in HEX mode or not, we expect EncryptedText to be in hex.
       # So, first we "clean up" the Encrypted Text.
       # --quite often the cut/paste will have SPACEs or ENTER characters which need to be removed. 
       cleanValidate=self.HexCleanup(self.EncryptedText)
       if cleanValidate!="":
          tkMessageBox.showwarning("Cleanup Encrypted Text", "PyEyeCrypt has modified the 'Encrypted Text' content: \n\n %s" % cleanValidate)


       # Function MUST NOT do anything IF "EncryptedText" is empty.
       # Unfortunately, the get() adds a newline to the text widget contents.
       # So, we must strip the trailing newline
       EncryptedTextContent=self.EncryptedText.get("1.0",END)
       if EncryptedTextContent[-1:] == '\n':
          EncryptedTextContent = EncryptedTextContent[:-1]
       if EncryptedTextContent=="":
          tkMessageBox.showwarning("Decrypt Not Possible", "Encrypted Text area is empty." )
          return 4

       # CHECK the PBKDF2 Iterations is a positive integer (allowed=01234567890) and NOT EMPTY
       # Do this whether 'ENABLE' is set or not (user could have disabled after changing it).
       PBKDF2iterations=self.user_entry_pbkdf2_iter.get()
       if PBKDF2iterations == "":
          #Trip an ERROR
          tkMessageBox.showwarning("Decrypt Not Possible", "PBKDF2 iterations is empty. \n\nIt must be a positive integer to generate a Key, preferably in the tens of thousands, larger being more secure.")
          return 5
       posintallowed="0123456789"
       for numericposintchar in PBKDF2iterations:
          if numericposintchar not in posintallowed:
             #Trip the ERROR
             tkMessageBox.showwarning("Decrypt Not Possible", "PBKDF2 iterations must be a positive integer." )
             return 6
       if int(PBKDF2iterations) == 0:
          #Trip an ERROR
          tkMessageBox.showwarning("Decrypt Not Possible", "PBKDF2 iterations is zero. \n\nIt must be a positive integer to generate a Key, preferably in the tens of thousands, larger being more secure.")
          return 7

       # Blocksize, Keysize, ivsize, saltsize hold the number of bits for each of these variables.
       # Set initial values for blocksize, keysize, ivsize, saltsize to -1. 
       # --(A nonsense value designed to protect us in the case that somehow we go to encryption without setting the proper values.)
       # Then set values based on type of encryption selected.
       blocksize=-1
       keysize=-1
       ivsize=-1
       saltsize=-1
       if self.ChosenEncryptMethod.get()=="AES-128 CBC":
          blocksize=128
          keysize=128
          ivsize=128
          saltsize=128
       if self.ChosenEncryptMethod.get()=="AES-128 ECB":
          blocksize=128
          keysize=128
          ivsize=0
          saltsize=128

       # Catch when the Password is empty. Users might do this accidentally
       # BUT there is a vald reason NOT to have a password: 
       # - if you are testing a KAT vector and decrypting with a known Key, which you are 'Keep'ing.
       if self.user_entry_password.get()=="":
          if self.CheckBoxValueEnableKeyOverride.get()==0:
             tkMessageBox.showwarning("Decrypt Not Possible", "'Password' is empty." )
             return 8

       #For Decrypt only,  see if the user-entered Salt is EMPTY. It should be empty for DECRYPTION to begin with. 
       #Differs relative to Encrypt! (There, salt_text is checked against salt_size and demanded if needed.)
       salt_text=self.user_entry_salt.get()
       if len(salt_text) != 0:
          # CAREFUL: if Salt field is not enabled, this insert will not work!
          saltwasenableda=0
          if (self.CheckBoxValueEnableSaltEntry.get()==1):
             saltwasenableda=1
          self.user_entry_salt.config(state=NORMAL)   
          self.user_entry_salt.delete(0,END)
          if (saltwasenableda==0):
             # Set Salt back to DISABLED!
             self.user_entry_salt.config(state=DISABLED)

       #For Decrypt only,  see if the user-entered IV is EMPTY. It should be empty for DECRYPTION to begin with. 
       #Differs relative to Encrypt! (There, iv_text is checked against iv_size and demanded="" for ECB mode)
       iv_text=self.user_entry_iv.get()
       if len(iv_text) != 0:
          # CAREFUL: if IV field is not enabled, this insert will not work!
          ivwasenableda=0
          if (self.CheckBoxValueEnableIvEntry.get()==1):
             ivwasenableda=1
          self.user_entry_iv.config(state=NORMAL)   
          self.user_entry_iv.delete(0,END)
          if (ivwasenableda==0):
             # Set IV back to DISABLED!
             self.user_entry_iv.config(state=DISABLED)

       #See if the 'Key' field is empty  -- this simply stops the code filling in the salt and IV in the next two steps, when it's going to stop anyway due to the 'Key'
       #This differs from IV and Salt above in that we sometimes use the 'Keep' function in decryption, instead of obtaining Salt/IV from the message itself (we don't need 'Keep').
       if self.user_entry_key.get()!="":  
          if self.CheckBoxValueEnableKeyOverride.get()==1:
             self.EnableKeyOverride()
          else:
             # CAREFUL: if Key field is not enabled, this insert will not work!
             keywasenableda=0
             if (self.CheckBoxValueEnableKeyEntry.get()==1):
                keywasenableda=1
             self.user_entry_key.config(state=NORMAL)   
             self.user_entry_key.delete(0,END)
             if (keywasenableda==0):
                # Set Key back to DISABLED!
                self.user_entry_key.config(state=DISABLED)
       


       # For AES, whether in HEX mode or not, we expect EncryptedText to be in hex.
       # So, now re-check the "allowed" characters in [0..9, a..f, A..F] for Key, Salt, IV, ClearText, Encrypted Text.
       # These were checked if we entered HEX mode, but could since have changed.
       # NOTE this means it's obvious that you DONT put 0x in front of hex strings, because you cannot enter the x.
       validate=""
       validate=self.HexCheck()
       #open a new window to explain the error; in hex mode we can ONLY use 0-9&a/A,b/B,c/C,d/D,e/E,f/F       
       if validate!="":     
          tkMessageBox.showwarning("Invalid Characters", "%s has invalid characters. \n\nOnly characters \n[0..9, a..f, A..F] are allowed.\n\n--NO SPACES, or CR/LF's!--" % validate )
          return 9


       #The first "saltsize" bits will be the Salt for the Key of the Encrypted Message. 
       if saltsize > 0:
          if  (len(EncryptedTextContent)*4) > saltsize:
             salt_text=EncryptedTextContent[:saltsize/4]
             EncryptedTextContent=EncryptedTextContent[saltsize/4:]

             # Now we've got it, put the Salt into the field on the gui..
             # CAREFUL: if Salt field is not enabled, this insert will not work!
             saltwasenabled=0
             if (self.CheckBoxValueEnableSaltEntry.get()==1):
                saltwasenabled=1
             self.user_entry_salt.config(state=NORMAL)   
             self.user_entry_salt.insert(0,salt_text)
             if (saltwasenabled==0):
                # Set Salt back to DISABLED!
                self.user_entry_salt.config(state=DISABLED)
          else:
             tkMessageBox.showwarning("Decrypt ERROR", "Error: Cannot Decrypt when Encrypted Text is not long enough to even contain the 'Salt' ('Salt'=%s bytes)." % saltsize )
             return 10

       #The next "ivsize" bits will be the IV of an encrypted message. 
       if ivsize > 0:
          if  (len(EncryptedTextContent)*4) > ivsize:
             iv_text=EncryptedTextContent[:ivsize/4]
             EncryptedTextContent=EncryptedTextContent[ivsize/4:]
             
             # Now we've got it, put the IV into the field on the gui..
             # CAREFUL: if IV field is not enabled, this insert will not work!
             ivwasenabled=0
             if (self.CheckBoxValueEnableIvEntry.get()==1):
                ivwasenabled=1
             self.user_entry_iv.config(state=NORMAL)   
             self.user_entry_iv.insert(0,iv_text)
             if (ivwasenabled==0):
                # Set IV back to DISABLED!
                self.user_entry_iv.config(state=DISABLED)
          else:
             tkMessageBox.showwarning("Decrypt ERROR", "Error: Cannot Decrypt when Encrypted Text is not long enough to even contain the 'IV' ('IV'=%s bytes)." %ivsize )
             return 11

       # NOTE Decryption IS different to Encryption; inasmuch as HEX mode indicates whether we want HEX Cleartext output; 
       #      the encrypted text SHOULD always be in HEX to begin with!
       # NOTE This means the validation has to be different too! 
       #      - EncryptedText must ALWAYS be in hex
       #      - IV (if required for CBC etc.) is extracted from EncryptedText, not user-entered.

       # We know from the checks three stages prior that the Key is empty, 
       # but to generate the Key we need password and Salt... 
       if self.user_entry_key.get()=="":  
          # Regenerate the Key from Password and Salt..
          # We always know keysize will be divisible by 8. We're not thaat stupid!
          keylengthinbytes=keysize/8

          # The "iterations" are user-alterable. The user's CPU might not be great.
          # Note: salttext is a string of hex doublets. The PBKDF2 requires salt to be a string or unicode, so we unhexlify(salttext) to pass it. 
          keyvalue = PBKDF2(self.user_entry_password.get(), binascii.unhexlify(salt_text) ,int(self.user_entry_pbkdf2_iter.get()), SHA256).read(keylengthinbytes)
          keyHex=binascii.hexlify(keyvalue)
          if keysize > 0:
             # Now we've got it, put the Key into the field on the gui..
             # CAREFUL: if Key field is not enabled, this insert will not work!
             keywasenabled=0
             if (self.CheckBoxValueEnableKeyEntry.get()==1):
                keywasenabled=1
             self.user_entry_key.config(state=NORMAL)   
             self.user_entry_key.insert(0,keyHex)
             if (keywasenabled==0):
                # Set Key back to DISABLED!
                self.user_entry_key.config(state=DISABLED)

       # Check that the Key is now indeed present (we must to this again, to check the above Key generation worked properly)
       if self.user_entry_key.get()=="":  
          tkMessageBox.showwarning("Decrypt Not Possible", "'Key' is empty." )
          return 12          

       # See if the Key is the right length -take each HEX digit as 4 bytes, so multiply by 4.
       key_text=self.user_entry_key.get()
       if (len(key_text)*4) != keysize:
          tkMessageBox.showwarning("Decrypt Not Possible", "'Key' length is wrong number of bits. Should be %s bits." % keysize  )
          return 13
             
       # For AES, whether in HEX mode or not, we expect EncryptedText to be in hex.
       # I require text to be a muliple of the blocksize (usually 128 bits).
       trailingpadding=""
       if ((len(EncryptedTextContent)*4) % blocksize ) !=0:
          tkMessageBox.showwarning("Padding Encryptedtext", "Warning: Encrypted text is being padded. Are you running the correct decryption algo?" )
          trailingpadding=self.PadTo128Bits( len(EncryptedTextContent)*4, blocksize )
          #Error Trapping - should only consist of hex digits so we will never falsely detect an error if we look for "PaddingError"!
          if (trailingpadding=="PaddingError"):
             tkMessageBox.showwarning("Padding Encryptedtext", "Error in PadTo128Bits() Function. Padding FAILED." )
             return 14 
       PaddedEncryptedTextContent=EncryptedTextContent+trailingpadding

       #Do the decryption
       self.DecryptValidatedEncryptedText(PaddedEncryptedTextContent, key_text, ivsize, iv_text, blocksize)          

          
   #####################################################
   # Do the decryption on a validated, 
   # padded encrypted text with the key in key_text
   # and the needed info on IVSize, IV, BlockSize. 
   # NOTE - this is diferent to encrypt!
   #      - the XOR'ing / calculation of TempIv has to differ from encryption.
   #      - the initial IV passed into this function is extracted from 'Encrypted Text', not user-entered.
   #####################################################
   def DecryptValidatedEncryptedText(self,TextForDecryption, EncryptionKey, EncryptionMethodIVSize, IV, EncryptionBlockSize):
       key_text_hexed=int(EncryptionKey,16)
       AESct = AES(key_text_hexed)
       EncryptedTextContentForChopping=TextForDecryption
       TempIV=0
       total_stripped_decrypted_filled=""

       if EncryptionMethodIVSize>0:
          TempIv=int(IV,16)
       while EncryptedTextContentForChopping:
          textblock=EncryptedTextContentForChopping[:EncryptionBlockSize/4]
          EncryptedTextContentForChopping=EncryptedTextContentForChopping[EncryptionBlockSize/4:]             
          encryptedtext_hexed=int(textblock,16)
          decrypted = AESct.decrypt(encryptedtext_hexed)
          if EncryptionMethodIVSize>0:
             decrypted=decrypted ^ TempIv
          stripped_decrypted="%x" % decrypted

          # add in leading zeroes, if they were removed:
          # e.g. try 0001bee22e409f96e93d7e117393172a encrypted with key 2b7e151628aed2a6abf7158809cf4f3c 
          #                                            gives enc digits: 1aa46f57d57b606c828c9519b18150c3
          #                  "stripped_decrypted"       and decrypts to: 1bee22e409f96e93d7e117393172a
          #                  "stripped_decrypted_filled"      should be: 0001bee22e409f96e93d7e117393172a
          stripped_decrypted_filled=stripped_decrypted.zfill(EncryptionBlockSize/4)   

          if EncryptionMethodIVSize>0:
             TempIv=int(textblock,16)

          # Append the "stripped_decrypted_filled" into "total_stripped_decrypted_filled" 
          total_stripped_decrypted_filled=total_stripped_decrypted_filled+stripped_decrypted_filled

       if self.CheckBoxValueClickKeyMode.get()==1:
          self.ClearText.config(state=NORMAL)
       if self.CheckBoxValueHexMode.get()==1:
          self.ClearText.insert(END,total_stripped_decrypted_filled)
       else:
          # Unhexlify and sanitise the stripped_decrypted_filled block; it CAN have padded junk which does not correspond to ascii chars. 
          unhexlified_stripped_decrypted_filled=binascii.unhexlify(total_stripped_decrypted_filled).decode('utf8','replace')
          self.ClearText.insert(END,unhexlified_stripped_decrypted_filled)
       if self.CheckBoxValueClickKeyMode.get()==1:
          self.ClearText.config(state=DISABLED)
   

   #####################################################
   # Function to hide/display content with "eyes"
   #####################################################
   def DisplayEyes(self):
       # Use the 'global' copies of these six variables, otherwise Python will try to make local copies all on its own!
       # We need global-level memory of the user-defined window dimensions and Text content of the windows
       # to cope with users selecting the 'Eyes' or 'Donate' checkboxes.   
       global user_defined_frame_width
       global user_defined_frame_height
       global user_defined_font_size
       global user_entered_ClearText
       global user_entered_EncryptedText
       global loopcount 

       # Update the Frame to get current height/width. 
       # These values start =1 and we MUST have the correct values here.
       self.update()

       # Before we clean up, and if we are setting the check-button, get copies of the user-entered text
       # (--except-- if this is the first time we do this at app initialisation!)
       if loopcount!=0:
          if (user_entered_ClearText=="") and (self.CheckBoxValueDisplayEyes.get()==1):
             user_entered_ClearText=self.ClearText.get("1.0",END)
          if (user_entered_EncryptedText=="") and (self.CheckBoxValueDisplayEyes.get()==1):
             user_entered_EncryptedText=self.EncryptedText.get("1.0",END)

       # Now, Clean up in preparation.
       self.CleanStart()

       # Make sure we never miss the user-entered text copying process above after initialisation. 
       loopcount=1      

       # We take the _temp (=current) value of width and height.
       # If the frame is still the default size, we will do nothing.
       # If the user has changed the frame size, we store the user-defined values for later.
       user_defined_frame_width_temp=IntVar()
       user_defined_frame_height_temp=IntVar()
       user_defined_frame_width_temp=self.winfo_width()
       user_defined_frame_height_temp=self.winfo_height()   

       if frame_width!=user_defined_frame_width_temp:
          user_defined_frame_width=user_defined_frame_width_temp
       if frame_height!=user_defined_frame_height_temp:
          user_defined_frame_height=user_defined_frame_height_temp

       # Now deal with the font size in ClearText/EncryptedText/Password widgets.
       # NB:- the (user defined) font size should the the same in all these windows
       # We take the _temp (=current) value of font size.
       # If the font is still the default size, we will do nothing.
       # If the user has changed the font size, we store the user-defined values for later.
       user_defined_font_size_temp=IntVar()
       fontinfoClearText = tkFont.Font(font=self.ClearText['font'])
       user_defined_font_size_temp=fontinfoClearText.actual('size')       
       if user_defined_font_size_temp!=bestfontsize:
          user_defined_font_size=user_defined_font_size_temp

       # Set the geeometry to the default size, so the eyes are displayed properly.
       root.wm_geometry("%dx%d" % (frame_width, frame_height))
       
       # Set the font size to the value which displays the eyes/QR code best.
       self.ClearText.config(font=( "Courier", bestfontsize, 'bold' ))
       self.EncryptedText.config(font=( "Courier", bestfontsize, 'bold' ))
       self.user_entry_password.config(font=( "arial", root.bestpasswordfontsize ))

       # If the other button (DisplayDonate) is ON, set it to off now;
       # This will ensure we don't have both ticked; it's 'almost' radiobutton behaviour, but not quite.
       if self.CheckBoxValueDisplayDonate.get()==1:
          self.DisplayDonateButton.deselect() 

       # When switching to "Eyes", If the "Reveal" checkboxes are ticked, untick them now.
       # And hide the pass/key
       if self.CheckBoxValueDisplayEyes.get()==1:
          if self.CheckBoxValueDisplayPassword.get()==1:
             self.DisplayPasswordButton.deselect()
             self.ShowHidePass()
          if self.CheckBoxValueDisplayKey.get()==1:
             self.DisplayKeyButton.deselect()
             self.ShowHideKey()

       # ASCII art adapted from http://ascii.co.uk/art/eye, part of "crying eye", artist unknown.
       EyeTextL=("\n"
                 "\n"
                 "\n"
                 "\n"
                 "\n"
                 "\n"
                 "\n"
                 "\n"
                 "\n"
                 "                        ,,........,,                 \n"
                 "                  .,;'';,.,;;;;;,,,.''';,            \n"
                 "                .,;'';;,..,;;;,,,,,..'';;,..         \n"
                 "              ,;'''                   ';;;;,;        \n"
                 "             ,;''                       ';;,;'       \n"
                 "            ;'    ,;;@;;',@@;, @@,'';;;;,  ,;';.     \n"
                 "           ;'    ,;@@@;',@@@;, @@, ';;;@@@;,;;.      \n"
                 "           ''  ,;;@@@;' ;@@@@; ''   ';;;@@@@@;;;.    \n"
                 "           ''  ,;@@@@'  ;@@@@; ''    ;;;@@@@@@;;;    \n"
                 "           '  ;;@@@@@   ''@@;       ,;;;@@@@@@@;;.   \n"
                 "              ;;@@@@@'   '''       .,;;;@@@@@@@;;;   \n"
                 "             ;;@@@@@@@'           ',,;;;@@@@@@@;;;.  \n"
                 "             ;;@@@@@@@,.         ' ,';;;@@@@@@@;;;.  \n"
                 "              ';@@@@@@@;;,.     '. ',;;@@@@@@@;;;;;  \n"
                 "              '';@@@@@@;;;,..  .,,',;;@@@@@@@;;;;;;  \n"
                 "                 . '';;;;;;;;;;;,;;;;@@@@@@;' ,.:;'  \n"
                 "                   .  ''''''''''''''          .:;'   \n"
                 "                   ''..,,     ''''     '   .,;'      \n"
                 "                        ''''''::''''''''             \n"
                 "                            ''':''''''               \n"
                 "\n")

       # NB: this is NOT just the reverse image of EyeTextL!
       EyeTextR=("\n"
                 "\n"
                 "\n"
                 "\n"
                 "\n"
                 "\n"
                 "\n"
                 "\n"
                 "\n"
                 "                           ,,........,,              \n"
                 "                      ,;'''.,,,;;;;;,.,;'';,.        \n"
                 "                   ..,;;''..,,,,,;;;,..,;;'';,.      \n"
                 "                  ;,;;;;''                  ''';,    \n"
                 "                 ';,;;'                       '';,   \n"
                 "               .;';,  ,;;;',@@;, @@, ';;;@;;,    ';  \n"
                 "               .;;,;@@@;;',@@@;, @@, ';;;@@@;,    '; \n"
                 "              .;;;@@@@@;' ;@@@@; ''    ;;;@@@;;,  '' \n"
                 "              ;;;@@@@@@'  ;@@@@; ''    ;;;@@@@;,  '' \n"
                 "             .;;@@@@@@@   ''@@;     .,,;;;@@@@@;;  ' \n"
                 "             ;;;@@@@@@@'   '''      .,,;;;@@@@@;;    \n"
                 "            .;;;@@@@@@@;           , ';;;@@@@@@@;;   \n"
                 "            .;;;@@@@@@@;           , ';;;@@@@@@@;;   \n"
                 "            ;;;;;@@@@@@@;;,.     ,  ',;;@@@@@@@;'    \n"
                 "            ;;;;;;@@@@@@@;;,.     , ',;;@@@@@@;''    \n"
                 "            ';:., ';@@@@@@;;;;,;;;;;;;;;;;'' .       \n"
                 "             ';:.          ''''''''''''''  .         \n"
                 "                ';,.   '     ''''     ,,..''         \n"
                 "                       ''''''''::''''''              \n"
                 "                         '''''':'''                  \n"
                 "\n"
                 )

       # If the DisplayEyes box is checked, insert the images
       if self.CheckBoxValueDisplayEyes.get()==1:
          if self.CheckBoxValueClickKeyMode.get()==1:
             self.ClearText.config(state=NORMAL)
          self.ClearText.insert(END,EyeTextL)
          if self.CheckBoxValueClickKeyMode.get()==1:
             self.ClearText.config(state=DISABLED)
          self.EncryptedText.insert(END,EyeTextR)
       # Otherwise, we might be here because the box was actively unchecked, and we must set the geometry
       # back to how it was before the box/boxes were checked.
       else:
          #  box is unchecked.. In case the user had a different geometry before checking the box...
          #  we re-instate that geometry.
          if (user_defined_frame_width!=frame_width) or (user_defined_frame_height!=frame_height):
             root.wm_geometry("%dx%d" % (user_defined_frame_width, user_defined_frame_height))
          #  and re-instate the font size selected by the user..
          if (user_defined_font_size!=bestfontsize):
             self.ClearText.config(font=( "Courier", user_defined_font_size, 'bold' ))
             self.EncryptedText.config(font=( "Courier", user_defined_font_size, 'bold' ))
             self.user_entry_password.config(font=( "arial", user_defined_font_size ))
             


       # After we cleaned up the Text, and restored the geometry..
       # IF we are UNchecking the box... and there is any user-entered text content....
       # restore the user-entered text... 
       # and then clean the buffer, again, only if there is any content. 
       if (self.CheckBoxValueDisplayEyes.get()==0):
          if (user_entered_ClearText!=""):
             # Remove any trailing "\n" newline, because the copy action we performed actually adds a newline!
             if user_entered_ClearText[-1:] == '\n':
                user_entered_ClearText = user_entered_ClearText[:-1]
             if self.CheckBoxValueClickKeyMode.get()==1:
                self.ClearText.config(state=NORMAL)
             self.ClearText.insert(END,user_entered_ClearText)
             if self.CheckBoxValueClickKeyMode.get()==1:
                self.ClearText.config(state=DISABLED)
             user_entered_ClearText=""
          if (user_entered_EncryptedText!=""):
             # Remove any trailing "\n" newline, because the copy action we performed actually adds a newline!
             if user_entered_EncryptedText[-1:] == '\n':
                user_entered_EncryptedText = user_entered_EncryptedText[:-1]
             self.EncryptedText.insert(END,user_entered_EncryptedText)
             user_entered_EncryptedText="" 

       
   #####################################################
   # Function to hide/display content with "Donate QR"
   #####################################################
   def DisplayDonate(self):
       # Use the 'global' copies of these five variables, otherwise Python will try to make local copies all on its own!
       # We need global-level memory of the user-defined window dimensions and Text content of the windows
       # to cope with users selecting the 'Eyes' or 'Donate' checkboxes.   
       global user_defined_frame_width
       global user_defined_frame_height
       global user_defined_font_size
       global user_entered_ClearText
       global user_entered_EncryptedText

       # Update the Frame to get current height/width. 
       # These values start =1 and we MUST have the correct values here.
       self.update()

       # Before we clean up, and if we are setting the check-button, get copies of the user-entered text
       if (user_entered_ClearText=="") and (self.CheckBoxValueDisplayDonate.get()==1):
          user_entered_ClearText=self.ClearText.get("1.0",END)
       if (user_entered_EncryptedText=="") and (self.CheckBoxValueDisplayDonate.get()==1):
          user_entered_EncryptedText=self.EncryptedText.get("1.0",END)

       # Now, Clean up in preparation.
       self.CleanStart()

       # We take the _temp (=current) value of width and height.
       # If the frame is still the default size, we will do nothing.
       # If the user has changed the frame size, we store the user-defined values for later.
       user_defined_frame_width_temp=IntVar()
       user_defined_frame_height_temp=IntVar()
       user_defined_frame_width_temp=self.winfo_width()
       user_defined_frame_height_temp=self.winfo_height()   
       if frame_width!=user_defined_frame_width_temp:
          user_defined_frame_width=user_defined_frame_width_temp
          #self.EncryptedText.insert(END,"WIDTH DIFFERENT, set user_defined_frame_width=CURRENT\n")
          #self.EncryptedText.insert(END,user_defined_frame_width)
          #self.EncryptedText.insert(END,"\n")
       if frame_height!=user_defined_frame_height_temp:
          user_defined_frame_height=user_defined_frame_height_temp
          #self.EncryptedText.insert(END,"HEIGHT DIFFERENT, set user_defined_frame_height=CURRENT\n")
          #self.EncryptedText.insert(END,user_defined_frame_height)
          #self.EncryptedText.insert(END,"\n")

       # Now deal with the font size in ClearText/EncryptedText widgets.
       # NB:- the (user defined) font size should the the same in both these windows
       # We take the _temp (=current) value of font size.
       # If the font is still the default size, we will do nothing.
       # If the user has changed the font size, we store the user-defined values for later.
       user_defined_font_size_temp=IntVar()
       fontinfoClearText = tkFont.Font(font=self.ClearText['font'])
       user_defined_font_size_temp=fontinfoClearText.actual('size')       
       if user_defined_font_size_temp!=bestfontsize:
          user_defined_font_size=user_defined_font_size_temp



       # Set the geeometry to the default size, so the QR is displayed properly.
       root.wm_geometry("%dx%d" % (frame_width, frame_height))

       # Set the font size to the value which displays the eyes/QR code best.
       self.ClearText.config(font=( "Courier", bestfontsize, 'bold' ))
       self.EncryptedText.config(font=( "Courier", bestfontsize, 'bold' ))
       self.user_entry_password.config(font=( "arial", root.bestpasswordfontsize ))

       
       # If the other button (DisplayEyes) is ON, set it to off now;
       # This will ensure we don't have both ticked; it's 'almost' radiobutton behaviour, but not quite.
       if self.CheckBoxValueDisplayEyes.get()==1:
          self.DisplayEyesButton.deselect() 

       # If the "Reveal" checkboxes are ticked, untick them now.
       # And hide the pass/key
       if self.CheckBoxValueDisplayDonate.get()==1:
          if self.CheckBoxValueDisplayPassword.get()==1:
             self.DisplayPasswordButton.deselect()
             self.ShowHidePass()
          if self.CheckBoxValueDisplayKey.get()==1:
             self.DisplayKeyButton.deselect()
             self.ShowHideKey()

       # Define the image. 
       DonateTextL=("██████████████████████████████████████████████████████████████\n"
                    "██              ██  ██  ██    ██  ██████    ██              ██\n"
                    "██  ██████████  ████          ██████████    ██  ██████████  ██\n"
                    "██  ██      ██  ██      ██████████  ██  ██  ██  ██      ██  ██\n"
                    "██  ██      ██  ██      ██  ██    ████████████  ██      ██  ██\n"
                    "██  ██      ██  ██  ████    ██    ██      ████  ██      ██  ██\n"
                    "██  ██████████  ██████    ██  ██████  ██    ██  ██████████  ██\n"
                    "██              ██  ██  ██  ██  ██  ██  ██  ██              ██\n"
                    "██████████████████████  ██  ████  ██      ████████████████████\n"
                    "██        ████  ██  ██        ██████  ██      ████      ██  ██\n"
                    "██  ██  ████  ████  ██  ██      ██  ████  ██  ██      ████  ██\n"
                    "██  ██    ████  ██            ████            ██  ████  ██████\n"
                    "██    ████  ████████    ████████  ██  ████  ████  ██  ██  ████\n"
                    "████    ██  ██    ██    ██  ██    ████████          ██    ████\n"
                    "██        ██████  ██████    ██    ██  ██  ██████████      ████\n"
                    "██  ██████  ██      ██    ██  ████  ██            ████████  ██\n"
                    "██    ██    ████    ██    ████  ██  ████      ██      ████  ██\n"
                    "██    ████████  ██  ██████  ██  ██████  ██  ██████    ████████\n"
                    "████    ████  ██  ████████████    ████  ████      ██  ████████\n"
                    "██  ████  ██      ██████████          ██  ██████          ████\n"
                    "██████      ████  ████    ██      ██████  ██████████    ██  ██\n"
                    "████        ██        ██████    ██    ██            ██████  ██\n"
                    "██████████████████      ████████    ████    ██████  ████  ████\n"
                    "██              ████  ████████  ██  ██████  ██  ██    ██  ████\n"
                    "██  ██████████  ████                    ██  ██████  ██████████\n"
                    "██  ██      ██  ██████    ██████    ██  ██          ████    ██\n"
                    "██  ██      ██  ██  ████  ██  ██████  ██  ████  ██        ████\n"
                    "██  ██      ██  ██  ██  ██  ██  ██████  ████████  ████████  ██\n"
                    "██  ██████████  ██  ██  ██    ██    ████  ████████████████  ██\n"
                    "██              ██  ████  ██████████          ██████  ██  ████\n"
                    "██████████████████████████████████████████████████████████████\n"
                    "  BTC donate to:    13BW54SgWUDhAJUujwkvo53LWk8TQ46bw2        \n"
                    "  -Thanks for **any** contribution, enjoy encrypting!-        \n")

       DonateTextR=("\n" 
                    "\n" 
                    "\n" 
                    "\n" 
                    "\n" 
                    "\n" 
                    "\n" 
                    "\n" 
                    "\n" 
                    "\n" 
                    "\n" 
                    "\n" 
                    "        <:::<    _____                  ___  ___     _ \n"
                    "      <:::<     /  ___|                 |  \/  |    | |\n"
                    "    <:::<       \ `--.  ___ __ _ _ __   | .  . | ___| |\n"
                    "  <:::::::::::=  `--. \/ __/ _` | '_ \  | |\/| |/ _ \ |\n"
                    "    <:::<       /\__/ / (_| (_| | | | | | |  | |  __/_|\n"
                    "      <:::<     \____/ \___\__,_|_| |_| \_|  |_/\___(_)\n"
                    "        <:::<                                          \n"
                    "\n")

       # If the DisplayDonate box is checked, insert the image.
       if self.CheckBoxValueDisplayDonate.get()==1:
          if self.CheckBoxValueClickKeyMode.get()==1:
             self.ClearText.config(state=NORMAL)
          self.ClearText.insert(END,DonateTextL)
          if self.CheckBoxValueClickKeyMode.get()==1:
             self.ClearText.config(state=DISABLED)
          self.EncryptedText.insert(END,DonateTextR)
       # Otherwise, we might be here because the box was actively unchecked, and we must set the geometry
       # back to how it was before the box/boxes were checked.
       else:
          #  box is unchecked.. In case the user had a different geometry before checking the box...
          #  we reinstate that geometry.
          if (user_defined_frame_width!=frame_width) or (user_defined_frame_height!=frame_height):
             root.wm_geometry("%dx%d" % (user_defined_frame_width, user_defined_frame_height))
          #  and re-instate the font size selected by the user..
          if (user_defined_font_size!=bestfontsize):
             self.ClearText.config(font=( "Courier", user_defined_font_size, 'bold' ))
             self.EncryptedText.config(font=( "Courier", user_defined_font_size, 'bold' ))
             self.user_entry_password.config(font=( "arial", user_defined_font_size ))



       # After we cleaned up and restored the geometry..
       # IF we are UNchecking the box... and there is any user-entered text content....
       # restore the user-entered text... 
       # and then clean the buffer, again, only if there is any content. 
       if (self.CheckBoxValueDisplayDonate.get()==0):
          if (user_entered_ClearText!=""):      
             # Remove any trailing "\n" newline, because the copy action we performed actually adds a newline!
             if user_entered_ClearText[-1:] == '\n':
                user_entered_ClearText = user_entered_ClearText[:-1]
             if self.CheckBoxValueClickKeyMode.get()==1:
                self.ClearText.config(state=NORMAL)
             self.ClearText.insert(END,user_entered_ClearText)
             if self.CheckBoxValueClickKeyMode.get()==1:
                self.ClearText.config(state=DISABLED)
             user_entered_ClearText=""
          if (user_entered_EncryptedText!=""):
             # Remove any trailing "\n" newline, because the copy action we performed actually adds a newline!
             if user_entered_EncryptedText[-1:] == '\n':
                user_entered_EncryptedText = user_entered_EncryptedText[:-1]
             self.EncryptedText.insert(END,user_entered_EncryptedText)
             user_entered_EncryptedText=""


   #####################################################
   # A Funcion to make the Help window using the "Notebook"
   # class defined later.
   #####################################################
   def HelpWindow(self):
      self.helpwin=Toplevel()
      self.helpwin.title("PyEyeCrypt (%s)   -  Copyright (C) 2015:   Help" %PyEyeCryptVersion)
      note=Notebook(self.helpwin, width= 600, height =550, activefg = 'red', inactivefg = 'blue')
      note.grid()
      tab1 = note.add_tab(text = "Encryption")
      tab2 = note.add_tab(text = "Encrypted Text")
      tab3 = note.add_tab(text = "Salt")
      tab4 = note.add_tab(text = "Key")
      tab5 = note.add_tab(text = "IV")
      tab6 = note.add_tab(text = "Decryption")
      tab7 = note.add_tab(text = "Encryption Methods")
      tab8 = note.add_tab(text = "Tests")
      tab9 = note.add_tab(text = "About")
      Label(tab1, text= 'ENCRYPTION:\n========\n1. Enter your message in the "Clear Text" window.\n2. Enter a Password (make it long and $tr0nG!, but mostly loooong) \n    -- the generated Key will only be as strong as your Password! \n3. Choose the encryption method (recommended "AES-128 CBC"). \n4. Click on the "ENCRYPT" button. \n\nYou may receive a warning that your text is being "padded".\nIf this happens, your message will have some random characters \nappended at the end which will be visible upon decryption. \nIt might be prudent to warn your intended recpient about this. \n\nGeek notes: \nThe padding is necessary because AES is a "block" cipher, \nwhich operates on blocks of text of a specific size. If your \nmessage is not exactly divisible by the block size, then your \ntext is padded with random characters to make it fit the cipher. \nThe random characters are generated by a cryptographically \nsecure method, (not a PRNG!). It is possible (but not necessary) \nto avoid the need for padding by lengthening your message. \n\nYour encrypted text will consist of hexadecimal digits 0-9,a-f.\n\nIMPORTANT:\n========\nThe new Windows 10 Privacy Statement includes the words: \n"Your typed and handwritten words are collected".\n- PyEyeCrypt will therefore enforce the use of "clickable keyboards" \n   for ClearText and Password entry, when it detects an operating \n   system which is known to snoop on users.', justify=LEFT).grid()

      Label(tab2, text ='UNDERSTANDING THE ENCRYPTED TEXT:\n========================= \nAfter encryption, the "Encrypted Text" area will contain your encrypted \nmessage, plus some other data which the receipient will need.  \n\nSpecifically, the "Encrypted Text" area contains, in order: \n1. Password Salt, or simply "Salt", \n2. Message Initialisation Vector, "IV" - Only if using "CBC" mode encryption.\n3. The Encrypted Message. \n\nIf you have just encrypted some cleartext, then the Salt and IV will \nbe present at the beginning of the "Encrypted Text". \n\nVERY IMPORTANT:\n============ \n- The "Password" must be kept secret. \n- The "Key" should be DISCARDED, and NEVER transmitted or divulged. \n         -- it will be recalculated by the recipient using the Password and Salt.', justify=LEFT).grid()

      Label(tab3, text = 'PASSWORD SALT:\n==========\nIf you just encrypted (or decrypted) some text, the Salt will be visible near \nthe bottom of the Main Window. \n\nThe Salt is transmitted to the recipient in first block of the Encrypted Text. \nIt is randomly generated for each message, and is needed by the recipient \nto turn your agreed Password into a "Key". The Salt should NEVER be \nre-used for a message you wish to keep secure. \n\nGeek notes:\n- It is OK to transmit the Salt unencrypted, since it is ONLY used to deter \n   the use of "rainbow" or "lookup" tables on common* passwords. \n- The use of Salt means that a lookup table would have to be computed \n   for each message. \n- Knowing the Salt DOES NOT help the attacker to deduce your Password. \n- Remember, the generated Key will only be as strong as your Password. \n\nSuper Geek Notes:\n- The Password and Salt are combined using the PBKDF2 function with \n   HMAC SHA256 hashing, and 16,384 iterations (by default) to make the Key. \n- *Rainbow tables exist to crack md5 hashes of ALL POSSIBLE passwords up \n   to 8 characters long (e.g. http://www.freerainbowtables.com/en/tables2/), \n   so in order to prevent computation of lookups (given the Salt), it is \n   imperative to use a tunably slow function like PBKDF2 (or equivalent); \n     - with a good hashing function (e.g. SHA-256), \n     - using a substantial number of iterations (tens of thousands), \n     - including a new, long, cryptographically-random Salt, \n     - and using lo0o0o0ooooong passwords.\n- If you are careful to NEVER re-use a Salt, then any attacker has to recompute \n   rainbow/lookup tables for each message!', justify=LEFT).grid()

      Label (tab4, text = 'Key: \n=== \nIf you just encrypted (or decrypted) some text, the Key will be visible near \nthe bottom of the Main Window (click "Reveal" to see it). \n\nThe Key should NEVER transmitted to the recipient, and should be DISCARDED \nafter each encryption (the recipient only needs the Password and Salt to \ndecrypt; the Key is computed from these). \n\nPBKDF2 Function:\n===========\nThe Key is computed using the Password Based Key Derivation Function2 \n(PBKDF2), which is designed to be tunably slow (higher iterations equals \nslower Key derivation): \n- The cryptographically-random Salt deters the use of rainbow/lookup tables. \n- The tunable slowness of PBKDF2 Key generation using higher iterations \n   deters the use of brute-force or dictionary attacks.  \n\nIn this software, PBKDF2 is set up to use HMAC SHA-256 hashing, the random \nSalt, Password, and 16,384 iterations by default. \n\nThe PBKDF2 iterations can be increased if desired, but the recipient must be \nwarned in advance, otherwise they will not compute the Key correctly, even if \nthey have the Password and Salt!',justify=LEFT).grid()

      Label (tab5, text = 'MESSAGE INITIALISATION VECTOR (IV):\n========================\nIf you just encrypted (or decrypted) some text and an IV is needed, it will \nbe visible near the bottom of the Main Window. \n\n- The IV is transmitted to the recipient in the second block of the \n   encrypted text, immediately following the "Salt". \n- It is a random series of hexadecimal digits created for each message. \n- An IV is generated when encrypting in "CBC" (Cipher Block Chain) mode. \n- IVs should NEVER be re-used on messages you wish to keep secure. \n\nGeek notes:\n- When a block is to be encrypted in CBC-mode, it is first XORed with the \n   previous encrypted block. \n- The IV has the role of the "-1" block (the previous encrypted block for \n   the first block). \n- The main consequence of re-using the IV is that if two messages begin \n   with the same sequence of bytes then the encrypted messages may also \n   be identical for a few blocks, depending on the Key. This leaks data and \n   opens the possibility of some attacks. \n\nFor more explanation on the use of "IV"s, see the Wikipedia entry on \nblock-ciphers: \nhttps://en.wikipedia.org/wiki/Block_cipher_mode_of_operation',justify=LEFT).grid()

      Label(tab6, text = 'DECRYPTION:\n==========\nWith your encrypted message consisting of hexadecimal digits 0-9,a-f in \nthe "Encrypted Text" window; \n- Select the appropriate decrpytion method. \n- Enter the "Password". \n- Click the "DECRYPT" button. \n\nNB: Depending on the length of the original un-encrypted message, your \ndeciphered message may have residual extra characters at the end. This \nis a consequence of padding, which is applied when the message was \noriginally encrypted and the length is not a multiple of the cipher block \nsize.', justify=LEFT).grid()

      Label(tab7, text = 'ENCRYPTION METHODS:\n===============\nIt is currently recommended to use the "AES-128 CBC" cipher. \n- The CBC mode will encrypt identical cleartext blocks into different ciphertext. \n- The ECB mode encrypts identical cleartext blocks into identical ciphertext blocks. \n- More methods are planned to be included! \n\nThere is nothing to stop you encrypting text, and then re-encrypting it using \nanother method. You should consider using "Hex Mode" if encrypting text which is \nalready "Hexified" (i.e contains only characters [0..9, a..f]). \n\nNB: NEVER re-use a Salt, IV, or Key on a message you wish to keep secure.', justify=LEFT).grid()

      Label(tab8, text = 'TESTING ENCRYPTION:\n============== \nIt is possible to test the encryption using Known Answer Test (KAT) Vectors. \n- KAT Vectors are usually published on the web in Hexadecimal notation, so \n   you should click the "Hex Mode" box. \n- Paste the KAT vector you wish to encrypt into the Clear Text window. \n- Next, check the "Enable" box to enter a Key. \n- Paste the Key used for the test into the "Key" row. \n- Click the "Keep" button to stop the software trying to calculate a new Key \n   when you encrypt.\n- If you are testing "CBC" mode, you will need to enter an IV for the KAT test, \n   and check the "Keep" box. \n\nNB: The "Encrypted Text" will have the Salt (and possibly IV) prepended \nbefore the actual encrypted message. As discussed, this presents NO \nsecurity risk to the user. The encrypted KAT vector can be compared to \nresults on the web by ignoring the Salt and IV portions of the Encrypted Text. \n\nNB: Be sure to double-check that the encryption method (e.g. "AES-128 CBC") \nis correct for the test you are performing! \n\n\nTESTING KEY GENERATION:\n================ \nIt is also possible to test that the Password and Salt correctly generate a Key. \n- You will have to look up PBKDF2 HMAC-SHA2 test vectors, and manually \n   enter (and keep) the Password and Salt. \n- The Salt has to be entered in Hexadecimal digits; so please convert any given \n   test Salt into "Hex" format before you enter it  -e.g. if the test Salt is the ASCII \n   string "NaCl", then you should enter "4e61436c" in the "Salt" window. \n- You will also have to override the PBKDF2 iterations to match the test value given. \n- We only keep enough bits of the derived Key to fit the Encryption Method being \n   used (e.g. AES-128 would keep 128 bits of the Key)', justify=LEFT).grid()

      Label(tab9, text = 'PyEyeCrypt (%s)    -    Copyright (C) 2015 "mi55 ing" <mi55ing@protonmail.ch>\n=================================================\nPLEASE REPORT FLAWS, BUGS, OR KNOWN SIDE-CHANNEL ATTACKS TO: \n"mi55 ing" <mi55ing@protonmail.ch> \n\nIt is politely suggested that you check the md5 hash of your downloaded \napplication against the value(s) on the github download page: \nhttps://github.com/mi55ing/PyEyeCrypt. \n- You can do this for the executable by simply typing (in OSX) "md5 PyEyeCrypt.app.tgz". \n- Check the source code by typing: "md5 PyEyeCrypt.py; md5 aes.py; md5 pbkdf2.py". \n\nIt is also suggested to perform encryption/decryption on a computer with (AT LEAST) \nan outbound firewall e.g. TCPBlock. Performing encryption whilst offline might also \nincrease your safety somewhat.' % PyEyeCryptVersion, justify=LEFT).grid()


   #####################################################
   # Initialise the main gui window 
   # with initial focus on ClearText window.
   #####################################################
   def __init__(self, master=None):
       Frame.__init__(self, master)
       self.pack()
       self.createWidgets()

       # Sort out the font for password field..using the salt field as a guide..
       fontinfoSalt = tkFont.Font(font=self.user_entry_salt['font'])
       salt_font_size_temp=fontinfoSalt.actual('size')       
       if salt_font_size_temp > root.bestpasswordfontsize:
          root.bestpasswordfontsize=salt_font_size_temp
          self.user_entry_password.config(font=("arial",root.bestpasswordfontsize))

       # Start the user on the ClearText or EncryptedText Window.
       # If we have isBadOS==1, then the user typing at startup actually does do *something*, albeit in the Encrypted Text window. 
       if self.CheckBoxValueClickKeyMode.get()==0:
          self.ClearText.focus_force()
       else:
          self.EncryptedText.focus_force()          
       # Eyes appear on startup.
       self.CheckBoxValueDisplayEyes.set(1)
       self.DisplayEyes()
       self.after(1500,self.CleanStartFirstEyesDonate)
       self.CheckBoxValueDisplayEyes.set(0)


######################################################################################
# A Class to allow multi-tabbing (e.g. in Help window) in Python 2                   #
######################################################################################
class Notebook(Frame):
    def __init__(self, parent, activerelief = SOLID, inactiverelief = SOLID, xpad = 4, ypad = 4, activefg = 'black',activebg='green',inactivebg='grey',bd=1,inactivefg = 'black', **kw):
        self.activefg = activefg
        self.activebg=activebg
        self.bd=bd
        self.inactivebg=inactivebg
        self.inactivefg = inactivefg
        self.deletedTabs = []        
        self.xpad = xpad
        self.ypad = ypad
        self.activerelief = activerelief
        self.inactiverelief = inactiverelief
        self.kwargs = kw
        self.tabVars = {}
        self.tabs = 0
        self.noteBookFrame = Frame(parent)
        self.BFrame = Frame(self.noteBookFrame)                                            
        self.noteBook = Frame(self.noteBookFrame, relief = RAISED, bd = 1, **kw)           
        self.noteBook.grid_propagate(0)
        Frame.__init__(self)
        self.noteBookFrame.grid()
        self.BFrame.grid(row =0, sticky = W)
        self.noteBook.grid(row = 1, column = 0, columnspan = 27)

    def add_tab(self, width = 1, **kw):            
            temp = self.tabs
            self.tabVars[self.tabs] = [Label(self.BFrame, relief = RIDGE, **kw)]               
            self.tabVars[self.tabs][0].bind("<Button-1>", lambda Event:self.change_tab(temp))  
            self.tabVars[self.tabs][0].pack(side = LEFT, ipady = self.ypad, ipadx = self.xpad) 
            self.tabVars[self.tabs].append(Frame(self.noteBook, **self.kwargs))                
            self.tabVars[self.tabs][1].grid(row = 0, column = 0)
            self.change_tab(0)
            self.tabs += 1
            return self.tabVars[temp][1]

    def change_tab(self, IDNum): 
        for i in (a for a in range(0, len(self.tabVars.keys()))):
            if not i in self.deletedTabs:
                if i <> IDNum:
                    self.tabVars[i][1].grid_remove()
                    self.tabVars[i][0]['relief'] = self.inactiverelief                     
                    self.tabVars[i][0]['fg'] = self.inactivefg
                    self.tabVars[i][0]['bg'] = self.inactivebg
                    self.tabVars[i][0]['bd'] = self.bd
                else:
                    self.tabVars[i][1].grid()
                    self.tabVars[IDNum][0]['relief'] = self.activerelief                   
                    self.tabVars[i][0]['fg'] = self.activefg
                    self.tabVars[i][0]['bg'] = self.activebg
                    self.tabVars[i][0]['bd'] = self.bd


######################################################################################
# A Class to make the keyboard Entropy Capture window to get                         #
# "desiredBits" worth of random hex.                                                 # 
######################################################################################
class EntropyWindow():
   def __init__(self,desiredBits):
        # Use the global version of the variables for window sizes in this class.
        global user_defined_frame_width
        global user_defined_frame_height

        self.entropywin=Toplevel()
        self.entropywin.title("PyEyeCrypt (%s)   -  Copyright (C) 2015:   Entropy (Randomness) Capture" %PyEyeCryptVersion)
        entropyframe=Frame(self.entropywin)
        self.entropywin.wm_geometry("%dx%d%+d%+d" % (3*user_defined_frame_width/4, 130, user_defined_frame_width/8, user_defined_frame_height/4)) 
        self.entropywin.grid_columnconfigure(0, weight=1)
        
        Label(entropyframe, text="ENTROPY GATHERING: Please press keys at RANDOM TIME INTERVALS:").grid(row=5, column=5, pady=(10,10), sticky=E+W)
        self.entropyKeyEntryWidget = self.makeentropyentry(entropyframe, 25) 
        self.entropyKeyEntryWidget.grid(row=5,column=6,columnspan=2,pady=(10,10), sticky=E+W)
        self.entropyKeyEntryWidget.focus_set()

        Label(entropyframe, text="Time: ").grid(row=6,column=5,sticky=E)
        self.sessionseedtimedisplay=StringVar()
        self.sessionseedtimedisplay.set("0.0000000000")
        self.displaytimevalues = Label(entropyframe, textvariable = self.sessionseedtimedisplay)
        self.displaytimevalues.grid(row=6,column=6, columnspan=2, sticky=W)

        self.sessionseedhexdisplay=StringVar()
        self.sessionseedhexdisplay.set("0x")
        self.displayhexvalues = Label(entropyframe, textvariable = self.sessionseedhexdisplay)
        self.displayhexvalues.grid(row=7,column=5,columnspan=2,sticky=W)

        self.bardisplay=StringVar()
        self.bardisplay.set("█")
        self.displayhexvalues = Label(entropyframe, textvariable = self.bardisplay)
        self.displayhexvalues.grid(row=8,column=5, columnspan=2,sticky=W)

        entropyframe.grid()

        #set up the variables needed later
        start_time = end_time = 0
        self.sessionseed=""

        # Grab a timedifference, make sure there are enough digits.
        # determine how many digits are in the timestamp after the decimal point..
        test_time=time()-start_time
        stringytesttime=repr(test_time)
        testtime_digits, testtimefract_digits = stringytesttime.split('.')    
        if len(testtimefract_digits) < 3:
           tkMessageBox.showwarning("Error Getting Entropy", "Error Getting Entropy: Time stamp does not have enough digits..\n start_time: %s \ntest_time: %s \ntesttimefract_digits: %s. \n\n Try Restarting PyEyeCrypt." % (start_time,test_time,testtimefract_digits) )
           sys.exit()

        # Keep 2 digits per keypress between positions 2-3 inclusive:
        self.digitstostartat=1
        self.digitstoendat=3

        def key(event): 
           end_time = time()
           timedifference=end_time-start_time
           stringythingy = repr(timedifference)
           signif_digits, fract_digits = stringythingy.split('.')

           #use zfill to ensure leading zeros for each of the decimal numbers after the first are counted too
           fract_firstdigits = fract_digits[self.digitstostartat:self.digitstoendat].zfill(self.digitstoendat-self.digitstostartat)

           self.sessionseedtimedisplay.set(str(timedifference)+" , ("+fract_firstdigits+")")
           self.sessionseed=fract_firstdigits+self.sessionseed
           self.sessionseedlong=long(self.sessionseed)
           self.sessionseedhex="%x" % self.sessionseedlong

           self.sessionseedhexdisplay.set("0x"+self.sessionseedhex)
           self.bardisplay.set(self.bardisplay.get().encode("utf8","strict")+"█")
           if len(self.sessionseedhex)*4 >= desiredBits:
              self.entropyKeyEntryWidget.unbind("<Key>")
              self.entropywin.destroy()
        self.entropyKeyEntryWidget.bind("<Key>", key) 
        start_time=time()
        self.entropyKeyEntryWidget.focus_force()
        self.entropywin.grab_set()

   def makeentropyentry(self,parent,width=None, **options):
        entry = Entry(parent, **options)
        if width:
           entry.config(width=width)
        return entry


######################################################################################
# Define the Class for the Clickable Keyboards                                       #
######################################################################################
class ClickableKeyboard():
   def __init__(self, parent, parentwidget):
      self.parent = parent
      self.parentwidget = parentwidget
      self.shiftToggle=0
      self.ConfigureParentWidget()

   def ConfigureParentWidget(self):
      #use the global version of the variable ckickableKeyboardSizeDenominator to get keyboard frame dimensions
      global ckickableKeyboardSizeDenominator      

      # Since we got here, we KNOW we don't have an existing Clickable Keyboard.
      # In this case, create one & position it.
      # First, Get the parent Window's x,y position so we can use it 
      # together with the parentwidget widget's size/offset
      # to correctly position the Clickable Keyboard.
      MainWindowOffsetX=self.parent.winfo_rootx()
      MainWindowOffsetY=self.parent.winfo_rooty()
      
      # Get the parentwidget widget's position, height & width so we can position the offset of the Clickable Keyboard
      parentwidgetGeometry= self.parentwidget.winfo_geometry()
      parentwidgetWidth   = parentwidgetGeometry.split('+')[0].split('x')[0]
      parentwidgetHeight  = parentwidgetGeometry.split('+')[0].split('x')[1]
      parentwidgetOffsetX = parentwidgetGeometry.split('+')[1]
      parentwidgetOffsetY = parentwidgetGeometry.split('+')[2]
      
      # Get the position to put the Ckickable Keyboard
      KeyboardOffsetX= int(MainWindowOffsetX) + int(parentwidgetOffsetX) 
      KeyboardOffsetY= int(MainWindowOffsetY) + int(parentwidgetOffsetY) + int(parentwidgetHeight)

      # Windows has an annoying habit of masking a little of the Password Entry widget with the Password Clickable Keyboard Window.
      # so I add 5px to the y-value.
      global theOS
      if theOS=="Windows":
         KeyboardOffsetY=KeyboardOffsetY+5

      # Set the "initial" width / height of the keyboard; this is annoyingly NOT
      # exactly what it should finally be -- it appears to differ by a few pixels
      KeyboardInitialWidth=int(float(2252)/float(ckickableKeyboardSizeDenominator))
      KeyboardInitialHeight=int(float(784)/float(ckickableKeyboardSizeDenominator))

      # Create the Clickable Keyboard Window with "initial" geometry from above.
      self.parentwidgetKeyboardWin=Toplevel()
      self.parentwidgetKeyboardWin.geometry("%dx%d+%d+%d" % ((KeyboardInitialWidth,KeyboardInitialHeight) + (KeyboardOffsetX,KeyboardOffsetY)))
      self.parentwidgetKeyboardWin.update_idletasks()
      self.parentwidgetKeyboardWin.title("PyEyeCrypt (%s)   -  Copyright (C) 2015: Keyboard" %PyEyeCryptVersion)
      myframe = Frame(self.parentwidgetKeyboardWin,width=KeyboardInitialWidth , height=KeyboardInitialHeight)

      # This is the special protocol we need to use to delete the Clickable Keyboard; 
      # It resets any global variables etc., then destroys the Clickable Keyboard.
      self.parentwidgetKeyboardWin.protocol("WM_DELETE_WINDOW", self.on_closing_parentwidgetKeyboardWin)
      
      # Import the background images of the UPPER and lower case keyboards.
      background_image_lc= PhotoImage(file = os.path.join(basedir, "keyblc-crop-framestage4-huge-krm-Enter-del-bkslpipe-arrows.gif"))
      background_image_uc= PhotoImage(file = os.path.join(basedir, "keybuc-crop-framestage4-huge-krm-Enter-del-bkslpipe-arrows.gif"))

      #Store scaled images as "Class varables", so we can swap the images when 'Shift' is pressed on the Clickable Keyboard.
      self.background_image_lc_scaled=background_image_lc.subsample(ckickableKeyboardSizeDenominator,ckickableKeyboardSizeDenominator)
      self.background_image_uc_scaled=background_image_uc.subsample(ckickableKeyboardSizeDenominator,ckickableKeyboardSizeDenominator)

      # Create the "Label" widget which holds the images of the keyboard.
      self.parentwidgetKeyboardWin.background_label=Label(self.parentwidgetKeyboardWin, image=self.background_image_lc_scaled, borderwidth=0)
      # Note the line below is needed. It keeps a reference. (Garbage Collector destroys it otherwise!).
      self.parentwidgetKeyboardWin.background_label.image=self.background_image_lc_scaled #Keeps a reference! (Garbage Collector destroys it otherwise!)
      self.parentwidgetKeyboardWin.background_label.place(x=0, y=0, relwidth=1, relheight=1)
      self.parentwidgetKeyboardWin.background_label.grid(row=1,column=1,columnspan=2)

      # Bind the left-button of the mouse to a "click" on the keyboard widget. 
      self.parentwidgetKeyboardWin.background_label.bind("<Button-1>", self.callbackClickedClickableKeyboard) 
      myframe.grid(row=1,column=1,columnspan=2)
      self.parentwidgetKeyboardWin.resizable(0,0)


   #####################################################
   # The function to close the "parentwidgetKeyboardWin" cleanly, 
   # It tells the parent widget that its ckickablekeyboard 
   # is no longer open, sets the keyboard focus
   # and then destroys() the Ckickable Keyboard Window.
   #####################################################
   def on_closing_parentwidgetKeyboardWin(self):
      if self.parentwidget==self.parent.ClearText:
         self.parent.ClearTextKeyboardOpened=0
      elif self.parentwidget==self.parent.user_entry_password:
         self.parent.PasswordKeyboardOpened=0
      else:
         tkMessageBox.showwarning("Error Closing Clickable Keyboard", "Error: unrecognised parent of Clickable Keyboard! Exiting. ")
         sys.exit()

      # Below means there is a definite focus, albeit null if the keyboard is closed and Click-to-type is still checked.
      # OSX (at least) can refuse to recognise mouse-clicks to force focus if this is not present!
      # - e.g if the user opens a clickable keyboard, then clicks on the entry/text widget, and then closes the keyboard window directly.
      self.parentwidget.focus_force() 
      self.parentwidgetKeyboardWin.destroy()


   #####################################################
   # The function which tells the ClearTextKeyboardWin
   # what each event (click) means..
   #####################################################
   def callbackClickedClickableKeyboard(self,event):
      actualWidth=self.parentwidgetKeyboardWin.winfo_width()
      actualHeight=self.parentwidgetKeyboardWin.winfo_height()
      relativeX=float(event.x)/float(actualWidth)
      relativeY=float(event.y)/float(actualHeight)
      keyPressed=""    
      #
      # ROW 1
      #
      if relativeY > 0.05 and relativeY < 0.23:
         if relativeX > 0.028 and relativeX < 0.085:
            if self.shiftToggle==0:
               keyPressed="`"
            else:
               keyPressed="~"
         if relativeX > 0.094 and relativeX < 0.153:
            if self.shiftToggle==0:
               keyPressed="1"
            else:
               keyPressed="!"
         if relativeX > 0.158 and relativeX < 0.218:
            if self.shiftToggle==0:
               keyPressed="2"
            else:
               keyPressed="@"
         if relativeX > 0.225 and relativeX < 0.284:
            if self.shiftToggle==0:
               keyPressed="3"
            else:
               keyPressed="#"
         if relativeX > 0.291 and relativeX < 0.350:
            if self.shiftToggle==0:
               keyPressed="4"
            else:
               keyPressed="$"
         if relativeX > 0.358 and relativeX < 0.417:
            if self.shiftToggle==0:
               keyPressed="5"
            else:
               keyPressed="%"
         if relativeX > 0.424 and relativeX < 0.483:
            if self.shiftToggle==0:
               keyPressed="6"
            else:
               keyPressed="^"
         if relativeX > 0.490 and relativeX < 0.549:
            if self.shiftToggle==0:
               keyPressed="7"
            else:
               keyPressed="&"
         if relativeX > 0.558 and relativeX < 0.616:
            if self.shiftToggle==0:
               keyPressed="8"
            else:
               keyPressed="*"
         if relativeX > 0.623 and relativeX < 0.682:
            if self.shiftToggle==0:
               keyPressed="9"
            else:
               keyPressed="("
         if relativeX > 0.689 and relativeX < 0.748:
            if self.shiftToggle==0:
               keyPressed="0"
            else:
               keyPressed=")"
         if relativeX > 0.755 and relativeX < 0.814:
            if self.shiftToggle==0:
               keyPressed="-"
            else:
               keyPressed="_"
         if relativeX > 0.821 and relativeX < 0.880:
            if self.shiftToggle==0:
               keyPressed="="
            else:
               keyPressed="+"
         if relativeX > 0.887 and relativeX < 0.982:
            #keyPressed="Bksp"
            self.parentwidget.config(state=NORMAL)
            try:
               self.parentwidget.delete("%s-1c" % INSERT, INSERT) 
            except:
               entryinsertpoint=self.parentwidget.index(INSERT)
               self.parentwidget.delete(entryinsertpoint-1,entryinsertpoint)
            self.parentwidget.config(state=DISABLED)
      #
      # ROW 2
      #
      if relativeY > 0.249 and relativeY < 0.413:
         if relativeX > 0.020 and relativeX < 0.131:
            keyPressed="\t"
         if relativeX > 0.139 and relativeX < 0.198:
            if self.shiftToggle==0:
               keyPressed="q"
            else:
               keyPressed="Q"
         if relativeX > 0.206 and relativeX < 0.265:
            if self.shiftToggle==0:
               keyPressed="w"
            else:
               keyPressed="W"
         if relativeX > 0.272 and relativeX < 0.331:
            if self.shiftToggle==0:
               keyPressed="e"
            else:
               keyPressed="E"
         if relativeX > 0.339 and relativeX < 0.396:
            if self.shiftToggle==0:
               keyPressed="r"
            else:
               keyPressed="R"
         if relativeX > 0.405 and relativeX < 0.464:
            if self.shiftToggle==0:
               keyPressed="t"
            else:
               keyPressed="T"
         if relativeX > 0.472 and relativeX < 0.529:
            if self.shiftToggle==0:
               keyPressed="y"
            else:
               keyPressed="Y"
         if relativeX > 0.536 and relativeX < 0.595:
            if self.shiftToggle==0:
               keyPressed="u"
            else:
               keyPressed="U"
         if relativeX > 0.604 and relativeX < 0.663:
            if self.shiftToggle==0:
               keyPressed="i"
            else:
               keyPressed="I"
         if relativeX > 0.670 and relativeX < 0.728:
            if self.shiftToggle==0:
               keyPressed="o"
            else:
               keyPressed="O"
         if relativeX > 0.735 and relativeX < 0.794:
            if self.shiftToggle==0:
               keyPressed="p"
            else:
               keyPressed="P"
         if relativeX > 0.801 and relativeX < 0.860:
            if self.shiftToggle==0:
               keyPressed="["
            else:
               keyPressed="{"
         if relativeX > 0.869 and relativeX < 0.928:
            if self.shiftToggle==0:
               keyPressed="]"
            else:
               keyPressed="}"
         if relativeX > 0.934 and relativeX < 0.993:
            #keyPressed="DEL"
            self.parentwidget.config(state=NORMAL)
            self.parentwidget.delete('insert')
            self.parentwidget.config(state=DISABLED)
      #
      # ROW 3
      #
      if relativeY > 0.433 and relativeY < 0.602:
         if relativeX > 0.092 and relativeX < 0.151:
            if self.shiftToggle==0:
               keyPressed="a"
            else:
               keyPressed="A"
         if relativeX > 0.158 and relativeX < 0.217:
            if self.shiftToggle==0:
               keyPressed="s"
            else:
               keyPressed="S"
         if relativeX > 0.224 and relativeX < 0.283:
            if self.shiftToggle==0:
               keyPressed="d"
            else:
               keyPressed="D"
         if relativeX > 0.290 and relativeX < 0.348:
            if self.shiftToggle==0:
               keyPressed="f"
            else:
               keyPressed="F"
         if relativeX > 0.355 and relativeX < 0.415:
            if self.shiftToggle==0:
               keyPressed="g"
            else:
               keyPressed="G"
         if relativeX > 0.422 and relativeX < 0.481:
            if self.shiftToggle==0:
               keyPressed="h"
            else:
               keyPressed="H"
         if relativeX > 0.489 and relativeX < 0.547:
            if self.shiftToggle==0:
               keyPressed="j"
            else:
               keyPressed="J"
         if relativeX > 0.555 and relativeX < 0.613:
            if self.shiftToggle==0:
               keyPressed="k"
            else:
               keyPressed="K"
         if relativeX > 0.620 and relativeX < 0.680:
            if self.shiftToggle==0:
               keyPressed="l"
            else:
               keyPressed="L"
         if relativeX > 0.687 and relativeX < 0.746:
            if self.shiftToggle==0:
               keyPressed=";"
            else:
               keyPressed=":"
         if relativeX > 0.753 and relativeX < 0.812:
            if self.shiftToggle==0:
               keyPressed="'"
            else:
               keyPressed="\""
         if relativeX > 0.816 and relativeX < 0.873:
            if self.shiftToggle==0:
               keyPressed="\\"
            else:
               keyPressed="|"
         if relativeX > 0.890 and relativeX < 0.990:
            keyPressed="\n"
      #
      # ROW 4
      #
      if relativeY > 0.623 and relativeY < 0.791:
         if relativeX > 0.080 and relativeX < 0.170:
            if self.shiftToggle == 0:
               self.shiftToggle=1
               self.parentwidgetKeyboardWin.background_label.configure(image=self.background_image_uc_scaled)
            else:
               self.shiftToggle=0
               self.parentwidgetKeyboardWin.background_label.configure(image=self.background_image_lc_scaled)
         if relativeX > 0.178 and relativeX < 0.238:
            if self.shiftToggle==0:
               keyPressed="z"
            else:
               keyPressed="Z"
         if relativeX > 0.245 and relativeX < 0.304:
            if self.shiftToggle==0:
               keyPressed="x"
            else:
               keyPressed="X"
         if relativeX > 0.311 and relativeX < 0.370:
            if self.shiftToggle==0:
               keyPressed="c"
            else:
               keyPressed="C"
         if relativeX > 0.378 and relativeX < 0.437:
            if self.shiftToggle==0:
               keyPressed="v"
            else:
               keyPressed="V"
         if relativeX > 0.444 and relativeX < 0.503:
            if self.shiftToggle==0:
               keyPressed="b"
            else:
               keyPressed="B"
         if relativeX > 0.510 and relativeX < 0.568:
            if self.shiftToggle==0:
               keyPressed="n"
            else:
               keyPressed="N"
         if relativeX > 0.575 and relativeX < 0.634:
            if self.shiftToggle==0:
               keyPressed="m"
            else:
               keyPressed="M"
         if relativeX > 0.641 and relativeX < 0.700:
            if self.shiftToggle==0:
               keyPressed=","
            else:
               keyPressed="<"
         if relativeX > 0.708 and relativeX < 0.767:
            if self.shiftToggle==0:
               keyPressed="."
            else:
               keyPressed=">"
         if relativeX > 0.774 and relativeX < 0.833:
            if self.shiftToggle==0:
               keyPressed="/"
            else:
               keyPressed="?"
         if relativeX > 0.840 and relativeX < 0.931:
            if self.shiftToggle == 0:
               self.shiftToggle=1
               self.parentwidgetKeyboardWin.background_label.configure(image=self.background_image_uc_scaled)
            else:
               self.shiftToggle=0
               self.parentwidgetKeyboardWin.background_label.configure(image=self.background_image_lc_scaled)
      #
      # ROW 5
      #
      if relativeY > 0.795 and relativeY < 0.995:
         if relativeX > 0.282 and relativeX < 0.731:
            keyPressed=" "
         if relativeX > 0.805 and relativeX < 0.995:
            # Arrow Keys
            if relativeY > 0.900 and relativeY < 0.995:

               if relativeX > 0.805 and relativeX < 0.863:
                  #keyPressed="LEFT"
                  # Sadly the "Entry" and "Text" widgets behave differently when asked for "index".
                  # If we try to split the Entry index, we get an "AttributeError"
                  try:
                     currentpos=self.parentwidget.index('insert').split('.')
                     currentline=currentpos[0]
                     currentcol=currentpos[1]
                     desiredcol=int(currentcol)-1
                     self.parentwidget.mark_set('insert' , currentline+'.'+str(desiredcol))
                  except AttributeError:   
                     currentcol=self.parentwidget.index(INSERT)
                     desiredcol=int(currentcol)-1
                     self.parentwidget.icursor(desiredcol)
                  except:
                     tkMessageBox.showwarning("Exception", "Exception: Can not determine parent widget to pass 'left arrow' to.")
                     return

               if relativeX > 0.869 and relativeX < 0.928:
                  #keyPressed="DOWN"
                  try:
                     currentpos=self.parentwidget.index('insert').split('.')
                     currentline=currentpos[0]
                     currentcol=currentpos[1]
                     desiredline=int(currentline)+1
                     self.parentwidget.mark_set('insert' , str(desiredline)+'.'+currentcol)
                  except AttributeError:   
                     currentcol=self.parentwidget.index(INSERT)
                     desiredcol=int(currentcol)+1
                     self.parentwidget.icursor(desiredcol)
                  except:
                     tkMessageBox.showwarning("Exception", "Exception: Can not determine parent widget to pass 'down arrow' to.")
                     return

               if relativeX > 0.935 and relativeX < 0.995:
                  #keyPressed="RIGHT"
                  try:
                     currentpos=self.parentwidget.index('insert').split('.')
                     currentline=currentpos[0]
                     currentcol=currentpos[1]
                     desiredcol=int(currentcol)+1
                     self.parentwidget.mark_set('insert' , currentline+'.'+str(desiredcol))
                  except AttributeError:   
                     currentcol=self.parentwidget.index(INSERT)
                     desiredcol=int(currentcol)+1
                     self.parentwidget.icursor(desiredcol)
                  except:
                     tkMessageBox.showwarning("Exception", "Exception: Can not determine parent widget to pass 'right arrow' to.")
                     return
                     
            if relativeX > 0.869 and relativeX < 0.928 and relativeY > 0.795 and relativeY < 0.888:
               #keyPressed="UP"
               try:
                  currentpos=self.parentwidget.index('insert').split('.')
                  currentline=currentpos[0]
                  currentcol=currentpos[1]
                  desiredline=int(currentline)-1
                  self.parentwidget.mark_set('insert' , str(desiredline)+'.'+currentcol)
               except AttributeError:   
                  currentcol=self.parentwidget.index(INSERT)
                  desiredcol=int(currentcol)-1
                  self.parentwidget.icursor(desiredcol)
               except:
                  tkMessageBox.showwarning("Exception", "Exception: Can not determine parent widget to pass 'up arrow' to.")
                  return

      # Most of the keys just insert a character.
      # If this event needs to insert, it will be done here.
      # Some keys don't insert; their action happens 
      # directly above, and keyPressed is blank.
      # The "see" method ensures the window scrolls to the insert point.
      if keyPressed != "":
         self.parentwidget.config(state=NORMAL)
         self.parentwidget.insert(INSERT,keyPressed)
         self.parentwidget.config(state=DISABLED)

      # After a key-press, and even if "keyPress" was blank, 
      # try to update the cursor "mycurs" to the current INSERT position.
      # AND update the "mycurslinehi" to highlight the current line.
      # Also, update the scrollbar to ensure we can still see the insert point.
      # This will only work when parentwidget is 'Text' , not 'Entry'. 
      # because the 'Entry' widget cannot accept tags.
      try:
         self.parentwidget.tag_remove('mycurs', 1.0, 'end')
         self.parentwidget.tag_add("mycurs", INSERT+'-0c', INSERT+'+1c')    
         self.parentwidget.tag_remove('mycurslinehi', 1.0, 'end')
         self.parentwidget.tag_add("mycurslinehi", 'insert lineend', 'insert lineend'+'+1c')
         self.parentwidget.see(INSERT)
      except:
         return


######################################################################################
# The main loop here                                                                 #
######################################################################################
root=Tk() 
root.title("PyEyeCrypt (%s)   -  Copyright (C) 2015:   Python-based Open Source Text Encryption GUI" %PyEyeCryptVersion)

# Allow the root window to expand..col=0,2,21,31,32,51, row=0,10,19
root.grid_columnconfigure(0,weight=1)
root.grid_columnconfigure(2,weight=1)
root.grid_columnconfigure(21,weight=1)
root.grid_columnconfigure(31,weight=1)
root.grid_columnconfigure(34,weight=1)
root.grid_columnconfigure(49,weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(10,weight=1)
root.grid_rowconfigure(19,weight=1)

# Our target initial width for the gui, assuming a small screen, will be close-to fullscreen. So which fits best?
# choose a ludicrously small size to begin with...
startingwidth=50
startingheight=50
startingwidth=root.winfo_screenwidth() *0.999
startingheight=root.winfo_screenheight() *0.999

# However, if we have an HD screen, don't fill it all with the gui!
if (root.winfo_screenwidth() > 1600 and root.winfo_screenheight() >1000 ):
   startingwidth=1565
   startingheight=950

# Text varies cross-platform and by python version! - so we need to get the width of 64 chars & height of 36 lines (in pixels) for courier font.
# in sizes 6,7,8,9,10,11,12,14,16,18
widthheightlist=[]
for myfontsize in [6,7,8,9,10,11,12,13,14,16,18]:
   font = tkFont.Font(family='courier', size=myfontsize, weight=tkFont.BOLD)
   (fontwidth,fontheight) = (font.measure("1234567890123456789012345678901234567890123456789012345678901234"),font.metrics("linespace"))
   widthheightlist.append([myfontsize,fontwidth,fontheight])


# The 64chars width and 36 chars height of courier font MUST fit in the text widget window "w" x "h". 
# make a list of fontsizes  which are "less than w" and "less than or equal to h" respectively
widthheightdiffs=[]
for measurement in widthheightlist:
   # Append the FontSize, width (px), height (px), diff(startingwidth-expected overall width), diff(startingheight-expected overall starting height)
   # NB: the factors 1.354 & 1.54 came from measurements of the gui.
   widthheightdiffs.append([measurement[0], measurement[1], measurement[2], startingwidth-(measurement[1]*2*1.354), startingheight-(measurement[2]*36*1.54)])
                          
# Set horibly small default font and w,h of the text widget
bestfontsize=2
root.bestpasswordfontsize=2
w=50
h=50

# Both diffw & diffh must be positive for a font to 'fit' in the gui.
# i.e. the diffw* and diffh* must be >=0 so we don't exceed the screen size.
# Since we ordered these in increasing font size, we will take the last one which fits.
for diffs in widthheightdiffs:
   if diffs[3] >=0 and diffs[4] >=0:
      bestfontsize=diffs[0]
      w=diffs[1]
      h=diffs[2]

# Finally, determine the font size for the Donate QR Code which fits in the (now decided) "w" and "h" for each text widget.
# QR code plus text needs 33 rows.
# NB: we do this in 'reverse order' from large font size down to small.
QRlist=[]
for myfontsize in [18,16,14,13,12,11,10,9,8,7,6]:
   font = tkFont.Font(family='courier', size=myfontsize, weight=tkFont.BOLD) 
   (QRwidth,QRheight) = (font.measure("██████████████████████████████████████████████████████████████"),font.metrics("linespace")) 
   if QRwidth < w and QRheight <= h:
      QRlist.append(myfontsize)

# Failing all that, append a tiny font, to make sure there's something in the QRlist!
QRlist.append(2)

# Since this is done in descending order, the largest font which fits will be at the beginning of the list.
bestdonatefontsize=QRlist[0]

# If the donatefont needs to be smaller, use it as the bestfontsize
if bestdonatefontsize < bestfontsize:
   bestfontsize=bestdonatefontsize

# Store the bestfontsize in "user_defined_font_size" so it can be altered later..
user_defined_font_size=bestfontsize


# Set initial geometry of window, and also set the values which the user can override.
frame_width=int(w*2*1.354)
user_defined_frame_width=frame_width
frame_height=int(h*36*1.54)
user_defined_frame_height=frame_height

# Set geometry of Clickable Keyboard using Clear Text Widget width "w" and height "h"
# Clickable Keyboard is 2252 x 784 px. 
# Make sure the new window is always SMALLER than the width of the existing ClearText widget by adding 1.0.
ckickableKeyboardSizeDenominator=int( (float(2252)/float(w)) + 1.0 )

# Define initial user-entered text content as ""
user_entered_ClearText=""
user_entered_EncryptedText=""

# Needed! - enables us to make a slightly different treatment for displaying 'eyes' on startup.
loopcount=0

# Set up the main window geometry.
root.wm_geometry("%dx%d%+d%+d" % (frame_width,frame_height,0, 0))

# Get some entropy from the Keyboard, to use as a seed for 
# the Pseudo Random Number Generator (PRNG).
# Note: we will ONLY ever use PRNG in XOR with "os.urandom"  
desiredEntropyBits=256
initialEntropyWindow=EntropyWindow(desiredEntropyBits)
root.deiconify()
root.lift()
try:
   initialEntropyWindow.entropywin.attributes("-topmost", True)
except:
   initialEntropyWindow.entropywin.lift()

#####################################################
# Detect OS, and possibly bring the gui window to the foreground. 
# The basic methods are deiconify(),lift(),focus_force(), though this does not work on OSX.
# If we're working on OSX, the focus will not be set on the application.
# we can force it in 10.X Kernel with osascript.
# Linux prtion used https://github.com/hpcugent/easybuild/wiki/OS_flavor_name_version
#####################################################
theOS=platform.system()
print "theOS=", theOS

#####################################################
# OSX
#####################################################
if theOS=="Darwin":
   # Darwin Releases...
   # 10.8   (OSX Snow Leopard)
   # 12.6.0 (Last release of OSX Mountain Lion)
   # PyEyeCrypt Security Cutoff here: Mavericks was a free upgrade; much more cloud-based.
   # 13.0   (OSX Mavericks)
   # 13.4   (Last release of OSX Mavericks)
   # 14.0   (OSX Yosemite)
   # ??.?   (OSX El Capitan) 
   DarwinKernelMajor=99  #<- a big number, so assume 'bad' OS.
   DarwinKernelMinor=99  #<- a big number, so assume 'bad' OS.
   try:
      DarwinKernel=platform.release().split('.')
      DarwinKernelMajor=int(DarwinKernel[0])
      DarwinKernelMinor=int(DarwinKernel[1])
      print "Kernel Major: ",DarwinKernelMajor
      print "Kernel Minor: ",DarwinKernelMinor 

      # Force the focus in OSX (lift() focus_force() doesn't work!
      print "Darwin / OSX, forcing focus may be required..."
      if DarwinKernelMajor >= 10:
         print "Kernel Version is >= 10.X, using osascript to force focus.."
         os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

         #This needs to be done again, unfortunately.
         try:
            initialEntropyWindow.entropywin.attributes("-topmost", True)
         except:
            initialEntropyWindow.entropywin.lift()
    
      # PyEyeCrypt will assume "clickable Keyboard" mode for Kernels >= 13.0.0
      if DarwinKernelMajor < 13:
         isBadOS=0
      else:
         isBadOS=1
   except:
      isBadOS=1      

#####################################################
# Windows
#####################################################
elif theOS=="Windows":
   # Trust Windows as far as you can throw it.  
   isBadOS=1    
   
#####################################################
# Linux
#####################################################
elif theOS=="Linux":
   #Opposite strategy to Windows: assume Linux is good and trap the bad.
   isBadOS=0

   # Ubuntu and "unity" desktop are known to compromise user data.
   # "elementary os" is essentially ubuntu.
   # Linux Mint includes proprietary software, ergo the OS is not open-source.
   try:
      LinuxDistribution=platform.linux_distribution()[0]
      print "Linux Distro: ",LinuxDistribution
      if LinuxDistribution=="Ubuntu":
         isBadOS=1
      elif LinuxDistribution=="ubuntu":
         isBadOS=1
      elif LinuxDistribution.startswith("elementary"):
         isBadOS=1
      elif LinuxDistribution.startswith("Elementary"):
         isBadOS=1
      elif LinuxDistribution=="LinuxMint":
         isBadOS=1
      elif LinuxDistribution=="linuxmint":
         isBadOS=1
      elif LinuxDistribution=="Mint":
         isBadOS=1
      elif LinuxDistribution=="mint":
         isBadOS=1
   except:
      print "platform.linux_distribution() apparently wasn't working. Assume Bad OS."
      isBadOS=1    
   #Since it is known that platform.linux_distribution() sometimes returns debian instead of ubuntu..
   try:
      LinuxDistributionTry2=platform.dist()[0]
      print "Linux Distro Try 2: ",LinuxDistributionTry2
      if LinuxDistributionTry2=="Ubuntu":
         isBadOS=1
      elif LinuxDistributionTry2=="ubuntu":
         isBadOS=1
   except:
      # Less stringent here since platform.dist has been depricated..      
      print "platform.dist() wasn't working... carry on"
   # Now look for unity/ubuntu in "DESKTOP_SESSION"
   desktop_session = os.environ.get("DESKTOP_SESSION")   
   if desktop_session:
      if desktop_session in ["unity", "Unity" ]:
         isBadOS=1
      elif desktop_session.startswith("ubuntu"):
         isBadOS=1
      elif desktop_session.startswith("lubuntu"): # LXDE in Ubuntu
         isBadOS=1
      elif desktop_session.startswith("kubuntu"): # KDE in ubuntu
         isBadOS=1
      elif desktop_session.startswith("xubuntu"): # XFCE in ubuntu
         isBadOS=1
      elif desktop_session.startswith("ubuntu"): 
         isBadOS=1
         
#####################################################
#Other operating systems; e.g. Solaris, DSM..  assume 'bad' for now.
#####################################################
else:
   isBadOS=1    
#####################################################
# END Small diversion from main loop to detect OS and bring gui window to foreground
#####################################################

# Wait for the Entropy to be gathered before checking sessionseed...
initialEntropyWindow.entropyKeyEntryWidget.wait_window(initialEntropyWindow.entropywin)

# Check the "sessionseedhex" exists, and has enough entropy..
try:
   lenSessionseedhex=len(initialEntropyWindow.sessionseedhex)
except:
   tkMessageBox.showwarning("Error Getting Entropy", "Error Getting Entropy: No entropy. Unable to continue." )
   sys.exit()
if lenSessionseedhex < desiredEntropyBits/4:
   tkMessageBox.showwarning("Error Getting Entropy", "Error Getting Entropy: Not enough entropy to continue." )
   sys.exit()
random.seed(initialEntropyWindow.sessionseedlong)

# Start the main window
app=MainWindowFrame(root)
app.grid(sticky=NSEW)
app.mainloop()
