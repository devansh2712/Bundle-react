import smartpy as sp

class DAO_Token(sp.Contract):
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
        
    
    

class Project_token(sp.Contract):
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
    def __init__(self,own):
        self.init(
            owner=own)
        
    @sp.entry_point
    def spendfunds(self,address, traamount):
        traamount = sp.local('amount', sp.amount)
        sp.verify(traamount.value<=sp.balance)
        sp.send(address, traamount.value)
        
        
        
class DAO(sp.Contract):
    def __init__(self,admin,strength,min_contribution):
        self.init(
            admin=admin,
            strength=strength,
            dispute=0,
            product_id =0,
            proposal_id=0,
            min_contribution=min_contribution,
            daotoken=sp.none,
            projecttoken=sp.none,
            addmemberdata = sp.big_map(tkey = sp.TAddress,
                			        tvalue = sp.TRecord(
                       				contribution = sp.TInt,
                       				balance = sp.TInt
									                    )
		    						),
			addprojectdata = sp.big_map( 
                tkey = sp.TInt, 
                tvalue = sp.TRecord(
                    serialno=sp.TInt,
                    proadd=sp.TAddress,
                    vote = sp.TInt
                )
            ),
            addpropoasldata = sp.big_map( 
                tkey = sp.TInt, 
                tvalue = sp.TRecord(
                    proposer=sp.TAddress,
                    fund=sp.TMutez,
                    serialno=sp.TInt,
                    vote = sp.TInt
                )
            )
            )
    

        
        
    @sp.entry_point
    def set_daotoken(self,Token):
        sp.set_type(Token, sp.TAddress)
        sp.verify(sp.sender == self.data.admin)
        sp.verify(~self.data.daotoken.is_some())
        self.data.daotoken = sp.some(Token)
    @sp.entry_point
    def set_projecttoken(self,Token):
        sp.set_type(Token, sp.TAddress)
        sp.verify(sp.sender == self.data.admin)
        sp.verify(~self.data.projecttoken.is_some())
        self.data.projecttoken = sp.some(Token)
        
    @sp.entry_point
    def addmember(self,contribution):
        #restrict karna hai member count se
        sp.set_type(contribution, sp.TInt)
        contribution = contribution
        sp.verify(contribution >= self.data.min_contribution)
        mem_address = sp.sender
        
        sp.if ~self.data.addmemberdata.contains(mem_address):
            self.data.addmemberdata[mem_address]=sp.record(contribution=contribution,balance=contribution)
            tokenContract = sp.contract(sp.TRecord(address = sp.TAddress, tokbal = sp.TNat),
                                    self.data.daotoken.open_some(),
                                    "mint").open_some()
            #sp.transfer(sp.record(address = sp.sender, value =contribution ),
                    # sp.tez(0),
                    # tokenContract)
    @sp.entry_point
    def addproduct(self):
        
        self.data.product_id += 1
        pd_index = self.data.product_id
        
        sp.if ~self.data.addprojectdata.contains(pd_index):
            self.data.addprojectdata[pd_index] = sp.record(serialno=pd_index,vote = 0,proadd=sp.sender) 
    
    @sp.entry_point
    def addproposal(self,funding):
        funding = sp.local('amount', sp.amount)
        self.data.proposal_id += 1
        ps_index = self.data.proposal_id
        
        sp.if ~self.data.addprojectdata.contains(ps_index):
            self.data.addpropoasldata[ps_index] = sp.record(serialno=ps_index,vote = 0,proposer=sp.sender,fund=funding.value)
    
    @sp.entry_point
    def voteproject(self,proindex,value):
        
        sp.if self.data.addprojectdata.contains(proindex):
            sp.if self.data.addmemberdata.contains(sp.sender):
                self.data.addprojectdata[proindex].vote+=value
                self.data.addmemberdata[sp.sender].balance-=value
            
    @sp.entry_point
    def voteproposal(self,proindex,value):
        
        sp.if self.data.addpropoasldata.contains(proindex):
            sp.if self.data.addmemberdata.contains(sp.sender):
                self.data.addpropoasldata[proindex].vote+=value
                self.data.addmemberdata[sp.sender].balance-=value
    @sp.entry_point
    def finalise(self,address, traamount):
        traamount = sp.local('amount', sp.amount)
        sp.verify(traamount.value<=sp.balance)
        sp.verify(self.data.dispute==0)
        sp.send(address, traamount.value)
    @sp.entry_point
    def dispute(self, value):
        self.data.dispute=value
    
    
if "templates" not in __name__:
    @sp.add_test(name="Test_contract")
    def contracttesting():
        scenario=sp.test_scenario()
        admin = sp.test_account('Administrator')
        admin = sp.test_account('Administrator')
        amit = sp.test_account('Amit')  
        dhruv = sp.test_account('Dhruv')  
        aryan = sp.test_account('Aryan')  
        devansh = sp.test_account('Devansh')  
        komal = sp.test_account('Komal')
        shikhar = sp.test_account('Shikhar')  
        jaanvi = sp.test_account('Jaanvi')
        product1 = sp.test_account('product1')
        product2 = sp.test_account('product2')
        product3 = sp.test_account('product3')
        daoc=DAO(admin.address,10,20)
        proc=project(devansh.address)
        dtokenc=DAO_Token(admin.address)
        ptokenc=Project_token(admin.address)
        scenario.h1("TIJORI Contract testing")
        scenario.h2("List of test accounts")
        scenario.show([admin, amit, dhruv,aryan,devansh,komal,shikhar,jaanvi])
        scenario.h2("list of contracts")
        scenario.h3("FA1.2 token(DAO Token)")
        scenario.show([dtokenc.address])
        scenario.h3("DAO contract")
        scenario.show([daoc.address])
        scenario.h3("Project contract")
        scenario.show([proc.address])
        scenario.h2("Project contract testing")
        scenario+=proc
        scenario.h2("Project contract initialized")
        scenario.h2("Spend funds")
        scenario+=proc.spendfunds(address=shikhar.address,amount=sp.mutez(200)).run(sender=devansh,amount=sp.tez(1000))
        scenario.p("Spend funds successful")
        scenario += daoc
        scenario.h3("Dao Initialized")
        scenario.h2('Set DAO token')
        scenario += daoc.set_daotoken(proc.address).run(sender = admin)
        scenario.h3("Set  DAO token succesful")
        scenario.h2('Set DAO token')
        scenario += daoc.set_projecttoken(proc.address).run(sender = admin)
        scenario.h3("Set Project token succesful")
        scenario.h2("Add member")
        scenario +=daoc.addmember(20).run(sender=dhruv,amount = sp.tez(20))
        scenario +=daoc.addmember(40).run(sender=jaanvi,amount= sp.tez(40))
        scenario +=daoc.addmember(15).run(sender=komal,amount= sp.tez(15), valid= False)
        scenario.h3("Add member succesful ")
        scenario.h2("Add project")
        scenario+=daoc.addproduct().run(sender=product1)
        scenario+=daoc.addproduct().run(sender=product2)
        scenario+=daoc.addproduct().run(sender=product3)
        scenario.h3("add project successful")
        scenario+=daoc.addproposal(funding=sp.mutez(100)).run(sender=devansh)
        scenario+=daoc.addproposal(funding=sp.mutez(100)).run(sender=komal)
        scenario+=daoc.addproposal(funding=sp.mutez(100)).run(sender=dhruv)
        scenario.h3("add propsal successful")
        scenario.h2(" Proposal voating ")
        scenario+=daoc.voteproposal(proindex=1,value=5).run(sender=dhruv)
        scenario+=daoc.voteproposal(proindex=1,value=4).run(sender=amit)
        scenario+=daoc.voteproposal(proindex=2,value=5).run(sender=devansh)
        scenario+=daoc.voteproposal(proindex=3,value=6).run(sender=jaanvi)
        scenario.h3("proposal voating succesful")
        scenario.h2(" Project voating ")
        scenario+=daoc.voteproject(proindex=1,value=5).run(sender=dhruv)
        scenario+=daoc.voteproject(proindex=1,value=4).run(sender=amit)
        scenario+=daoc.voteproject(proindex=2,value=5).run(sender=devansh)
        scenario+=daoc.voteproject(proindex=3,value=6).run(sender=jaanvi)
        scenario.h3("Project voating succesful")
        scenario.h2("Finalise")
        scenario+=daoc.finalise(address=product1.address,amount=sp.mutez(200)).run(sender=devansh,amount=sp.tez(1000))
        scenario.h3("project finalised")
        scenario.h2("raise dispute")
        scenario+=daoc.dispute(1).run(sender=dhruv)
        scenario.h3("raise dispute sucessful")
        
        
        
        
        
        
