
from encodings.punycode import T


objlist={}
complist=[]
varlist=[]


class Signal:
    # default signals that exist indepdently
    def __init__(self,value):
        self.value=value
        self.parents=[]
    def output(self):
        return self.value
    
objlist['0']=Signal(0)
objlist['1']=Signal(1)
objlist['-1']=Signal(-1)


class Gate:   

    def __init__(self):
        # gate's children or inputs
        self.children=[]
        # parents of the gate
        self.parents=[]
        # input limit
        self.inputlimit=2
        # each gate will have it's own unique id
        self.code=''
    # sets number of children
    def setlimits(self,l):
        self.inputlimit=l

    # connects gates
    def connect(self,child):
        if self.code in varlist:
            self.children[0]=child
        elif len(self.children)<self.inputlimit:
            self.children.append(child)
            objlist[child].parents.append(self.code)

    # deletes parent from the parent list
    def disconnect(self,node):    
        # check if node is a parent or a child
        # then delete accordingly
        if node in self.parents:
            objlist[node].children.remove(self.code)
            self.parents.remove(node)
        elif node in self.children:
            objlist[node].parents.remove(self.code)
            self.children.remove(node)
        else:
            print('Not Connected')

    # checks if there are enough desired children
    def output_check(self):
        return len(self.children)==self.inputlimit
    
    def output(self):
        pass
    
    # gives output in T or F
    def display_output(self):
        out=self.output()
        return 'T' if out else 'F'





class Variable(Gate):
    # this can be both an input or output(bulb)
    rank=0
    def __init__(self):
        super().__init__()        
        self.inputlimit=1
        self.code=chr(ord('A') + Variable.rank)
        Variable.rank+=1
        self.children.append('0')
    # no changing the limit
    def setlimits(self):
        pass
    def output(self):
        if self.output_check()==False:
                return -1        
        child =objlist[self.children[0]].output()
        if child==-1:
            return -1
        else:
            return child
    
        
class NOT(Gate):
    rank=0
    def __init__(self):
        super().__init__()        
        self.inputlimit=1
        NOT.rank+=1
        self.code='NOT-'+str(NOT.rank)

    # no changing the limit
    def setlimits(self):
        pass
    def output(self):
        if self.output_check()==False:
            return -1
        
        child=objlist[self.children[0]].output()
        if child==-1:
            return -1
        else:
            return not child
        
class AND(Gate):

    rank=0
    def __init__(self):
        super().__init__()        
        AND.rank+=1
        self.code='AND-'+str(AND.rank)
    def output(self):
        if self.output_check()==False:
            return -1
        # iterate through the children/inputs
        x=objlist[self.children[0]].output()
        for i in range(1,self.inputlimit):
            x= x and objlist[self.children[i]].output()
        return x
    


class NAND(AND):
    rank=0
    # basically a not + and gate
    def __init__(self):
        super().__init__()
        NAND.rank+=1
        self.code='NAND-'+str(NAND.rank)
        AND.rank-=1
    def output(self):
        return not super().output()

class OR(Gate):
    rank=0
    def __init__(self):
        super().__init__()        
        OR.rank+=1
        self.code='OR-'+str(OR.rank)
    def output(self):
        if self.output_check()==False:
            return -1
        x=objlist[self.children[0]].output()
        for i in range(1,self.inputlimit):
            x= x or objlist[self.children[i]].output()
        return x

class NOR(OR):
    rank=0
    def __init__(self):
        super().__init__()
        NOR.rank+=1
        self.code='NOR-'+str(NOR.rank)
        OR.rank-=1
    def output(self):
        return not super().output()

class XOR(Gate):
    rank=0
    def __init__(self):
        super().__init__()        
        XOR.rank+=1
        self.code='XOR-'+str(XOR.rank)
    def output(self):
        if self.output_check()==False:
            return -1
        x=objlist[self.children[0]].output()
        for i in range(1,self.inputlimit):
            x= x ^ objlist[self.children[i]].output()
        return x

class XNOR(XOR):
    rank=0
    def __init__(self):
        super().__init__()
        XNOR.rank+=1
        self.code='XNOR-'+str(XNOR.rank)
        XOR.rank-=1
    def output(self):
        return not super().output()


# inventory
def listComponent():
    for i in range(len(complist)):
        print(f'{i}. {complist[i]}')

def addComponent():
    print("Choose a gate to add to the circuit:")
    print("1. NOT")
    print("2. AND")
    print("3. NAND")
    print("4. OR")
    print("5. NOR")  
    print("6. XOR")
    print("7. XNOR")
    print("8. Variable")     

    choice = input("Enter your choice: ").split()

    for i in choice:
        if i == '1':
            gt = NOT()
        elif i == '2':
            gt = AND()
        elif i == '3':
            gt = NAND()
        elif i == '4':
            gt = OR()
        elif i == '5':
            gt = NOR()                
        elif i == '6':
            gt = XOR()
        elif i == '7':
            gt = XNOR()
        elif i=='8':
            gt=Variable()
            varlist.append(gt.code)
        objlist[gt.code]=gt
        complist.append(gt.code)

def deleteComponent(gate):
    for child in gate.children:
        objlist[child].parents.remove(gate)
    for parent in gate.parent:
        objlist[parent].children.remove(gate)
    
# wiring

def connect(gate,comp):
    objlist[gate].connect(comp)
def disconnect(gate,comp):
    objlist[gate].disconnect(comp)


# Result 
def output(gate):
    print(objlist[gate].display_output())

# create items manually
addComponent()
connect('AND-1','A')
connect('AND-1','B')
connect('NOT-1','AND-1')

connect('A','1')
connect('B','0')

output('AND-1')

disconnect('NOT-1','AND-1')
connect('NOT-1','0')

output('NOT-1')





