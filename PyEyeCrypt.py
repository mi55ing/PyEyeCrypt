# -*- coding: utf-8 -*-
# THE ABOVE LINE IS REQUIRED TO ENABLE UTF-8 DISPLAY IN THE TEXT WIDGETS.            # 
######################################################################################
#                                                                                    #
PyEyeCryptVersion="v1.0"                                                             #
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
# v1.0:                                                                              #
# Initial Release                                                                    # 
#                                                                                    #
#                                                                                    #
# Future Improvements                                                                #
# ===================                                                                #
# 1: Message Authentication                                                          #
# 2: Add Win10 spying "Countermeasures"; allow to run in Win10.                      #
# 3: Add a "characters to complete block" counter under/on top of Cleartext          #
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

######################################################################################
# Define the Class for the Main Window                                               #
######################################################################################
class MainWindowFrame(Frame):

   #####################################################
   # Create Widgets in the main gui window
   #####################################################
   def createWidgets(self):
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
       self.EncryptMethod.grid(row=14,column=27,pady=(40,0),padx=10,sticky=S)
       ToolTip.ToolTip(self.EncryptMethod, 'Cipher Mode: CBC-mode is recommended.')
       
       self.Encrypt = Button(self)
       self.Encrypt["text"] = ">>ENCRYPT>>"
       self.Encrypt["fg"] = "red"
       self.Encrypt["command"] = self.ValidateEncryptText
       self.Encrypt.grid(row=15,column=27, pady=(0,0),padx=10, sticky=S+N)      
       
       self.Decrypt = Button(self)
       self.Decrypt["text"] = "<<DECRYPT<<"
       self.Decrypt["fg"] = "red"
       self.Decrypt["command"] = self.ValidateDecryptText
       self.Decrypt.grid(row=16,column=27, pady=(0,00),padx=10, sticky=N)      
        
       self.CheckBoxValueHexMode=IntVar()
       self.HexModeButton = Checkbutton(self)
       self.HexModeButton["text"] = "Hex Mode"
       self.HexModeButton["command"] = self.HexEnable
       self.HexModeButton["variable"] = self.CheckBoxValueHexMode
       self.HexModeButton.grid(row=17,column=27,padx=(80,60), pady=(0,0), sticky=N+W) 
       ToolTip.ToolTip(self.HexModeButton, 'Hex Mode: Used for trying out Known Answer Test (KAT) Vectors')       

       self.CheckBoxValueDisplayEyes=IntVar()
       self.DisplayEyesButton = Checkbutton(self)
       self.DisplayEyesButton["text"] = "Eyes"
       self.DisplayEyesButton["command"] = self.DisplayEyes
       self.DisplayEyesButton["variable"] = self.CheckBoxValueDisplayEyes
       self.DisplayEyesButton.grid(row=18,column=27,padx=(80,60), pady=(0,0), sticky=N+W) 
       self.DisplayEyesButton.config(state=DISABLED)

       self.CheckBoxValueDisplayDonate=IntVar()
       self.DisplayDonateButton = Checkbutton(self)
       self.DisplayDonateButton["text"] = "Donate"
       self.DisplayDonateButton["command"] = self.DisplayDonate
       self.DisplayDonateButton["variable"] = self.CheckBoxValueDisplayDonate
       self.DisplayDonateButton.grid(row=19,column=27,padx=(80,60), pady=(0,10), sticky=N+W) 
       self.DisplayDonateButton.config(state=DISABLED)

       self.user_entry_password= self.makeentry(self, 32, show="*", background="black",foreground="yellow", insertbackground="yellow",highlightthickness=0);
       self.user_entry_password.grid( row= 29, column=27,pady=(80,0), sticky=W+S)
       Label(self, text="Password (Secret!):").grid(row=29, column=21, padx=(10,0),pady=(80,0), sticky=E+S)

       self.CheckBoxValueDisplayPassword=IntVar()
       self.DisplayPasswordButton = Checkbutton(self)
       self.DisplayPasswordButton["text"] = "Reveal"
       self.DisplayPasswordButton["command"] = self.ShowHidePass 
       self.DisplayPasswordButton["variable"] = self.CheckBoxValueDisplayPassword
       self.DisplayPasswordButton.grid(row=29,column=32,padx=(0,0), pady=(80,0), sticky=W+S) 

       self.user_entry_salt= self.makeentry(self, 32, background="black",foreground="yellow", insertbackground="yellow",highlightthickness=0, disabledforeground="gray50",disabledbackground="gray81");
       self.user_entry_salt.grid( row= 30, column=27,pady=(0,0), sticky=W+N+S)
       Label(self, text="Password Salt:").grid(row=30, column=21, padx=(10,0),pady=(0,0), sticky=E)
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

       self.user_entry_key= self.makeentry(self, 32, show="*", background="black",foreground="yellow", insertbackground="yellow",highlightthickness=0, disabledforeground="gray50",disabledbackground="gray81");
       self.user_entry_key.grid( row= 31, column=27,pady=(0,0), sticky=W+N+S)
       Label(self, text="Key (Secret!):").grid(row=31, column=21, padx=(10,0),pady=(0,0), sticky=E+N)
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

       self.user_entry_iv= self.makeentry(self, 32, background="black",foreground="yellow", insertbackground="yellow",highlightthickness=0, disabledforeground="gray50",disabledbackground="gray81");
       self.user_entry_iv.grid( row= 32, column=27,pady=(0,0), sticky=W+N+S)
       Label(self, text="IV:").grid(row=32, column=21, padx=(10,0),pady=(0,0), sticky=E+N)
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

       self.user_entry_pbkdf2_iter= self.makeentry(self, 32, show="", background="black",foreground="yellow", insertbackground="yellow",highlightthickness=0, disabledforeground="gray50",disabledbackground="gray81");
       self.user_entry_pbkdf2_iter.grid( row= 33, column=27,pady=(0,20),padx=(0,0), sticky=W+N)
       Label(self, text="PBKDF2 iterations").grid(row=33, column=21, padx=(10,0),pady=(0,20), sticky=E+N)
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
      else:
         self.user_entry_key.config(state=DISABLED)

   def EnableSaltEntry(self):
      if self.CheckBoxValueEnableSaltEntry.get()==1:
         self.user_entry_salt.config(state=NORMAL)
      else:
         self.user_entry_salt.config(state=DISABLED)

   def EnableIvEntry(self):
      if self.CheckBoxValueEnableIvEntry.get()==1:
         self.user_entry_iv.config(state=NORMAL)
      else:
         self.user_entry_iv.config(state=DISABLED)

   def EnablePBKDF2Entry(self):
      if self.CheckBoxValueEnablePBKDF2Entry.get()==1:
         tkMessageBox.showwarning("Warning", "Changing PBKDF2 iterations: \n\nIf you change this value, you MUST tell your intended recipient, otherwise they will not be able to generate the Key \n-even if they have the correct password!" )
         self.user_entry_pbkdf2_iter.config(state=NORMAL)
      else:
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


   #####################################################
   # Functions to clean the windows
   #####################################################
   def DeleteClearText(self):
       self.ClearText.delete(1.0,END) 

   def DeleteEncryptedText(self):
       self.EncryptedText.delete(1.0,END)

   def CleanStart(self):
       self.DeleteClearText()
       self.DeleteEncryptedText()

   def CleanStartFirstEyesDonate(self):
       self.DisplayEyesButton.config(state=NORMAL)
       self.DisplayDonateButton.config(state=NORMAL)
       #Finally, clear the windows.
       self.CleanStart()


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

       # Do the following extra checks on ClearText and EncryptedText, if we are in hex mode:      
       if self.CheckBoxValueHexMode.get()==1:
          #get the contents of cleartext, key and encrypted text and see if only 0-9&a/A,b/B,c/C,d/D,e/E,f/F
          ClearTextContent=self.ClearText.get("1.0",END)
          if ClearTextContent[-1:] == '\n':
             ClearTextContent = ClearTextContent[:-1]
          EncryptedTextContent=self.EncryptedText.get("1.0",END)
          if EncryptedTextContent[-1:] == '\n':
             EncryptedTextContent = EncryptedTextContent[:-1]
          for hexchar in ClearTextContent:
             if hexchar not in allowed:
                #Trip the ERROR variable so we know there's a char in the text which is not allowed for HEX mode.
                errorTripped="Clear Text Window"
          for hexchar in EncryptedTextContent:
             if hexchar not in allowed:
                #Trip the ERROR variable so we know there's a char in the text which is not allowed for HEX mode.
                errorTripped="Encrypted Text Window"                              

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
         tkMessageBox.showwarning("Padding Text", "Text (%s bits) is not a multiple of %s bits. Padding..  \n\nNOTE: When this text is DEcrypted, it will have spurious extra characters at the end of the message. \n\nEither lengthen the message yourself, or warn the recipient. \n\n-FOR REFERENCE: \nMissing bits from text: %s \n\n-Randombytes retrieved: %s \n\n-Hex digits required: %s \n\n-Calculated Hex Padding: %s" % (lengthOfHexlifiedContentInBits,BlockSizeInBits,finalmissingbits,randombytes,hexdigitsrequired,hexpadding))
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
          return 7

       # Check that salt is present/ right length.
       salt_text=self.user_entry_salt.get()
       if (len(salt_text)*4) != saltsize:
          tkMessageBox.showwarning("Encrypt Not Possible", "Can not produce encrypted text. \n\n'Salt' length is wrong number of bits. Should be %s bits." % saltsize  )
          return 8

       # Check that the Key is present
       if self.user_entry_key.get()=="":  
          tkMessageBox.showwarning("Encrypt Not Possible", "'Key' is empty." )
          return 9          

       # See if the Key is the right length -take each HEX digit as 4 bytes, so multiply by 4.
       key_text=self.user_entry_key.get()
       if (len(key_text)*4) != keysize:
          tkMessageBox.showwarning("Encrypt Not Possible", "'Key' length is wrong number of bits. Should be %s bits." % keysize  )
          return 10

       # See if the IV is the right size. This one CAN be empty in ECB mode, for example.
       iv_text=self.user_entry_iv.get()
       if (len(iv_text)*4) != ivsize:
          tkMessageBox.showwarning("Encrypt Not Possible", "'IV' is wrong length (%s bytes) . Should be %s bytes." % (len(iv_text)*4,ivsize)  )
          return 11

       # Check that Salt, Key, IV only contain HEX digits; regardless of whether we're in hex mode this should be true.
       validate=""
       validate=self.HexCheck()
       if validate!="":
          tkMessageBox.showwarning("Invalid Characters", "%s has invalid characters. \n\nOnly characters \n[0..9, a..f, A..F] are allowed.\n\n--NO SPACES, or CR/LF's!--" % validate )
          return 12   

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
             return 13
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
             tkMessageBox.showwarning("Key Overwrite", "'Key' field is not empty. \n'Key' will be overwritten!" )
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
             tkMessageBox.showwarning("IV Overwrite", "'IV' field is not empty. \n'IV' will be overwritten!" )
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
             tkMessageBox.showwarning("Salt Overwrite", "'Salt' field is not empty. \n'Salt' will be overwritten!" )
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

       #For Decrypt only,  see if the user-entered Salt is EMPTY. It should be empty for DECRYPTION to begin with. 
       #Differs relative to Encrypt! (There, salt_text is checked against salt_size and demanded if needed.)
       salt_text=self.user_entry_salt.get()
       if len(salt_text) != 0:
          tkMessageBox.showwarning("Salt Overwrite", "'Salt' field is not empty. \n'Salt' will be overwritten!" )
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
          tkMessageBox.showwarning("IV Overwrite", "'IV' field is not empty. \n'IV' will be overwritten!" )
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
             tkMessageBox.showwarning("Key Overwrite", "'Key' field is not empty. \n'Key' will be overwritten!" )
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
          return 7

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
             return 8

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
             return 9


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
          return 10          

       # See if the Key is the right length -take each HEX digit as 4 bytes, so multiply by 4.
       key_text=self.user_entry_key.get()
       if (len(key_text)*4) != keysize:
          tkMessageBox.showwarning("Decrypt Not Possible", "'Key' length is wrong number of bits. Should be %s bits." % keysize  )
          return 11
             
       # For AES, whether in HEX mode or not, we expect EncryptedText to be in hex.
       # I require text to be a muliple of the blocksize (usually 128 bits).
       trailingpadding=""
       if ((len(EncryptedTextContent)*4) % blocksize ) !=0:
          tkMessageBox.showwarning("Padding Encryptedtext", "Warning: Encrypted text is being padded. Are you running the correct decryption algo?" )
          trailingpadding=self.PadTo128Bits( len(EncryptedTextContent)*4, blocksize )
          #Error Trapping - should only consist of hex digits so we will never falsely detect an error if we look for "PaddingError"!
          if (trailingpadding=="PaddingError"):
             tkMessageBox.showwarning("Padding Encryptedtext", "Error in PadTo128Bits() Function. Padding FAILED." )
             return 12 
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

       if self.CheckBoxValueHexMode.get()==1:
          self.ClearText.insert(END,total_stripped_decrypted_filled)
       else:
          # Unhexlify and sanitise the stripped_decrypted_filled block; it CAN have padded junk which does not correspond to ascii chars. 
          unhexlified_stripped_decrypted_filled=binascii.unhexlify(total_stripped_decrypted_filled).decode('utf8','replace')
          self.ClearText.insert(END,unhexlified_stripped_decrypted_filled)
   

   #####################################################
   # Function to hide/display content with "eyes"
   #####################################################
   def DisplayEyes(self):
       # Use the 'global' copies of these four variables, otherwise Python will try to make local copies all on its own!
       # We need global-level memory of the user-defined window dimensions and Text content of the windows
       # to cope with users selecting the 'Eyes' or 'Donate' checkboxes.   
       global user_defined_frame_width
       global user_defined_frame_height
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

       # Set the geeometry to the default size, so the eyes are displayed properly.
       root.wm_geometry("%dx%d" % (frame_width, frame_height))

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
          self.ClearText.insert(END,EyeTextL)
          self.EncryptedText.insert(END,EyeTextR)
       # Otherwise, we might be here because the box was actively unchecked, and we must set the geometry
       # back to how it was before the box/boxes were checked.
       else:
          #  box is unchecked.. In case the user had a different geometry before checking the box...
          #  we re-instate that geometry.
          if (user_defined_frame_width!=frame_width) or (user_defined_frame_height!=frame_height):
             root.wm_geometry("%dx%d" % (user_defined_frame_width, user_defined_frame_height))

       # After we cleaned up the Text, and restored the geometry..
       # IF we are UNchecking the box... and there is any user-entered text content....
       # restore the user-entered text... 
       # and then clean the buffer, again, only if there is any content. 
       if (self.CheckBoxValueDisplayEyes.get()==0):
          if (user_entered_ClearText!=""):
             # Remove any trailing "\n" newline, because the copy action we performed actually adds a newline!
             if user_entered_ClearText[-1:] == '\n':
                user_entered_ClearText = user_entered_ClearText[:-1]
             self.ClearText.insert(END,user_entered_ClearText)
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
       # Use the 'global' copies of these four variables, otherwise Python will try to make local copies all on its own!
       # We need global-level memory of the user-defined window dimensions and Text content of the windows
       # to cope with users selecting the 'Eyes' or 'Donate' checkboxes.   
       global user_defined_frame_width
       global user_defined_frame_height
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

       # Set the geeometry to the default size, so the QR is displayed properly.
       root.wm_geometry("%dx%d" % (frame_width, frame_height))
       
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
          self.ClearText.insert(END,DonateTextL)
          self.EncryptedText.insert(END,DonateTextR)
       # Otherwise, we might be here because the box was actively unchecked, and we must set the geometry
       # back to how it was before the box/boxes were checked.
       else:
          #  box is unchecked.. In case the user had a different geometry before checking the box...
          #  we reinstate that geometry.
          if (user_defined_frame_width!=frame_width) or (user_defined_frame_height!=frame_height):
             root.wm_geometry("%dx%d" % (user_defined_frame_width, user_defined_frame_height))

       # After we cleaned up and restored the geometry..
       # IF we are UNchecking the box... and there is any user-entered text content....
       # restore the user-entered text... 
       # and then clean the buffer, again, only if there is any content. 
       if (self.CheckBoxValueDisplayDonate.get()==0):
          if (user_entered_ClearText!=""):      
             # Remove any trailing "\n" newline, because the copy action we performed actually adds a newline!
             if user_entered_ClearText[-1:] == '\n':
                user_entered_ClearText = user_entered_ClearText[:-1]
             self.ClearText.insert(END,user_entered_ClearText)
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
      Label(tab1, text= 'ENCRYPTION:\n========\n1. Enter your message in the "Clear Text" window.\n2. Enter a Password (make it long and $tr0nG!, but mostly loooong) \n    -- the generated Key will only be as strong as your Password! \n3. Choose the encryption method (recommended "AES-128 CBC"). \n4. Click on the "ENCRYPT" button. \n\nYou may receive a warning that your text is being "padded".\nIf this happens, your message will have some random characters \nappended at the end which will be visible upon decryption. \nIt might be prudent to warn your intended recpient about this. \n\nGeek notes: \nThe padding is necessary because AES is a "block" cipher, \nwhich operates on blocks of text of a specific size. If your \nmessage is not exactly divisible by the block size, then your \ntext is padded with random characters to make it fit the cipher. \nThe random characters are generated by a cryptographically \nsecure method, (not a PRNG!). It is possible (but not necessary) \nto avoid the need for padding by lengthening your message. \n\nYour encrypted text will consist of hexadecimal digits 0-9,a-f.\n\nIMPORTANT:\n========\nThe new Windows 10 Privacy Statement includes the words: \n"your typed and handwritten words are collected".\n- It is therefore suggested **NOT** to use Win10 with PyEyeCrypt! \n- Consider encrypting on e.g. a Raspberry Pi, and only transfer the \n   Encrypted Text to Win10, if you have to use it.', justify=LEFT).grid()

      Label(tab2, text ='UNDERSTANDING THE ENCRYPTED TEXT:\n========================= \nAfter encryption, the "Encrypted Text" area will contain your encrypted \nmessage, plus some other data which the receipient will need.  \n\nSpecifically, the "Encrypted Text" area contains, in order: \n1. Password Salt, or simply "Salt", \n2. Message Initialisation Vector, "IV" - Only if using "CBC" mode encryption.\n3. The Encrypted Message. \n\nIf you have just encrypted some cleartext, then the Salt and IV will \nbe present at the beginning of the "Encrypted Text". \n\nVERY IMPORTANT:\n============ \n- The "Password" must be kept secret. \n- The "Key" should be DISCARDED and NEVER transmitted or divulged. \n         -- it will be recalculated by the recipient using the Password and Salt.', justify=LEFT).grid()

      Label(tab3, text = 'PASSWORD SALT:\n==========\nIf you just encrypted (or decrypted) some text, the Salt will be visible near \nthe bottom of the Main Window. \n\nThe Salt is transmitted to the recipient in first block of the Encrypted Text. \nIt is randomly generated for each message, and is needed by the recipient \nto turn your agreed Password into a "Key". The Salt should NEVER be \nre-used for a message you wish to keep secure. \n\nGeek notes:\n- It is OK to transmit the Salt unencrypted, since it is ONLY used to deter \n   the use of "rainbow" or "lookup" tables on common* passwords. \n- The use of Salt means that a lookup table would have to be computed \n   for each message. \n- Knowing the Salt DOES NOT help the attacker to deduce your Password. \n- Remember, the generated Key will only be as strong as your Password. \n\nSuper Geek Notes:\n- The Password and Salt are combined using the PBKDF2 function with \n   HMAC SHA256 hashing, and 16,384 iterations (by default) to make the Key. \n- *Rainbow tables exist to crack md5 hashes of ALL POSSIBLE passwords up \n   to 8 characters long (e.g. http://www.freerainbowtables.com/en/tables2/), \n   so in order to prevent computation of lookups (given the Salt), it is \n   imperative to use a tunably slow function like PBKDF2 (or equivalent); \n     - with a good hashing function (e.g. SHA-256), \n     - using a substantial number of iterations (tens of thousands), \n     - including a new, long, cryptographically-random Salt, \n     - and using lo0o0o0ooooong passwords.\n- If you are careful to NEVER re-use a Salt, then any attacker has to recompute \n   rainbow/lookup tables for each message!', justify=LEFT).grid()

      Label (tab4, text = 'Key: \n=== \nIf you just encrypted (or decrypted) some text, the Key will be visible near \nthe bottom of the Main Window (click "Reveal" to see it). \n\nThe Key should NEVER transmitted to the recipient, and should be DISCARDED \nafter each encryption (the recipient only needs the Password and Salt to \ndecrypt; the Key is computed from these). \n\nPBKDF2 Function:\n===========\nThe Key is computed using the Password Based Key Derivation Function2 \n(PBKDF2), which is designed to be tunably slow (higher iterations equals \nslower Key derivation): \n- The cryptographically-random Salt deters the use of rainbow/lookup tables. \n- The tunable slowness of PBKDF2 Key generation using higher iterations \n   deters the use of brute-force or dictionary attacks.  \n\nIn this software, PBKDF2 is set upto use HMAC SHA-256 hashing, the random \nSalt, Password, and 16,384 iterations by default. \n\nThe PBKDF2 iterations can be increased if desired, but the recipient must be \nwarned in advance, otherwise they will not compute the Key correctly, even if \nthey have the Password and Salt!',justify=LEFT).grid()

      Label (tab5, text = 'MESSAGE INITIALISATION VECTOR (IV):\n========================\nIf you just encrypted (or decrypted) some text and an IV is needed, it will \nbe visible near the bottom of the Main Window. \n\n- The IV is transmitted to the recipient in the second block of the \n   encrypted text, immediately following the "Salt". \n- It is a random series of hexadecimal digits created for each message. \n- An IV is generated when encrypting in "CBC" (Cipher Block Chain) mode. \n- IVs should NEVER be re-used on messages you wish to keep secure. \n\nGeek notes:\n- When a block is to be encrypted in CBC-mode, it is first XORed with the \n   previous encrypted block. \n- The IV has the role of the "-1" block (the previous encrypted block for \n   the first block). \n- The main consequence of re-using the IV is that if two messages begin \n   with the same sequence of bytes then the encrypted messages may also \n   be identical for a few blocks, depending on the Key. This leaks data and \n   opens the possibility of some attacks. \n\nFor more explanation on the use of "IV"s, see the Wikipedia entry on \nblock-ciphers: \nhttps://en.wikipedia.org/wiki/Block_cipher_mode_of_operation',justify=LEFT).grid()

      Label(tab6, text = 'DECRYPTION:\n==========\nWith your encrypted message consisting of hexadecimal digits 0-9,a-f in \nthe "Encrypted Text" window; \n- Select the appropriate decrpytion method. \n- Enter the "Password". \n- Click the "DECRYPT" button. \n\nNB: Depending on the length of the original un-encrypted message, your \ndeciphered message may have residual extra characters at the end. This \nis a consequence of padding, which is applied when the message was \noriginally encrypted and the length is not a multiple of the cipher block \nsize.', justify=LEFT).grid()

      Label(tab7, text = 'ENCRYPTION METHODS:\n===============\nIt is currently recommended to use the "AES-128 CBC" cipher. \n- The CBC mode will encrypt identical cleartext blocks into different ciphertext. \n- The ECB mode encrypts identical cleartext blocks into identical ciphertext blocks. \n- More methods are planned to be included! \n\nThere is nothing to stop you encrypting text, and then re-encrypting it using \nanother method. You should consider using "Hex Mode" if encrypting text which is \nalready "Hexified" (i.e contains only characters [0..9, a..f]). \n\nNB: NEVER re-use a Salt, IV, or Key on a message you wish to keep secure.', justify=LEFT).grid()

      Label(tab8, text = 'TESTING ENCRYPTION:\n============== \nIt is possible to test the encryption using Known Answer Test (KAT) Vectors. \n- KAT Vectors are usually published on the web in Hexadecimal notation, so \n   you should click the "Hex Mode" box. \n- Paste the KAT vector you wish to encrypt into the Clear Text window. \n- Next, check the "Enable" box to enter a Key. \n- Paste the Key used for the test into the "Key" row. \n- Click the "Keep" button to stop the software trying to calculate a new Key \n   when you encrypt.\n- If you are testing "CBC" mode, you will need to enter an IV for the KAT test, \n   and check the "Keep" box. \n\nNB: The "Encrypted Text" will have the Salt (and possibly IV) prepended \nbefore the actual encrypted message. As discussed, this presents NO \nsecurity risk to the user. The encrypted KAT vector can be compared to \nresults on the web by ignoring the Salt and IV portions of the Encrypted Text. \n\nNB: Be sure to double-check that the encryption method (e.g. "AES-128 CBC") \nis correct for the test you are performing! \n\n\nTESTING KEY GENERATION:\n================ \nIt is also possible to test that the Password and Salt correctly generate a Key. \n- You will have to look up PBKDF2 HMAC-SHA2 test vectors, and manually \n   enter (and keep) the Password and Salt. \n- The Salt has to be entered in Hexadecimal digits; so please convert any given \n   test Salt into "Hex" format before you enter it  -e.g. if the test Salt is the ASCII \n   string "NaCl", then you should enter "4e61436c" in the "Salt" window. \n- You will also have to override the PBKDF2 iterations to match the test value given. \n- We only keep enough bits of the derived Key to fit the Encryption Method being \n   used (e.g. AES-128 would keep 128 bits of the Key)', justify=LEFT).grid()

      Label(tab9, text = 'PyEyeCrypt (%s)    -    Copyright (C) 2015 "mi55 ing" <mi55ing@protonmail.ch>\n=================================================\nPLEASE REPORT FLAWS, BUGS, OR KNOWN SIDE-CHANNEL ATTACKS TO: \n"mi55 ing" <mi55ing@protonmail.ch> \n\nIt is politely suggested that you check the md5 hash of your downloaded \napplication against the value(s) on the github download page: \nhttps://github.com/mi55ing/PyEyeCrypt. \n- You can do this for the executable by simply typing (in OSX) "md5 PyEyeCrypt.app.tgz". \n- Check the source code by typing: "md5 PyEyeCrypt.py; md5 aes.py; md5 pbkdf2.py". \n\nIt is also suggested to perform encryption/decryption on a computer with (AT LEAST) \nan outbound firewall e.g. TCPBlock. Performing encryption whilst offline can also \nincrease your safety somewhat. \n\nIMPORTANT:\n========\nThe new Windows 10 Privacy Statement includes the words: \n"your typed and handwritten words are collected".\n- It is therefore suggested **NOT** to use Win10 with PyEyeCrypt! \n- Consider encrypting on e.g. a Raspberry Pi, and only transfer the \n   Encrypted Text to Win10, if you have to use it.' % PyEyeCryptVersion, justify=LEFT).grid()


   #####################################################
   # Initialise the main gui window 
   # with initial focus on ClearText window.
   #####################################################
   def __init__(self, master=None):
       Frame.__init__(self, master)
       self.pack()
       self.createWidgets()
       # Start the user on the ClearText Window..
       self.ClearText.focus_force()
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
        # Grab a time() value before frame is created.
        test_time1=time()
        self.entropywin=Toplevel()
        self.entropywin.title("PyEyeCrypt (%s)   -  Copyright (C) 2015:   Entropy (Randomness) Capture" %PyEyeCryptVersion)
        entropyframe=Frame(self.entropywin)
        self.entropywin.wm_geometry("%dx%d%+d%+d" % (5*user_defined_frame_width/8, 100, user_defined_frame_width*3/16, user_defined_frame_height/4)) 
        self.entropywin.grid_columnconfigure(0, weight=1)
        
        Label(entropyframe, text="ENTROPY GATHERING: Please press keys at random time intervals:").grid(row=5, column=5, pady=(10,10), sticky=E+W)
        self.entropyKeyEntryWidget = self.makeentropyentry(entropyframe, 15) 
        self.entropyKeyEntryWidget.grid(row=5,column=6,pady=(10,10), sticky=E+W)
        self.entropyKeyEntryWidget.focus_set()

        self.sessionseedhexdisplay=StringVar()
        self.sessionseedhexdisplay.set("0x")
        self.displayhexvalues = Label(entropyframe, textvariable = self.sessionseedhexdisplay)
        self.displayhexvalues.grid(row=7,column=5,columnspan=2,sticky=W)

        self.bardisplay=StringVar()
        self.bardisplay.set("█")
        self.displayhexvalues = Label(entropyframe, textvariable = self.bardisplay)
        self.displayhexvalues.grid(row=8,column=5, columnspan=2,sticky=W)

        entropyframe.grid()

        # Grab a time() value after frame is created.
        test_time2=time()

        #set up the variables needed later
        start_time = end_time = 0
        self.sessionseed=""

        # determine how many digits are in the timestamp after the decimal point, 
        # and keep up to 6 digits per keypress between positions 3-8 inclusive:
        difftesttime=test_time1-test_time2
        stringydifftesttime=repr(difftesttime)
        difftesttime_digits, difftesttimefract_digits = stringydifftesttime.split('.')
        if len(difftesttimefract_digits) < 9:
           tkMessageBox.showwarning("Error Getting Entropy", "Error Getting Entropy: Time stamp does not have enough digits.." )
           sys.exit()
        self.digitstostartat=2
        self.digitstoendat=8

        def key(event): 
           end_time = time()
           timedifference=end_time-start_time
           stringythingy = repr(timedifference)
           signif_digits, fract_digits = stringythingy.split('.')
           #use zfill to ensure leading zeros for each of the decimal numbers after the first are counted too
           fract_firstdigits = fract_digits[self.digitstostartat:self.digitstoendat].zfill(self.digitstoendat-self.digitstostartat)
           #self.sessionseedtimedisplay.set(str(timedifference)+" , ("+fract_firstdigits+")")
           self.sessionseed=fract_firstdigits+self.sessionseed
           self.sessionseedlong=long(self.sessionseed)
           self.sessionseedhex="%x" % self.sessionseedlong
           self.sessionseedhexdisplay.set("0x"+self.sessionseedhex)
           self.bardisplay.set(self.bardisplay.get().encode("utf8","strict")+"███")
           if len(self.sessionseedhex)*4 >= desiredBits:
              self.entropyKeyEntryWidget.unbind("<Key>")
              self.entropywin.destroy()
        self.entropyKeyEntryWidget.bind("<Key>", key) 
        start_time=time()
        self.entropyKeyEntryWidget.focus_force()
        self.entropywin.grab_set()
        self.entropywin.attributes("-topmost", True)
        self.entropyKeyEntryWidget.wait_window(self.entropywin)

   def makeentropyentry(self,parent,width=None, **options):
        entry = Entry(parent, **options)
        if width:
           entry.config(width=width)
        return entry


######################################################################################
# The main loop here                                                                 #
######################################################################################
root=Tk() 
root.title("PyEyeCrypt (%s)   -  Copyright (C) 2015:   Python-based Open Source GUI text encryption" %PyEyeCryptVersion)

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
for myfontsize in [6,7,8,9,10,11,12,14,16,18]:
   font = tkFont.Font(family='courier', size=myfontsize)
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
for myfontsize in [18,16,14,12,11,10,9,8,7,6]:
   font = tkFont.Font(family='courier', size=myfontsize) 
   (QRwidth,QRheight) = (font.measure("██████████████████████████████████████████████████████████████"),font.metrics("linespace")) 
   if QRwidth < w and QRheight <= h:
      QRlist.append(myfontsize)
# Failing all that, append a tiny font, to make sure there's something in the QRlist!
QRlist.append(2)

# Since this is done in descending order, the largest font which fits will be at the beginning of the list.
bestdonatefontsize=QRlist[0]

if bestdonatefontsize < bestfontsize:
   bestfontsize=bestdonatefontsize

# Set initial geometry of window, and also set the values which the user can override.
frame_width=int(w*2*1.354)
user_defined_frame_width=frame_width
frame_height=int(h*36*1.54)
user_defined_frame_height=frame_height

# Define initial user-entered text content as ""
user_entered_ClearText=""
user_entered_EncryptedText=""

# Needed! - enables us to make a slightly different treatment for displaying 'eyes' on startup.
loopcount=0

# Set up the main window geometry.
root.wm_geometry("%dx%d%+d%+d" % (frame_width,frame_height,0, 0))
#####################################################
# Small diversion from main loop to bring the gui window to the foreground 
# For now, I'll just go with deiconify(),lift(),focus_force(), though this does not work on OSX.
# If we're working on OSX, the focus will not be set on the application.
# we can force it in 10.X Kernel with osascript.
theOS=platform.system()
print "theOS=", theOS
if theOS=="Darwin":
    print "Darwin / OSX, forcing focus may be required..."
    theKernelVersionMajor=os.popen('''uname -r | awk -F '.' '{print $1 "."}' | tr -d '\n' ''').read()
    print "theKernelVersionMajor=",theKernelVersionMajor
    if theKernelVersionMajor=="10.":
        print "Kernel Version is 10.X, using osascript to force focus.."
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
elif theOS=="Windows":
   # Both print and showerror...
   print "==============================================================="
   print "==============================================================="
   print "==============================================================="
   print "Detected Windows >>>  Exiting,  Sorry!"
   print ""
   print "The new Windows 10 Privacy Statement includes the words:"
   print "'your typed and handwritten words are collected'"
   print ""
   print "This means that passwords typed by a single recipient using"
   print "Win10 would, *unknown to the sender*, jeopardise the sender's"
   print "password!"
   print ""
   print "This behaviour is akin to a keylogging virus."
   print "It is therefore NOT suitable to use Win10 with PyEyeCrypt!"
   print "==============================================================="
   print "==============================================================="
   print "==============================================================="
   tkMessageBox.showerror("Error", "Detected Windows >>>  Exiting,  Sorry! \n\nThe new Windows 10 Privacy Statement includes the words:\n'your typed and handwritten words are collected' \n\nTHINK VERY CAREFULLY before you subvert this check. This means that passwords typed by a single recipient using Win10 would, *unknown to the sender*, expose the sender's password and text! \n\nThis behaviour is akin to a keylogging virus. It is therefore NOT suitable to use Win10 with PyEyeCrypt!")
   sys.exit()
else:
   root.deiconify()
   root.lift()
# END Small diversion from main loop to bring gui window to foreground
#####################################################


# Get some entropy from the Keyboard, to use as a seed for 
# the Pseudo Random Number Generator (PRNG).
# Note: we will ONLY ever use PRNG in XOR with "os.urandom"  
desiredEntropyBits=256
initialEntropyWindow=EntropyWindow(desiredEntropyBits)

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
