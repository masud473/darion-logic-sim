
from encodings.punycode import T


objlist={}
complist=[]
varlist=[]


class Signal:
    # default signals that exist indepdently
    def __init__(self,value):
        self.value=value
    def output(self):
        return self.value
    
objlist[0]=Signal(0)
objlist[1]=Signal(1)
objlist[-1]=Signal(-1)


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
        if len(self.children)<self.inputlimit:
            self.children.append(child)
            objlist[child].parents.append(self.code)

    # deletes parent from the parent list
    def delparent(self,parent):    
        if parent in self.parents:
            objlist[parent].children.remove(self.code)
            self.parents.remove(parent)
    
    # deletes child from the children list
    def delchild(self,child):    
        if child in self.children:
            objlist[child].parents.remove(self.code)
            self.children.remove(child)

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
    rank=0
    def __init__(self):
        super().__init__()        
        self.inputlimit=1
        self.code=chr(ord('A') + Variable.rank)
        Variable.rank+=1
        self.children.append(0)

    def output(self):
       child=self.children[0]
       return objlist[child].output()
    
        
class NOT(Gate):
    rank=0
    def __init__(self):
        super().__init__()        
        self.inputlimit=1
        NOT.rank+=1
        self.code='NOT-'+str(NOT.rank)
        
    def output(self):
        if self.output_check()==False:
            return -1
        
        x=objlist[self.children[0]].output()
        if x==-1:
            return -1
        else:
            return not x
        
class AND(Gate):

    rank=0
    def __init__(self):
        super().__init__()        
        AND.rank+=1
        self.code='AND-'+str(AND.rank)
    def output(self):
        if self.output_check()==False:
            return -1
        x=objlist[self.children[0]].output()
        for i in range(1,self.inputlimit):
            x= x and objlist[self.children[i]].output()
        return x
    


class NAND(AND):
    rank=0
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



def addComponent():
    while True:
        print("Choose a gate to add to the circuit:")
        print("1. NOT")
        print("2. AND")
        print("3. NAND")
        print("4. OR")
        print("5. NOR")  
        print("6. XOR")
        print("7. XNOR")
        print("8. Variables")     

        choice = input("Enter your choice: ").split()
        if len(choice)==0:
            break
        for i in choice:
            print(i)
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
            else:
                break
            objlist[gt.code]=gt

            complist.append(gt.code)
        print(complist)

objlist['AND-1']=AND()
objlist['A']=Variable()
objlist['A'].children[0]=1
objlist['AND-1'].children.append('A')
objlist['B']=Variable()
objlist['B'].children[0]=0
objlist['AND-1'].children.append('B')
objlist['NOT-1']=NOT()
# add and-1 ,not-1 and variables to complist with append
complist.append('AND-1')
complist.append('A')
complist.append('B')
complist.append('NOT-1')
# add each input to their parent and vise versa
objlist['AND-1'].parents.append('NOT-1')
objlist['NOT-1'].children.append('AND-1')
# same for variables
objlist['A'].parents.append('AND-1')
objlist['B'].parents.append('AND-1')



#print(objlist['NOT-1'].display_output())

def removeparent(gate,parent):    
    objlist[parent].children.remove(gate)
    objlist[gate].parents.remove(parent)


def removechild(gate,child):    
    objlist[child].parents.remove(gate)       
    objlist[gate].children.remove(child)


def disconnect():
    while True:
        for i in range(len(complist)):
            print(f'{i}. {complist[i]}')
        print()
        print("Which component do you want to disconnect?")
        
        
        comp = int(input("Enter the index of the component to disconnect (or -1 to exit): "))
        print()
        if comp == -1:
            break
        op1=input('1. Parent 2. children\n')

        if op1=='1':
            parentlist=objlist[complist[comp]].parents
            print('Parentlist: ',end='')
            for i in range(len(parentlist)):
                print(f'{i}. {parentlist[i]}')
            parent=complist[int(input('Select Parent from the list: '))]
            gate=complist[comp]
            print(f'disconnecting {gate} & {parent}')
            removeparent(gate,parent)
        if op1=='2':
            childlist=objlist[complist[comp]].children
            print('childlist: ',end='')
            for i in range(len(childlist)):
                print(f'{i}. {childlist[i]}')
            child=complist[int(input('Select Child from the list: '))]
            gate=complist[comp]
            print(f'disconnecting {gate} & {child}')
            removechild(gate,child)      
                
disconnect()

        

        

def wires():
    while True:
        for i in range(len(complist)):
                print(f'{i}. {complist[i]}',end=' | ')
        print()
        print('1. Connect Components')
        print('2. Variable input')
        print('3. See outputs')
        choice=input()
        if choice=='1':            
            comp=int(input('Select Component: '))
            if(comp==-1):
                break
           
            add = list(map(int,input("Enter your children: ").split()))
            if len(add)==0:
                break
            for i in add:    
                objlist[complist[i]].parents.append(complist[comp])
                objlist[complist[comp]].children.append(complist[i])
            print(objlist[complist[comp]].children)
        elif choice=='2':
             if complist[comp] in varlist:
                    objlist[complist[comp]].children[0]=int(input('0 or 1'))
        elif choice=='3':
            comp=int(input('Select Component: '))
            print(objlist[complist[comp]].display_output())
        else:
            break





