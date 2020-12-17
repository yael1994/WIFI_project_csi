import array
import sys
import os
import numpy as np
from datetime import datetime


def fromfileskip(file_name,size,precision,skip=0,dtype='little'):
    dic={
        'uint8':1,
        'uint16':2,
        'uint32':4,
        'uint64':8}
    #f   : file ,Should be open binary file.
    #size  : size array for output
    #precision : int, number of bytes to read
    #skip   : int, Number of bytes to skip between reads.
    #dtype  : np.dtype object, Type of each binary element.
    if size==1:
        byte=file_name.read(dic[precision])
        data=int.from_bytes(byte,byteorder=dtype) 
        if skip!=0:
            file_name.seek( file_name.tell() + skip)      
    else:
        data=[]
        for index in range(size):
            byte=file_name.read(dic[precision])
            data.append(int.from_bytes(byte,byteorder=dtype))       
            if skip!=0:
                file_name.seek( file_name.tell() + skip)          
    return data
    


def read_log_file(file_name):
    try:
        f=open(file_name,'rb')
    except:
        print('couldn''t open file '+ filename)
    len_file=os.path.getsize(file_name)
    print('file lenght is: '+str(len_file))

     #empty array size 420/len_file 
    ret=['None']*round(len_file/420)
    cur=0
    count=0  

    endian_format ='big'
    path='output_new/'
    while cur<(len_file-4):
        path_new=path+'num_'+str(count)
        os.mkdir(path_new)
        try:
            file_print= open(path_new+'/output.csv','w')
        except:
            print('cant open file: output.csv')
        
        
        file_print.write('count is:%d\n' % (count))

        field_len=fromfileskip(f,1,'uint16',0,endian_format) #unit16 - 2 bytes
        cur+=2
        file_print.write('Block length is:%d\n' % (field_len))
        if (cur+field_len)>len_file:
            break

        timestamp = fromfileskip(f, 1, 'uint64', 0, endian_format)
        cur+=8
        file_print.write('before -timestamp is %s\n' % (timestamp))
        #change timestamp for unix time
        #timestamp = datetime.fromtimestamp(timestamp)
        #file_print.write('timestamp is %s\n' % (timestamp))

        csi_len = fromfileskip(f, 1, 'uint16', 0, endian_format)
        cur+=2
        file_print.write('csi_len is %d\n' % (csi_len))

        tx_channel = fromfileskip(f, 1, 'uint16', 0, endian_format)
        cur+=2
        file_print.write('tx_channel is %d\n' % (tx_channel))
        
        err_info = fromfileskip(f, 1,'uint8')
        file_print.write('err_info is %d\n' % (err_info))
        cur+=1

        noise_floor = fromfileskip(f, 1, 'uint8')
        cur+=1
        file_print.write('noise_floor is %d\n' % (noise_floor))

        Rate = fromfileskip(f, 1, 'uint8')
        cur+=1
        file_print.write('rate is %x\n' % (Rate))

        bandWidth = fromfileskip(f, 1, 'uint8')
        cur+=1
        file_print.write('bandWidth is %d\n' % (bandWidth))

        num_tones = fromfileskip(f, 1, 'uint8')
        cur+=1
        file_print.write('num_tones is %d\n' % (num_tones))

        nr = fromfileskip(f, 1, 'uint8')
        cur+=1
        file_print.write('nr is %d\n' % (nr))

        nc = fromfileskip(f, 1, 'uint8')
        cur+=1
        file_print.write('nc is %d\n' % (nc))
	
        rssi = fromfileskip(f, 1, 'uint8')
        cur+=1
        file_print.write('rssi is %d\n' % (rssi))

        rssi1 = fromfileskip(f, 1, 'uint8')
        cur+=1
        file_print.write('rssi1 is %d\n' % (rssi1))

        rssi2 = fromfileskip(f, 1, 'uint8')
        cur+=1
        file_print.write('rssi2 is %d\n' % (rssi2))

        rssi3 = fromfileskip(f, 1, 'uint8')
        cur+=1
        file_print.write('rssi3 is %d\n' % (rssi3))

        payload_len = fromfileskip(f, 1, 'uint16', 0, endian_format)
        cur+=2
        file_print.write('payload length: %d\n' % (payload_len))	
        

        if csi_len > 0:
            csi_buf = fromfileskip(f, csi_len, 'uint8')
            #TODO:call the c file
            csi = read_csi(csi_buf, nr, nc, num_tones)
            with open(path_new+'/csifile.txt', 'w') as filehandle:
                for listitem in csi:
                    filehandle.write('%d\n' % listitem)
            filehandle.close()        
            cur = cur + csi_len
        else:
            csi = 0
               
        if payload_len > 0:
            payload = fromfileskip(f, payload_len, 'uint8')  
            with open(path_new+'/payloadfile.txt', 'w') as filehandle:
                for listitem in payload:
                    filehandle.write('%d\n' % listitem)
            filehandle.close()        
            cur = cur + payload_len
        else:
            payload = 0
        
        if (cur + 420 > len_file):
             break
        count = count + 1   
        file_print.close() 

    f.close()

if __name__ == "__main__":
    read_log_file(sys.argv[1])