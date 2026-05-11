password = input('')
char = list(password) 
#for i in range(len(char)):
 #   ky_tu = char[i]
  #  if ky_tu in [0,1,2,3,4,5,6,7,8,9]:
   #     print('co digit')

for i in char:
    if i in '0123456789':    
        print('co digit')
        break
    elif char[-1] not in '0123456789':    
        print('ko digit')
        break
print('done')



