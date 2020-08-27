# Project contract
import smartpy as sp

class Tijori_pro_c(sp.Contract):
    def __init__(self,admin):
        self.init(
            product=sp.none,
            owner=sp.none,
            admin=admin,
            reqfunds=sp.none,
            funded=sp.none,
            address=sp.none,
            link=sp.none,
            comm=sp.none,
            revoke= False,
            balance=sp.none,
            category=sp.none)
            
    @sp.entry_point
    def setowner(self,params):
        sp.set_type(params, sp.TAddress)
        sp.verify(sp.sender == self.data.address)
        self.data.admin=params


    @sp.entry_point
    def setRevoke(self,params):
        sp.set_type(params, sp.TBool)
        sp.verify(sp.sender==self.data.admin)
        self.data.revoke=params
        
    @sp.entry_point
    def spendFunds(self,params):
        sp.set_type(params, sp.TRecord(from_=sp.TAddress, to_ =sp.TAddress, value=sp.TNat).layout(("from_ as from", ("to_ as to", "value"))))
        sp.verify((sp.sender == self.data.admin) |
            (~self.data.revoke &
                   ((params.amount<= self.data.funded) |
                   (sp.send(sp.TAddress,amount))
                   (_balance = self.data.funded - params.amount))))
    
    
    @sp.add_test(name = "Project contract")
    def test():

        scenario = sp.test_scenario()
        scenario.h1("Project contract")


        admin = sp.test_account("Administrator")
        alice = sp.test_account("Alice")
        bob   = sp.test_account("Robert")
        john  = sp.test_account("John")
        mike = sp.test_account("Mike") 
        
        #Initialize contracts
        proC = Tijori_pro_c(admin.address)
        scenario.h1("Project Contract")
        
        #perform setowner
        scenario.h2("Set owner")
        scenario += proC.setowner(owner = ownerC.address).run(sender=admin)
        
        
        scenario.h2("set revoke")
        scenario += proC.setRevoke(revoke = False).run(sender=admin)
