from flatten_json import flatten
def normalize(a):
    if not type(a) is list:
        return a
     
    ione=0
    eleOne=[]
    for ele in a:
        if type(ele) is list and len(ele)==1:
            ione+=1
            eleOne.append(ele[0])
    if ione!=len(a):
        return a
    else:
        return eleOne
    
def myFunc(e):
  return e['id']

def colsAreEqual(a,b):
    if len(b)==0:
        return len(a)==0
    aso=normalize(a)
    bso=normalize(b)
    
    if type(b[0]) is list:
       return False
    
    if type(a[0]) is list:
        return False
    
    if type(bso[0]) is dict:
        if not type(aso[0]) is dict:
            return False
        elif 'id' in bso[0].keys():
            if 'id' in aso[0].keys():
                aso.sort(key=myFunc)
                bso.sort(key=myFunc)
            else:
                for asokey in aso[0].keys():
                    if asokey.lower().endswith("id") or asokey.lower().startswith("id"):
                        def myFunc2(e):
                            return e[asokey]
                        aso.sort(key=myFunc2)
                        bso.sort(key=myFunc)
    else:    
        aso.sort()
        bso.sort()

    for irow in range(len(bso)):
        ae=aso[irow]
        be=bso[irow]
        #pprint(ae)
        #pprint(be)
        if not compareToRef(ae,be):
            return False
    return True


def correctArrayInArray(myarray):
    if type(myarray) is list:
        #print('GGG\n')
        #print(myarray)
        #print(len(myarray))
        #print('\n')
        if len(myarray)==1:
            #print('ZZZ')
            if type(myarray[0]) is list:
                #print(myarray[0])
                return myarray[0]
    return myarray

def get_equi_key(a:dict,rke:str):
    if rke in a:
        return rke
    else:
        for kea in a:
            if kea.lower().startswith(rke) or kea.lower().endswith(rke):
                return kea
        nfound=0
        keyfound=''
        for kea in a:
            if rke in kea.lower():
                keyfound=kea
                nfound=nfound+1
        if nfound==1:
            return keyfound
    return None

def isFlatDict(a: dict):
    if not type(a) is dict:
        return False
    for rkey in a.keys():
        valref=a[rkey]
        if type(valref) is dict:
            return False
        if type(valref) is list:
            return False
    return True

def objectsAreEqualFlat(a: dict,ref: dict):
    if not type(ref) is dict:
        return False
    if not type(a) is dict:
        return False
    if not isFlatDict(ref):
        return False
    a_flat=flatten(a)
    for rkey in ref.keys():
        akey_corr=get_equi_key(a_flat,rkey)
        if akey_corr == None:
            #print(rkey)
            return False
        #print('KEY: '+akey_corr+', REF KEY: '+rkey)
        vala=a_flat[akey_corr]
        valref=ref[rkey]
        #print('V'+str(vala)+', VREF '+str(valref))
        if not compareToRef(vala,valref):
            #print('V'+str(vala)+', VREF '+str(valref))
            return False
    return True

def objectsAreEqualNonFlat(a: dict,ref: dict):
    for rkey in ref.keys():
        akey_corr=get_equi_key(a,rkey)
        if akey_corr == None:
            #print(rkey)
            return False
        #print('KEY: '+akey_corr+', REF KEY: '+rkey)
        vala=a[akey_corr]
        valref=ref[rkey]
        #print('V'+str(vala)+', VREF '+str(valref))
        if not compareToRef(vala,valref):
            #print('V'+str(vala)+', VREF '+str(valref))
            return False
    return True

def objectsAreEqual(a: dict,ref: dict):
    if isFlatDict(ref):
        return objectsAreEqualFlat(a,ref)
    else:
        return objectsAreEqualNonFlat(a,ref)
    
def extractCols(array):
    if not type(array)==list:
        return None
    if len(array)==0:
        return []
    if type(array[0])==dict:
        keys=[]
        values=[]        
        for key in array[0]:
          keys.append(key)
          vals=[]
          for i in range(0,len(array)):
              vals.append(array[i][key])
          values.append(vals)
        return values
    return None

def compare_multi_cols(values,ref):
  if not type(values)==list:
    return False
  if not type(ref)==list:
    return False
  #print(values)
  if values==None:
    return False
  for colval in values:
    #print(colval)
    if colsAreEqual(colval,ref):
        return True
  return False

def compareToRef(ao: any, refo: any):
    if type(refo) is list:
         if not type(ao) is list:
              #print(refo)
              #print(len(refo))
              if len(refo)==0:
                if ao == None:
                   return True 
              if len(refo)==1:
                  if type(ao)==type(refo[0]):
                      return compareToRef(ao,refo[0])

              #print(type(ao))
              #print("No List: "+str(ao))
              return False
         else:
            refo2=correctArrayInArray(refo)
            ao2=correctArrayInArray(ao)
            if len(ao2) !=  len(refo2):
                #print("Different length: Mo:"+str(len(ao2)) +', Ref: ' + str(len(refo2)) )
                return False
            else:
                if len(refo2)>0 and type(refo2[0]) != dict and type(ao2[0])==dict:
                    #print('llll')
                    cvalues=extractCols(ao2)
                    if cvalues!=None:
                        return compare_multi_cols(cvalues,refo2)          
                return colsAreEqual(ao2,refo2)
    elif type(refo) is dict:
        if not type(ao) is dict:
              if type(ao) is list and len(ao)==1:
                  return objectsAreEqual(ao[0],refo)     
              #print("No dict"+str(ao))
              return False
        else:
             #print("obj")
             return objectsAreEqual(ao,refo)
    else:
        if type(ao) != type(refo):
              if type(ao) is dict:
                  for aokey in ao.keys():
                      aovalue=ao[aokey]
                      if type(aovalue)==type(refo):
                        if aovalue==refo:
                            return True
                      else:
                            if type(aovalue) is list and len(aovalue)==1 and type(aovalue[0])==type(refo) and aovalue[0]==refo:
                                #print("Found in dict: "+str(aovalue))
                                return True
              elif type(ao) is list and len(ao)==1:
                  #print("list of one: "+str(ao[0]))
                  if type(ao[0])==type(refo):
                      if ao[0]==refo:
                          return True
                                
              #pprint(ao)
              #pprint(refo)          
              return False
        else:
            #print('ääää')
            return ao==refo
        

def findValue(rkey,ao):
    for key in ao:
        if rkey in key:
            return ao[key]
    return None

def compareGroupToRef(ao: any, refo: any):
    if not type(ao) is dict:
       return False
    if not type(refo) is dict:
       return False
    
    for rkey in refo:
        vref=refo[rkey]
        vao=findValue(rkey,ao)
        if vao == None:
            return False
        isEqual=compareToRef(vao,vref)
        if not isEqual:
            return False
    return True        

def testCompareToRef():
    a1=['Port James']
    aref='Port James'
    copo=compareToRef(a1,aref)
    if copo != True:
        return False
    
    a1=[{'employeeId': 'E00001', 'employeeName': 'Shannon Curtis', 'skillsCount': {'primary': 1, 'secondary': 2, 'domains': 2, 'certifications': 3, 'total': 8}}]
    aref=[{'id': 'E00001', 'name': 'Shannon Curtis', 'skills': 3}]
    copo=compareToRef(a1,aref)
    if copo == True:
        return False
    a1=[{'employeeId': 'E00002', 'employeeName': 'Tommy Parker'}]
    r1=[{'id': 'E00002', 'name': 'Tommy Parker'}]
    copo=compareToRef(a1,r1)
    if copo != True:
        return False
    a1={"domain": "E-commerce", "count": 73}
    aref="E-commerce"
    copo=compareToRef(a1,aref)
    if copo != True:
        return False
    a1={"employeeId": "E00001", "employeeName": "Shannon Curtis"}
    aref={"id":'E00001',"name":"Shannon Curtis"}
    copo=compareToRef(a1,aref)
    if copo != True:
        return False
    a1=[{'employeeId': 'E00002', 'employeeName': 'Tommy Parker'}]
    r1=[{'id': 'E00002', 'name': 'Tommy Parker'}]
    copo=compareToRef(a1,r1)
    if copo != True:
        return False
    a1={'mostCommonDomains': ['E-commerce'], 'frequency': 73}
    aref='E-commerce'
    copo=compareToRef(a1,aref)
    if copo != True:
        return False
    # L
    a1=[{'employeeId': 'E00001', 'employeeName': 'Shannon Curtis', 'skillsCount': {'primary': 1, 'secondary': 2, 'domains': 2, 'certifications': 3, 'total': 8}}]
    aref=[{'id': 'E00001', 'name': 'Shannon Curtis', 'skills': 3}]
    copo=compareToRef(a1,aref)
    if copo == True:
        return False
    a1=[{'id': 'E00001', 'name': 'Shannon Curtis'}]
    aref={'id': 'E00001', 'name': 'Shannon Curtis'}
    copo=compareToRef(a1,aref)
    if copo != True:
        return False
    a1={'city': 'North Ann', 'location': {'country': 'USA', 'geo': {'lat': '-0.5213', 'long': '69.7529', 'timezone': {'name': 'America/Denver', 'utc_offset': '-07:00'}}, 'state': 'TX'}, 'street': '597 Mark Centers'}
    aref=[{'street': '597 Mark Centers', 'city': 'North Ann'}]
    copo=compareToRef(a1,aref)
    if copo != True:
        return False
    
    a1=[{'id': 'E00001', 'name': 'Shannon Curtis', 'email': 'robert91@example.com'}, {'id': 'E00002', 'name': 'Tommy Parker', 'email': 'arnoldtheresa@example.com'}, {'id': 'E00003', 'name': 'Benjamin Archer', 'email': 'burnsmark@example.com'}, {'id': 'E00004', 'name': 'Donna Reilly', 'email': 'mark31@example.org'}, {'id': 'E00005', 'name': 'Amy Wilson', 'email': 'cwiley@example.org'}, {'id': 'E00006', 'name': 'Eileen Fitzgerald', 'email': 'uthomas@example.net'}, {'id': 'E00007', 'name': 'Luke Soto', 'email': 'ericwilliams@example.org'}, {'id': 'E00008', 'name': 'Carolyn Cruz', 'email': 'joshuacrawford@example.org'}, {'id': 'E00009', 'name': 'Ashley Arroyo', 'email': 'brittanybrown@example.net'}, {'id': 'E00010', 'name': 'Blake Mitchell', 'email': 'johnsummers@example.org'}, {'id': 'E00011', 'name': 'Jacob Cook', 'email': 'schmidtandrea@example.org'}, {'id': 'E00012', 'name': 'Thomas Santiago', 'email': 'apeters@example.com'}, {'id': 'E00013', 'name': 'Christopher Thompson', 'email': 'crystalalvarez@example.net'}, {'id': 'E00014', 'name': 'Stephanie Lewis', 'email': 'jhernandez@example.net'}, {'id': 'E00015', 'name': 'Stephanie Fernandez', 'email': 'eugenemendoza@example.net'}, {'id': 'E00016', 'name': 'Garrett Martin', 'email': 'kflores@example.org'}, {'id': 'E00017', 'name': 'Ryan Decker', 'email': 'bmorales@example.net'}, {'id': 'E00018', 'name': 'Christopher Martin', 'email': 'isabel45@example.net'}, {'id': 'E00019', 'name': 'Chris Thomas', 'email': 'kevin62@example.org'}, {'id': 'E00020', 'name': 'Kayla Harrington', 'email': 'jmcdonald@example.net'}, {'id': 'E00021', 'name': 'Julie Patterson', 'email': 'fli@example.net'}, {'id': 'E00022', 'name': 'Brittany Daniels', 'email': 'georgegeorge@example.net'}, {'id': 'E00023', 'name': 'Brenda Wang', 'email': 'hharper@example.org'}, {'id': 'E00024', 'name': 'David Taylor', 'email': 'cynthiapowell@example.org'}, {'id': 'E00025', 'name': 'Kristin Rose', 'email': 'taylorkelly@example.com'}, {'id': 'E00026', 'name': 'Sherry Yates', 'email': 'valeriecannon@example.net'}, {'id': 'E00027', 'name': 'Anthony Jefferson', 'email': 'wallstephanie@example.com'}, {'id': 'E00028', 'name': 'Toni Sanchez', 'email': 'james58@example.com'}, {'id': 'E00029', 'name': 'Sherry Henson', 'email': 'josephshort@example.net'}, {'id': 'E00030', 'name': 'Deborah Paul', 'email': 'sheltonelizabeth@example.org'}, {'id': 'E00031', 'name': 'Brett Guzman', 'email': 'sarablake@example.com'}, {'id': 'E00032', 'name': 'Jennifer Logan', 'email': 'rhudson@example.org'}, {'id': 'E00033', 'name': 'Jasmine Sutton', 'email': 'evanstimothy@example.com'}, {'id': 'E00034', 'name': 'Mrs. Tammy Cooper', 'email': 'fosterpatricia@example.com'}, {'id': 'E00035', 'name': 'David Smith', 'email': 'christopher88@example.org'}, {'id': 'E00036', 'name': 'Cheryl Lee', 'email': 'haleyjames@example.org'}, {'id': 'E00037', 'name': 'Patrick Lee', 'email': 'tammy61@example.net'}, {'id': 'E00038', 'name': 'Jim Werner', 'email': 'sharonparsons@example.net'}, {'id': 'E00039', 'name': 'Adrian Berry', 'email': 'justin30@example.com'}, {'id': 'E00040', 'name': 'Melissa Simmons', 'email': 'ivincent@example.net'}, {'id': 'E00041', 'name': 'Joanna Myers', 'email': 'hectormorris@example.net'}, {'id': 'E00042', 'name': 'Holly Hill', 'email': 'christopherburns@example.org'}, {'id': 'E00043', 'name': 'Tanner Bauer', 'email': 'kristin30@example.net'}, {'id': 'E00044', 'name': 'Jason Powell', 'email': 'john41@example.com'}, {'id': 'E00045', 'name': 'Valerie Rosales', 'email': 'shirleywalters@example.org'}, {'id': 'E00046', 'name': 'Amy Huerta', 'email': 'johnsonanthony@example.com'}, {'id': 'E00047', 'name': 'Abigail Briggs', 'email': 'ruizmichele@example.com'}, {'id': 'E00048', 'name': 'Sarah Moore', 'email': 'josephfitzgerald@example.org'}, {'id': 'E00049', 'name': 'Cathy Oconnor', 'email': 'ecarter@example.com'}, {'id': 'E00050', 'name': 'Ricky Perry', 'email': 'qjones@example.net'}, {'id': 'E00051', 'name': 'Michelle Petty', 'email': 'crystalgray@example.net'}, {'id': 'E00052', 'name': 'Morgan Wolfe', 'email': 'christopher77@example.com'}, {'id': 'E00053', 'name': 'Billy Bradley DVM', 'email': 'cruzkristine@example.com'}, {'id': 'E00054', 'name': 'Isaiah Gonzalez', 'email': 'joel18@example.org'}, {'id': 'E00055', 'name': 'Rachel Jackson', 'email': 'danielle00@example.net'}, {'id': 'E00056', 'name': 'Matthew Caldwell', 'email': 'kjames@example.com'}, {'id': 'E00057', 'name': 'Jeffrey Johnson', 'email': 'andrew43@example.com'}, {'id': 'E00058', 'name': 'Terry Elliott', 'email': 'jerry07@example.net'}, {'id': 'E00059', 'name': 'James Ellis', 'email': 'qaustin@example.org'}, {'id': 'E00060', 'name': 'Justin Smith', 'email': 'andersonpatrick@example.org'}, {'id': 'E00061', 'name': 'Barbara Coleman', 'email': 'jay56@example.org'}, {'id': 'E00062', 'name': 'Stacie Silva', 'email': 'edwardsjoel@example.com'}, {'id': 'E00063', 'name': 'David Jackson', 'email': 'phillipellis@example.com'}, {'id': 'E00064', 'name': 'Miss Connie Levy', 'email': 'lnorman@example.net'}, {'id': 'E00065', 'name': 'Rhonda King', 'email': 'morgangeorge@example.net'}, {'id': 'E00066', 'name': 'Christopher Evans', 'email': 'farleymark@example.org'}, {'id': 'E00067', 'name': 'Phillip Parrish', 'email': 'wendyanthony@example.net'}, {'id': 'E00068', 'name': 'Robert Kelley', 'email': 'deborahbrown@example.org'}, {'id': 'E00069', 'name': 'Jesse Chapman', 'email': 'bradleyduncan@example.net'}, {'id': 'E00070', 'name': 'Carol Briggs', 'email': 'john01@example.net'}, {'id': 'E00071', 'name': 'Jeffrey Cruz', 'email': 'sean57@example.net'}, {'id': 'E00072', 'name': 'Alexander Guerrero IV', 'email': 'alex97@example.org'}, {'id': 'E00073', 'name': 'Sara Williams DDS', 'email': 'vowens@example.org'}, {'id': 'E00074', 'name': 'Darlene Allen', 'email': 'hannah58@example.org'}, {'id': 'E00075', 'name': 'Jessica Guzman', 'email': 'alexanderchristopher@example.org'}, {'id': 'E00076', 'name': 'Stephanie Collier', 'email': 'richardbarnes@example.com'}, {'id': 'E00077', 'name': 'Sandra Davis', 'email': 'johnduncan@example.net'}, {'id': 'E00078', 'name': 'James Garza', 'email': 'marshalldustin@example.net'}, {'id': 'E00079', 'name': 'James Smith', 'email': 'allentyler@example.com'}, {'id': 'E00080', 'name': 'Nichole Rios', 'email': 'iadams@example.org'}, {'id': 'E00081', 'name': 'Ashley Miller', 'email': 'fweber@example.com'}, {'id': 'E00082', 'name': 'Daniel Mueller', 'email': 'mcdowelljeremy@example.org'}, {'id': 'E00083', 'name': 'William Pierce', 'email': 'henglish@example.org'}, {'id': 'E00084', 'name': 'Hannah Farley', 'email': 'michellelester@example.net'}, {'id': 'E00085', 'name': 'Emily Riddle', 'email': 'dcook@example.org'}, {'id': 'E00086', 'name': 'Stephanie Smith', 'email': 'kari58@example.org'}, {'id': 'E00087', 'name': 'Rebecca King', 'email': 'julian32@example.net'}, {'id': 'E00088', 'name': 'Cheryl Scott', 'email': 'montgomeryalyssa@example.com'}, {'id': 'E00089', 'name': 'Stephanie Farmer', 'email': 'finleyjason@example.org'}, {'id': 'E00090', 'name': 'Anthony Whitehead', 'email': 'dwood@example.com'}, {'id': 'E00091', 'name': 'Edward Jenkins', 'email': 'gallaghercharles@example.com'}, {'id': 'E00092', 'name': 'Christopher Alvarado', 'email': 'uhall@example.net'}, {'id': 'E00093', 'name': 'Jessica Clay', 'email': 'fgarrett@example.org'}, {'id': 'E00094', 'name': 'Olivia Cervantes', 'email': 'john63@example.net'}, {'id': 'E00095', 'name': 'Matthew Henderson', 'email': 'joseph26@example.com'}, {'id': 'E00096', 'name': 'Colleen Poole', 'email': 'jodi20@example.org'}, {'id': 'E00097', 'name': 'Tonya Wang', 'email': 'johnsonjeanette@example.net'}, {'id': 'E00098', 'name': 'Holly Burke', 'email': 'jason10@example.org'}, {'id': 'E00099', 'name': 'Michael Perry', 'email': 'charlesfox@example.com'}, {'id': 'E00100', 'name': 'Tony Kelley', 'email': 'belljack@example.net'}, {'id': 'E00101', 'name': 'Javier Rivera', 'email': 'dana18@example.net'}, {'id': 'E00102', 'name': 'Ruben Hancock', 'email': 'hallmeredith@example.com'}, {'id': 'E00103', 'name': 'Timothy Haynes', 'email': 'aparker@example.net'}, {'id': 'E00104', 'name': 'John Long', 'email': 'adam92@example.org'}, {'id': 'E00105', 'name': 'Dawn Gross', 'email': 'xking@example.com'}, {'id': 'E00106', 'name': 'Dr. William Berger', 'email': 'taylorjustin@example.net'}, {'id': 'E00107', 'name': 'Jon Harper', 'email': 'reynoldscarlos@example.net'}, {'id': 'E00108', 'name': 'Andrew House', 'email': 'dawnhinton@example.net'}, {'id': 'E00109', 'name': 'Kerry Bishop', 'email': 'pwalker@example.org'}, {'id': 'E00110', 'name': 'Amber Anderson', 'email': 'ddickerson@example.org'}, {'id': 'E00111', 'name': 'Jesse Ramos', 'email': 'zyoung@example.org'}, {'id': 'E00112', 'name': 'Jeanne Robinson', 'email': 'anthony70@example.com'}, {'id': 'E00113', 'name': 'April Richardson', 'email': 'deborahcraig@example.com'}, {'id': 'E00114', 'name': 'Howard Brown', 'email': 'moranphilip@example.org'}, {'id': 'E00115', 'name': 'Mary Moore', 'email': 'richardwalsh@example.net'}, {'id': 'E00116', 'name': 'Dr. Ariana Henderson MD', 'email': 'dorothybutler@example.net'}, {'id': 'E00117', 'name': 'Sophia Everett', 'email': 'ojohnson@example.net'}, {'id': 'E00118', 'name': 'Barbara Andrews', 'email': 'hallmegan@example.net'}, {'id': 'E00119', 'name': 'Megan Conway', 'email': 'kelsey31@example.com'}, {'id': 'E00120', 'name': 'Jessica Peterson', 'email': 'cfranco@example.org'}, {'id': 'E00121', 'name': 'Theresa Frazier', 'email': 'gregory79@example.org'}, {'id': 'E00122', 'name': 'Cristina Baker', 'email': 'fjefferson@example.org'}, {'id': 'E00123', 'name': 'Dustin Newton', 'email': 'wellsmichael@example.net'}, {'id': 'E00124', 'name': 'David Ryan', 'email': 'pmiranda@example.org'}, {'id': 'E00125', 'name': 'Mario Lloyd', 'email': 'meyerschristina@example.com'}, {'id': 'E00126', 'name': 'Amy Parker', 'email': 'dawn12@example.com'}, {'id': 'E00127', 'name': 'Melissa Edwards', 'email': 'nancycarter@example.org'}, {'id': 'E00128', 'name': 'Sara Rivera', 'email': 'jcarson@example.org'}, {'id': 'E00129', 'name': 'Joshua Joseph', 'email': 'michaelunderwood@example.net'}, {'id': 'E00130', 'name': 'Dr. Anthony Davis', 'email': 'john32@example.org'}, {'id': 'E00131', 'name': 'Robert Carlson', 'email': 'greenjohn@example.com'}, {'id': 'E00132', 'name': 'Lauren Hamilton', 'email': 'clee@example.org'}, {'id': 'E00133', 'name': 'Bobby Pham', 'email': 'jmarsh@example.org'}, {'id': 'E00134', 'name': 'Elizabeth Price', 'email': 'benjamin17@example.com'}, {'id': 'E00135', 'name': 'Duane Aguilar', 'email': 'johnbryant@example.com'}, {'id': 'E00136', 'name': 'Karen Cobb', 'email': 'emilygardner@example.com'}, {'id': 'E00137', 'name': 'Teresa Lee', 'email': 'trobertson@example.net'}, {'id': 'E00138', 'name': 'John Watson', 'email': 'hopkinsjennifer@example.org'}, {'id': 'E00139', 'name': 'John Bradshaw', 'email': 'dcurry@example.net'}, {'id': 'E00140', 'name': 'Erik Franklin', 'email': 'epotts@example.com'}, {'id': 'E00141', 'name': 'Ashley Ross', 'email': 'taylor01@example.org'}, {'id': 'E00142', 'name': 'Elizabeth Wilson', 'email': 'davidvasquez@example.org'}, {'id': 'E00143', 'name': 'Vanessa Cox', 'email': 'davidburns@example.com'}, {'id': 'E00144', 'name': 'Kristen Hughes', 'email': 'richard07@example.org'}, {'id': 'E00145', 'name': 'Javier York', 'email': 'palmerronald@example.org'}, {'id': 'E00146', 'name': 'Benjamin Watson', 'email': 'michaelmartin@example.com'}, {'id': 'E00147', 'name': 'April Cline', 'email': 'rebeccabrandt@example.net'}, {'id': 'E00148', 'name': 'Michael Hunt', 'email': 'phillipreeves@example.com'}, {'id': 'E00149', 'name': 'Allen Guzman', 'email': 'zrodriguez@example.com'}, {'id': 'E00150', 'name': 'Elizabeth Spence', 'email': 'ashley64@example.com'}, {'id': 'E00151', 'name': 'Adam Mills', 'email': 'sanchezjill@example.net'}, {'id': 'E00152', 'name': 'Robert Moore', 'email': 'smithphyllis@example.net'}, {'id': 'E00153', 'name': 'Dylan Mckinney', 'email': 'deanna09@example.org'}, {'id': 'E00154', 'name': 'Kristin Williams', 'email': 'brooke17@example.com'}, {'id': 'E00155', 'name': 'Miranda Cole', 'email': 'david96@example.net'}, {'id': 'E00156', 'name': 'Robert Bell', 'email': 'cwilson@example.org'}, {'id': 'E00157', 'name': 'Michelle Brown', 'email': 'lclay@example.com'}, {'id': 'E00158', 'name': 'Lucas Wagner', 'email': 'karl88@example.net'}, {'id': 'E00159', 'name': 'Robert Johnson', 'email': 'samantha28@example.org'}, {'id': 'E00160', 'name': 'William Jackson', 'email': 'joyce76@example.net'}, {'id': 'E00161', 'name': 'Mary Buck', 'email': 'laurawaller@example.com'}, {'id': 'E00162', 'name': 'Amanda Villegas', 'email': 'gallagherevelyn@example.net'}, {'id': 'E00163', 'name': 'Shawn Bowen', 'email': 'conradjames@example.com'}, {'id': 'E00164', 'name': 'Willie Jones', 'email': 'burnsmichelle@example.net'}, {'id': 'E00165', 'name': 'Robert Mccall', 'email': 'jaclynfry@example.org'}, {'id': 'E00166', 'name': 'Martin Roberts', 'email': 'rriley@example.org'}, {'id': 'E00167', 'name': 'Kelly Watts', 'email': 'rodriguezjon@example.net'}, {'id': 'E00168', 'name': 'Kelly Cardenas', 'email': 'lisa17@example.net'}, {'id': 'E00169', 'name': 'Jeff Wilkerson', 'email': 'courtneyortiz@example.org'}, {'id': 'E00170', 'name': 'Jennifer Anderson', 'email': 'joshuawallace@example.com'}, {'id': 'E00171', 'name': 'Amanda Luna', 'email': 'rogerray@example.com'}, {'id': 'E00172', 'name': 'Elizabeth Lopez', 'email': 'garciacarol@example.net'}, {'id': 'E00173', 'name': 'Alexis Chen', 'email': 'pvega@example.com'}, {'id': 'E00174', 'name': 'Brian Jones', 'email': 'lauren65@example.com'}, {'id': 'E00175', 'name': 'Jennifer Vincent', 'email': 'chaneynicholas@example.com'}, {'id': 'E00176', 'name': 'Mr. Joseph Ford DDS', 'email': 'amy17@example.com'}, {'id': 'E00177', 'name': 'Amanda Daniels', 'email': 'theresa27@example.com'}, {'id': 'E00178', 'name': 'Mary Fox', 'email': 'crystal76@example.net'}, {'id': 'E00179', 'name': 'Gerald Ross', 'email': 'hward@example.net'}, {'id': 'E00180', 'name': 'Amy Pollard', 'email': 'bedwards@example.org'}, {'id': 'E00181', 'name': 'Amber Silva', 'email': 'mbrown@example.net'}, {'id': 'E00182', 'name': 'Jasmine Moreno', 'email': 'donna63@example.org'}, {'id': 'E00183', 'name': 'Lisa Griffin', 'email': 'zbarker@example.net'}, {'id': 'E00184', 'name': 'Justin Myers', 'email': 'phillipmitchell@example.org'}, {'id': 'E00185', 'name': 'Carmen Torres', 'email': 'hinespeter@example.org'}, {'id': 'E00186', 'name': 'Monica Clark', 'email': 'longcraig@example.com'}, {'id': 'E00187', 'name': 'Dawn Santiago', 'email': 'fscott@example.com'}, {'id': 'E00188', 'name': 'Alexander Rocha', 'email': 'justin91@example.com'}, {'id': 'E00189', 'name': 'Haley Williams', 'email': 'smithcraig@example.net'}, {'id': 'E00190', 'name': 'Courtney Jackson', 'email': 'smithpaula@example.org'}, {'id': 'E00191', 'name': 'Albert Gonzalez', 'email': 'haleygood@example.net'}, {'id': 'E00192', 'name': 'John Jones', 'email': 'ryan47@example.com'}, {'id': 'E00193', 'name': 'Katherine Becker', 'email': 'brooke32@example.org'}, {'id': 'E00194', 'name': 'Christina Colon', 'email': 'adam30@example.com'}, {'id': 'E00195', 'name': 'Roberto Lopez', 'email': 'meganmitchell@example.org'}, {'id': 'E00196', 'name': 'Eric Jones', 'email': 'robertwhite@example.net'}, {'id': 'E00197', 'name': 'Julie Brown', 'email': 'bmorris@example.org'}, {'id': 'E00198', 'name': 'Nancy Morrison', 'email': 'matthew37@example.org'}, {'id': 'E00199', 'name': 'Jacob Carlson', 'email': 'aandrews@example.org'}, {'id': 'E00200', 'name': 'Timothy Mullins', 'email': 'sotokaren@example.org'}, {'id': 'E00201', 'name': 'Peter Haley', 'email': 'jason16@example.com'}]
    aref=['robert91@example.com', 'arnoldtheresa@example.com', 'burnsmark@example.com', 'mark31@example.org', 'cwiley@example.org', 'uthomas@example.net', 'ericwilliams@example.org', 'joshuacrawford@example.org', 'brittanybrown@example.net', 'johnsummers@example.org', 'schmidtandrea@example.org', 'apeters@example.com', 'crystalalvarez@example.net', 'jhernandez@example.net', 'eugenemendoza@example.net', 'kflores@example.org', 'bmorales@example.net', 'isabel45@example.net', 'kevin62@example.org', 'jmcdonald@example.net', 'fli@example.net', 'georgegeorge@example.net', 'hharper@example.org', 'cynthiapowell@example.org', 'taylorkelly@example.com', 'valeriecannon@example.net', 'wallstephanie@example.com', 'james58@example.com', 'josephshort@example.net', 'sheltonelizabeth@example.org', 'sarablake@example.com', 'rhudson@example.org', 'evanstimothy@example.com', 'fosterpatricia@example.com', 'christopher88@example.org', 'haleyjames@example.org', 'tammy61@example.net', 'sharonparsons@example.net', 'justin30@example.com', 'ivincent@example.net', 'hectormorris@example.net', 'christopherburns@example.org', 'kristin30@example.net', 'john41@example.com', 'shirleywalters@example.org', 'johnsonanthony@example.com', 'ruizmichele@example.com', 'josephfitzgerald@example.org', 'ecarter@example.com', 'qjones@example.net', 'crystalgray@example.net', 'christopher77@example.com', 'cruzkristine@example.com', 'joel18@example.org', 'danielle00@example.net', 'kjames@example.com', 'andrew43@example.com', 'jerry07@example.net', 'qaustin@example.org', 'andersonpatrick@example.org', 'jay56@example.org', 'edwardsjoel@example.com', 'phillipellis@example.com', 'lnorman@example.net', 'morgangeorge@example.net', 'farleymark@example.org', 'wendyanthony@example.net', 'deborahbrown@example.org', 'bradleyduncan@example.net', 'john01@example.net', 'sean57@example.net', 'alex97@example.org', 'vowens@example.org', 'hannah58@example.org', 'alexanderchristopher@example.org', 'richardbarnes@example.com', 'johnduncan@example.net', 'marshalldustin@example.net', 'allentyler@example.com', 'iadams@example.org', 'fweber@example.com', 'mcdowelljeremy@example.org', 'henglish@example.org', 'michellelester@example.net', 'dcook@example.org', 'kari58@example.org', 'julian32@example.net', 'montgomeryalyssa@example.com', 'finleyjason@example.org', 'dwood@example.com', 'gallaghercharles@example.com', 'uhall@example.net', 'fgarrett@example.org', 'john63@example.net', 'joseph26@example.com', 'jodi20@example.org', 'johnsonjeanette@example.net', 'jason10@example.org', 'charlesfox@example.com', 'belljack@example.net', 'dana18@example.net', 'hallmeredith@example.com', 'aparker@example.net', 'adam92@example.org', 'xking@example.com', 'taylorjustin@example.net', 'reynoldscarlos@example.net', 'dawnhinton@example.net', 'pwalker@example.org', 'ddickerson@example.org', 'zyoung@example.org', 'anthony70@example.com', 'deborahcraig@example.com', 'moranphilip@example.org', 'richardwalsh@example.net', 'dorothybutler@example.net', 'ojohnson@example.net', 'hallmegan@example.net', 'kelsey31@example.com', 'cfranco@example.org', 'gregory79@example.org', 'fjefferson@example.org', 'wellsmichael@example.net', 'pmiranda@example.org', 'meyerschristina@example.com', 'dawn12@example.com', 'nancycarter@example.org', 'jcarson@example.org', 'michaelunderwood@example.net', 'john32@example.org', 'greenjohn@example.com', 'clee@example.org', 'jmarsh@example.org', 'benjamin17@example.com', 'johnbryant@example.com', 'emilygardner@example.com', 'trobertson@example.net', 'hopkinsjennifer@example.org', 'dcurry@example.net', 'epotts@example.com', 'taylor01@example.org', 'davidvasquez@example.org', 'davidburns@example.com', 'richard07@example.org', 'palmerronald@example.org', 'michaelmartin@example.com', 'rebeccabrandt@example.net', 'phillipreeves@example.com', 'zrodriguez@example.com', 'ashley64@example.com', 'sanchezjill@example.net', 'smithphyllis@example.net', 'deanna09@example.org', 'brooke17@example.com', 'david96@example.net', 'cwilson@example.org', 'lclay@example.com', 'karl88@example.net', 'samantha28@example.org', 'joyce76@example.net', 'laurawaller@example.com', 'gallagherevelyn@example.net', 'conradjames@example.com', 'burnsmichelle@example.net', 'jaclynfry@example.org', 'rriley@example.org', 'rodriguezjon@example.net', 'lisa17@example.net', 'courtneyortiz@example.org', 'joshuawallace@example.com', 'rogerray@example.com', 'garciacarol@example.net', 'pvega@example.com', 'lauren65@example.com', 'chaneynicholas@example.com', 'amy17@example.com', 'theresa27@example.com', 'crystal76@example.net', 'hward@example.net', 'bedwards@example.org', 'mbrown@example.net', 'donna63@example.org', 'zbarker@example.net', 'phillipmitchell@example.org', 'hinespeter@example.org', 'longcraig@example.com', 'fscott@example.com', 'justin91@example.com', 'smithcraig@example.net', 'smithpaula@example.org', 'haleygood@example.net', 'ryan47@example.com', 'brooke32@example.org', 'adam30@example.com', 'meganmitchell@example.org', 'robertwhite@example.net', 'bmorris@example.org', 'matthew37@example.org', 'aandrews@example.org', 'sotokaren@example.org', 'jason16@example.com']


    copo=compareToRef(a1,aref)   
    if copo != True:
        return False 
    
    a1={'address': {'city': 'North Ann', 'location': {'country': 'USA', 'geo': {'lat': '-0.5213', 'long': '69.7529', 'timezone': {'name': 'America/Denver', 'utc_offset': '-07:00'}}, 'state': 'TX'}, 'street': '597 Mark Centers'}, 'email': 'jcarson@example.org', 'phone': '388-532-0441x74446'}
    aref=[{'street': '597 Mark Centers', 'city': 'North Ann'}]
    copo=compareToRef(a1,aref)   
    if copo != True:
        return False 
    
    return True