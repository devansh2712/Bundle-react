import smartpy as sp
class token(sp.Contract):
    def __init__(self, admin):
        self.init(paused = False, balances = sp.big_map(tvalue = sp.TRecord(approvals = sp.TMap(sp.TAddress, sp.TNat), balance = sp.TNat)), administrator = admin, totalSupply = 0)

    @sp.entry_point
    def transfer(self, params):
        sp.set_type(params, sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value"))))
        sp.verify((sp.sender == self.data.administrator) |
            (~self.data.paused &
                ((params.from_ == sp.sender) |
                 (self.data.balances[params.from_].approvals[sp.sender] >= params.value))))
        self.addAddressIfNecessary(params.to_)
        sp.verify(self.data.balances[params.from_].balance >= params.value)
        self.data.balances[params.from_].balance = sp.as_nat(self.data.balances[params.from_].balance - params.value)
        self.data.balances[params.to_].balance += params.value
        sp.if (params.from_ != sp.sender) & (self.data.administrator != sp.sender):
            self.data.balances[params.from_].approvals[sp.sender] = sp.as_nat(self.data.balances[params.from_].approvals[sp.sender] - params.value)

    @sp.entry_point
    def approve(self, params):
        sp.set_type(params, sp.TRecord(spender = sp.TAddress, value = sp.TNat).layout(("spender", "value")))
        sp.verify(~self.data.paused)
        alreadyApproved = self.data.balances[sp.sender].approvals.get(params.spender, 0)
        sp.verify((alreadyApproved == 0) | (params.value == 0), "UnsafeAllowanceChange")
        self.data.balances[sp.sender].approvals[params.spender] = params.value

    @sp.entry_point
    def setPause(self, params):
        sp.set_type(params, sp.TBool)
        sp.verify(sp.sender == self.data.administrator)
        self.data.paused = params

    @sp.entry_point
    def setAdministrator(self, params):
        sp.set_type(params, sp.TAddress)
        sp.verify(sp.sender == self.data.administrator)
        self.data.administrator = params

    @sp.entry_point
    def mint(self, params):
        sp.set_type(params, sp.TRecord(address = sp.TAddress, value = sp.TNat))
        sp.verify(sp.sender == self.data.administrator)
        self.addAddressIfNecessary(params.address)
        self.data.balances[params.address].balance += params.value
        self.data.totalSupply += params.value

    @sp.entry_point
    def burn(self, params):
        sp.set_type(params, sp.TRecord(address = sp.TAddress, value = sp.TNat))
        sp.verify(sp.sender == self.data.administrator)
        sp.verify(self.data.balances[params.address].balance >= params.value)
        self.data.balances[params.address].balance = sp.as_nat(self.data.balances[params.address].balance - params.value)
        self.data.totalSupply = sp.as_nat(self.data.totalSupply - params.value)

    def addAddressIfNecessary(self, address):
        sp.if ~ self.data.balances.contains(address):
            self.data.balances[address] = sp.record(balance = 0, approvals = {})

    @sp.view(sp.TNat)
    def getBalance(self, params):
        sp.result(self.data.balances[params].balance)

    @sp.view(sp.TNat)
    def getAllowance(self, params):
        sp.result(self.data.balances[params.owner].approvals[params.spender])

    @sp.view(sp.TNat)
    def getTotalSupply(self, params):
        sp.set_type(params, sp.TUnit)
        sp.result(self.data.totalSupply)

    @sp.view(sp.TAddress)
    def getAdministrator(self, params):
        sp.set_type(params, sp.TUnit)
        sp.result(self.data.administrator)
        
        
class project(sp.Contract):
    def __init__(self,admin):
        self.init(
            admin=admin,
            product=sp.none,
            owner=sp.none,
            revoke=False,
            reqfunds=sp.none,
            funded=sp.none,
            link=sp.none,
            comm=sp.none,
            value=sp.none,
            balance=sp.none,
            approval=0,
            category=sp.none)
            
    @sp.entry_point
    def setowner(self,own):
        sp.set_type(own, sp.TAddress)
        sp.verify(sp.sender == self.data.admin)
        sp.verify(~self.data.owner.is_some())
        self.data.owner = sp.some(own)
        
    @sp.entry_point
    def getvalue(self,pro,reqf,lin,com,cat):
        product=pro
        reqfunds=reqf
        link=lin
        comm=com
        category=cat
        
    @sp.entry_point
    def getbalance(self):
        balance=sp.balance
        
    @sp.entry_point
    def setrevoke(self,params):
        sp.set_type(
            params,
            sp.TRecord(
                revoke=sp.TBool
            )
        )
        self.data.revoke= params.revoke
        
    @sp.entry_point
    def spendfunds(self,address, amount):
        amount = sp.local('amount', sp.amount)

        sp.send(address, amount.value)
        balance = self.data.funded - amount.value
        
        
    

class DAO(sp.Contract):
    def __init__(self,admin,strength,min_contribution):
        self.init(
            admin=admin,
            strength=strength,
            product_id =0,
            maxvoteid=0,
            maxvotecount=0,
            min_contribution=min_contribution,
            token=sp.none,
            addmemberdata = sp.big_map(tkey = sp.TAddress,
                			        tvalue = sp.TRecord(
                       				#address = sp.TAddress,
                       				contribution = sp.TNat,
                       				status = sp.TBool
									                    )
		    						),
			addprojectdata = sp.big_map( 
                tkey = sp.TInt, 
                tvalue = sp.TRecord(
                    roundno= sp.TNat,
                    proadd=sp.TAddress,
                    vote = sp.TInt
                )
            ),
            addpropoasldata = sp.big_map( 
                tkey = sp.TNat, 
                tvalue = sp.TRecord(
                    starttime= sp.TTimestamp,
                    endtime= sp.TTimestamp,
                    vote = sp.TInt
                )
            ),
		    						
		    						
		    						
			
            )
            
    @sp.entry_point
    def set_token(self,Token):
        sp.set_type(Token, sp.TAddress)
        sp.verify(sp.sender == self.data.admin)
        sp.verify(~self.data.token.is_some())
        self.data.token = sp.some(Token)
        
        
    @sp.entry_point
    def addmember(self,contribution):
        
        sp.set_type(contribution, sp.TNat)
        contribution = contribution
        sp.verify(contribution >= self.data.min_contribution)
        mem_address = sp.sender
        
        sp.if ~self.data.addmemberdata.contains(mem_address):
            self.data.addmemberdata[mem_address]=sp.record(contribution=contribution,status=True)
            
        
        

        

    
    
    @sp.entry_point
    def addproduct(self,rou):
        
        sp.set_type(rou, sp.TNat)
        self.data.product_id += 1
        pd_index = self.data.product_id
        
        sp.if ~self.data.addprojectdata.contains(pd_index):
            self.data.addprojectdata[pd_index] = sp.record(roundno = 0, vote = 0,proadd=sp.sender)
            
            
    '''def addproposal(self,st,et):
        
        sp.set_type(st, sp.TTimestamp)
        sp.set_type(et, sp.TTimestamp)
        
        self.data.addpropoasldata[approval].starttime=st
        self.data.addpropoasldata[approval].endtime=et
        approval+=1
        set params'''
            
    '''@sp.entery_point
    def voteproject(self,proid,votetype):
        sp.set_type(proid)'''
        

    @sp.entry_point
    def vote(self,proindex):
        
        sp.if self.data.addprojectdata.contains(proindex):
            self.data.addprojectdata[proindex].vote+=1
              
    @sp.entry_point
    def voteresult(self):
        r=self.data.product_id
        self.data.maxvotecount=self.data.addprojectdata[1].vote
        sp.for x in sp.range(1,r,1):
            sp.if (self.data.addprojectdata[x].vote>self.data.maxvotecount):
                self.data.maxvotecount=self.data.addprojectdata[x].vote
                self.data.maxvoteid=x
        
            
@sp.add_test(name="Test_contract")
def testContract():
    scenario = sp.test_scenario()
    admin = sp.test_account('Administrator')
    amit = sp.test_account('Amit')  
    dhruv = sp.test_account('Dhruv')  
    aryan = sp.test_account('Aryan')  
    devansh = sp.test_account('Devansh')  
    komal = sp.test_account('Komal')
    shikhar = sp.test_account('Shikhar')  
    jaanvi = sp.test_account('Jaanvi')
    daoadd= sp.test_account('daoaccount')
    proadd =sp.test_account('projectaccount')
    daoc=DAO(admin.address,10,10)
    tokc=token(daoc.address)
    proc=project(daoadd.address)
    scenario.h1("TIJORI Contract testing")
    scenario.h2("List of test accounts")
    scenario.show([admin, amit, dhruv,aryan,devansh,komal,shikhar,jaanvi])
    scenario.h2("list of contracts")
    scenario.h3("FA1.2 token(DAO Token)")
    scenario.show([tokc.address])
    scenario.h3("DAO contract")
    scenario.show([daoc.address])
    scenario.h3("Project contract")
    scenario.show([proc.address])
    scenario.h2("Project contract testing")
    scenario+=proc
    scenario.h2("Set owner")
    scenario +=proc.setowner(devansh.address).run(sender= daoadd)
    scenario.h3("set owner succesful")
    scenario.h2("Get value")
    scenario+=proc.getvalue(pro='a',reqf=5000,lin='c',cat='d').run(sender=devansh)
    scenario.h3("get value succesful")
    scenario.h2("get balance")
    scenario+=proc.getbalance().run(sender=devansh)
    scenario.h3("get balance sucesful")
    scenario.h2("setrevoke")
    scenario+=proc.setrevoke(revoke=True).run(sender=devansh)
    scenario.h3("set revoke sucessful")
    scenario.h2("spend funds")
    scenario+=proc.spendfunds(address=shikhar.address,amount=sp.tez(10)).run(sender=devansh)
    scenario.h2("DAO Contract testing")
    scenario += daoc
    scenario.h3("Dao Initialized")
    scenario.h2('Set token')
    scenario += daoc.set_token(proc.address).run(sender = admin)
    scenario.h3("Set token succesful")
    scenario.h2("Add member")
    scenario +=daoc.addmember(10).run(sender=dhruv)
    scenario +=daoc.addmember(10).run(sender=amit)
    scenario +=daoc.addmember(10).run(sender=devansh)
    scenario.h3("Add member succesful ")
    scenario.h2("Add project")
    scenario+=daoc.addproduct(1).run(sender=proadd)
    scenario.h3("add project successful")
    scenario.h2("vote")
    scenario+=daoc.vote(1).run(sender=dhruv)
    scenario+=daoc.vote(1).run(sender=amit)
    scenario+=daoc.vote(1).run(sender=devansh)
    scenario+=daoc.vote(1).run(sender=jaanvi)
    scenario.h3("voting done")
    scenario.h2("show voting result")
    scenario+=daoc.voteresult().run(sender=devansh)
    scenario.h3("voating results calculated")
