

class Diffi():
    # sharedPrime=23    
    # sharedBase=5 
    
    def __init__(self):
        pass

    def diffi_KeySEND(self, SecretKey):
        global sharedPrime    
        global sharedBase    
  
        sharedPrime=23    
        sharedBase=5
        Exchange = (sharedBase**SecretKey)%sharedPrime
        return Exchange

    def diffi_KeyGET(self, SecretKey, Exchange):

        Key = (Exchange**SecretKey)%sharedPrime
        return Key


class Enc_Dec():

    def __init__(self):
        pass

    def encrypt(self, string, key):
        print(key)
        cipher =""
        for char in string: 
            if char == ' ':
                cipher = cipher + char
            elif  char.isupper():
                cipher = cipher + chr((ord(char) + key - 65) % 26 + 65)
            else:
                cipher = cipher + chr((ord(char) + key - 97) % 26 + 97)    
        return cipher
    
    def decrypt(self,string, shift):
        
        cipher = ''
        for char in string: 
            if char == ' ':
                cipher = cipher + char
            elif  char.isupper():
                cipher = cipher + chr((ord(char) - shift - 65) % 26 + 65)
            else:
                cipher = cipher + chr((ord(char) - shift - 97) % 26 + 97)
        return cipher


 

