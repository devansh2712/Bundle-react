import smartpy as sp
class Tijori_pro_c(sp.Contract):
    def _init_(self,admin):
        self.init(
            product=sp.none,
            owner=sp.none,
            adminAddress=admin,
            reqfunds=sp.none,
            funded=sp.none,
            address=sp.none,
            link=sp.none,
            comm=sp.none,
            revoke= False,
            value=sp.none,
            balance=sp.none,
            category=sp.none)
    
    @sp.entry_point
    def setowner(self,params):
        sp.set_type(
            params,
            sp.TRecord(
                owner=sp.TAddress
            )
        )
        sp.verify(sp.sender==self.data.adminAddress)
        self.data.adminAddress=params.owner

    @sp.entry_point
    def get_value(self):
        sp.verify(sp.sender == self.data.owner)
        product=input('product')
        reqfunds=input('required funds')
        link=input('project link')
        comm=input('communnication link')
        category=input('category')

        


    @sp.entry_point
    def get_balance(self):
        balance=sp.balance
        print(balance)
    
    @sp.entry_point
    def setRevoke(self,params):
        sp.set_type(
            params,
            sp.TRecord(
                revoke=sp.TBool
            )
        )
        sp.verify(sp.sender==self.data.adminAddress)
        self.data.revoke= params.revoke
    @sp.entry_point
    def spendFunds(self,address, amount):
        #amount= sp.tez(10)
        #sp.set_type(params, sp.TRecord(from_=sp.TAddress, to_ =sp.TAddress, value=sp.TMutez).layout(("from_ as from", ("to_ as to", "value"))))
        amount = sp.local('amount', sp.amount)
        sp.verify((sp.sender == self.data.owner) &
            (self.data.revoke==True )&( self.data.amount<=self.data.balance))
        sp.send(address, amount.value)
        balance = self.data.funded - amount.value
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
        proC = Tijori_pro_c(admin=admin.address)
        scenario.h2("initialize")
        #perform setowner
        scenario.h2("Set owner")
        scenario += proC
        scenario.h3("Owner assigned")
        scenario += proC.setowner(owner=alice.address).run(sender=admin)
        #perform set revoke
        scenario.h2("set revoke")
        scenario += proC.setRevoke(revoke=True).run(sender=alice, valid=False)
        scenario.h3("revoke state defined")
        #perform spend funds
        scenario.h2("spend funds")
        scenario += proC.setRevoke(revoke=True).run(sender=admin)
        scenario += proC.spendFunds(address=admin.address,amount=sp.tez(10)).run(sender=admin)
        scenario.h3("funds sent")
        #perform get balance
        scenario.h2("balance")
        scenario += proC.setRevoke(revoke=True).run(sender=admin)
        #scenario += proC.get_balance()
        scenario.h3("balance defined")
