import sys
import re
import pandas as pd
import random
import string

def rand_fix_len(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)

def randomString(stringLength):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def encrypt_file(filename):
  FName_dict = {}
  LName_dict = {}
  Add_dict   = {}
  City_dict  = {}
  Org_dict   = {}
  num_dict   = {}
  
  final_list = []
  f_Sample = open(filename,'r')
  text = f_Sample.readlines()
  
  Dummy_FNames_df=pd.read_excel(r'C:\Users\rahuljoshi\Documents\Machine Learning\EDIMasking\EDI Mask\First Name Table.xlsx')
  Dummy_LNames_df=pd.read_excel(r'C:\Users\rahuljoshi\Documents\Machine Learning\EDIMasking\EDI Mask\Last Name Table.xlsx')
  Dummy_Add_df=pd.read_excel(r'C:\Users\rahuljoshi\Documents\Machine Learning\EDIMasking\EDI Mask\Address Table.xlsx')
  Dummy_City_df=pd.read_excel(r'C:\Users\rahuljoshi\Documents\Machine Learning\EDIMasking\EDI Mask\City Table.xlsx')
  Dummy_Org_df=pd.read_excel(r'C:\Users\rahuljoshi\Documents\Machine Learning\EDIMasking\EDI Mask\Organization Table.xlsx')
  
  for t in text:
        print(t)
        # Replace First Name
        #FName = re.search(r'(NM1\*[\w\d]+\*\d\*[\w]+\*)([\w]+)(.+)',t)
        FName = re.search(r'(NM1\*[\w\d]+\*\d\*)([\w]+)\*([\w]+)([\*\w]*)\*([\d\w]+)(.+)',t)
        Addrs = re.search(r'N3\*([\w\s\d\.\*]+)(.+)',t)
        City  = re.search(r'N4\*([\w\s]+)\*AZ\*(\d+).+',t)
       # Org   = re.search(r'(NM1\*[\w\d]+\*\d\*)([\w\s]+)\*(.+)',t)
        Org   = re.search(r'(NM1\*[\w\d]+\*\d\*)([\w\s]+)(\**)([\d\w]+\*)(\d+)(.+)',t)
        Spl_ID= re.search(r'DMG\*D8\*(\d+).*',t)
        #REF*D9*18291892~

        Spl_ID2= re.search(r'REF\*[\w\d]+\*(\d+).*',t)
        
        
        """
        if FName:
            repl = Dummy_FNames_df.iat[random.randint(0,int(Dummy_FNames_df.count())),0]
            FName = re.sub(r'(NM1\*[\w\d]+\*\d\*[\w]+\*)([\w]+)(.+)',r'\1'+repl+r'\3',t)
            t = FName
            
        # Replace Last Name    
            repl = Dummy_LNames_df.iat[random.randint(0,int(Dummy_LNames_df.count())),0]
            LName = re.sub(r'(NM1\*[\w\d]+\*\d\*)([\w]+)(.+)',r'\1'+repl+r'\3',t)
            final_list.append(LName)            
            t = LName
            
            NM1_zip = re.search(r'(NM1\*[\w\d]+\*\d\*[\w]+\*)([\w]+)(.+)',t)
        # Replace Address    
        """
        if FName:
            Orig_FName = FName.group(3)
            Orig_LName = FName.group(2)  
            Orig_num   =  FName.group(5)
            
            if Orig_FName.casefold() in FName_dict:
                repl_FName = FName_dict[Orig_FName.casefold()]
            else:
                repl_FName = Dummy_FNames_df.iat[random.randint(0,int(Dummy_FNames_df.count())-1),0]
                FName_dict[Orig_FName.casefold()] = repl_FName
                
            if Orig_LName.casefold() in LName_dict:
                repl_LName = LName_dict[Orig_LName.casefold()]
            else:
                repl_LName = Dummy_LNames_df.iat[random.randint(0,int(Dummy_LNames_df.count())-1),0]   
                LName_dict[Orig_LName.casefold()] = repl_LName       
                
            if Orig_num.casefold() in num_dict:
                repl_num = num_dict[Orig_num.casefold()]
            else:
                len_Orig_num = len(Orig_num)
                repl_num = str(rand_fix_len(len_Orig_num))
                num_dict[Orig_num.casefold()] = repl_num
                
            encrpt_Names = re.sub(r'(NM1\*[\w\d]+\*\d\*)([\w]+)\*([\w]+)(.+)',r'\1'+ repl_LName + r'*'+ repl_FName +r'\4' ,t)
            
            final_list.append(encrpt_Names)
            t = encrpt_Names
            
        # Replace Address    
        elif Addrs:
            Orig_Add = Addrs.group(1)
            
            if Orig_Add in Add_dict:
                repl_Add = Add_dict[Orig_Add]
            else:
                repl_Add = Dummy_Add_df.iat[random.randint(0,int(Dummy_Add_df.count())-1),0]
                Add_dict[Orig_Add] = repl_Add
                
            Addrs = re.sub(r'N3\*([\w\d\s\.\*]+)(.+)',r'N3*'+repl_Add+r'\2',t)
            final_list.append(Addrs)            
            t = Addrs    

        # Replace City    
        
        elif City:
            Orig_City = City.group(1)
            Orig_num  = City.group(2)

            Orig_num_123 = Orig_num[:3]
            Orig_num_4   = Orig_num[3:]
            
           
            if Orig_City in City_dict:
                repl_City = City_dict[Orig_City]
            else:
                repl_City = Dummy_City_df.iat[random.randint(0,int(Dummy_City_df.count())-1),0]
                City_dict[Orig_City] = repl_City
               
            if Orig_num_4 in num_dict:
                repl_num = num_dict[Orig_num_4]
            else:
                len_Orig_num = len(Orig_num_4)
                repl_num = str(rand_fix_len(len_Orig_num))
                num_dict[Orig_num_4] = repl_num

            
            City  = re.sub(r'N4\*([\w\s]+)\*AZ\*(\d+)(.+)',r'N4*'+repl_City+r'*AZ*'+Orig_num_123+repl_num+r'\3',t)
            final_list.append(City)            
            t = City          
            
        # Replace Org

        elif Org:
            Orig_Org = Org.group(2)
            Orig_num = Org.group(5)

            if Orig_Org in Org_dict:
                repl_Org = Org_dict[Orig_Org]
            else: 
                repl_Org = Dummy_Org_df.iat[random.randint(0,int(Dummy_Org_df.count())),0]
                Org_dict[Orig_Org] = repl_Org

            if Orig_num in num_dict:
                repl_num = num_dict[Orig_num]
            else:
                len_Orig_num = len(Orig_num)
                repl_num = str(rand_fix_len(len_Orig_num))
                num_dict[Orig_num] = repl_num    
                
            Org = re.sub(r'(NM1\*[\w\d]+\*\d\*)([\w\s]+)(.+)',r'\1'+ repl_Org + r'\3',t)
            final_list.append(Org)            
            t = Org      
            
        # Replace Special ID

        elif Spl_ID:
            Orig_num = Spl_ID.group(1)
            Orig_num_YM = Orig_num[:6]
            Orig_num_D  = Orig_num[6:]
                        
            if Orig_num_D in num_dict:
                repl_num = num_dict[Orig_num_D]
            else:
                len_Orig_num = len(Orig_num_D)
                repl_num = str(random.randint(10,30))
                num_dict[Orig_num_D] = repl_num    
                
            Spl_ID = re.sub(r'(DMG\*D8)\*(\d+)(.*)',r'\1*'+Orig_num_YM+ repl_num + r'\3',t)
            final_list.append(Spl_ID)            
            t = Spl_ID    
         
        # Replace Special ID 2

        elif Spl_ID2:
            Orig_num = Spl_ID2.group(1)
            
            if Orig_num in num_dict:
                repl_num = num_dict[Orig_num]
            else:
                len_Orig_num = len(Orig_num)
                repl_num = str(rand_fix_len(len_Orig_num))
                num_dict[Orig_num] = repl_num    
                
            Spl_ID2 = re.sub(r'(REF\*[\w\d]+)\*(\d+)(.*)',r'\1*'+ repl_num + r'\3',t)
            final_list.append(Spl_ID2)            
            t = Spl_ID2    
        else:
            final_list.append(t)
        print(t)
            
  return(final_list)
  
 
def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print('usage: [--maskfile] file')
    sys.exit(1)

  # Notice the Mask flag and remove it from args if it is present.
  mask = False
  if args[0] == '--maskfile':
    mask = True
    del args[0]

  for filename in args:
    names = encrypt_file(filename)
  
  print(names)
  mask_data = ''.join(names)
  new_file = filename[0:len(filename)-4]

  if mask:
        ofile = open(new_file + '_encrypt.edi','w+')
        ofile.write(mask_data) 
  else:
        print(mask_data)
      
  
if __name__ == '__main__':
  main()


"""
        elif Org:
            repl = Dummy_Org_df.iat[random.randint(0,int(Dummy_Org_df.count())),0]
            Org = re.sub(r'(NM1\*[\w\d]+\*\d\*)([\w\s]+)(.+)',r'\1'+repl+r'\3',t)
            final_list.append(Org)            
            t = Org          
"""   