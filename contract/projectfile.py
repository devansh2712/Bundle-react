# Project contract
import smartpy as sp

class Tijori_pro_c(sp.Contract):
    def __init__(self,admin):
        self.init(
            product=sp.none,
            owner=sp.none,
            admin=_admin,
            reqfunds=sp.none,
            funded=sp.none,
            address=sp.none,
            link=sp.nonw,
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
        sp.verify(sp.seder==self.data.admin)
        self.data.revoke=params
        
    @sp.entry_point
    def spendFunds(self,params):
        sp.set_type(params, sp.TRecord(from_=sp.TAddress, to_ =sp.TAddress, value=sp.TNat).layout(("from_ as from", ("to_ as to", "value"))))
        sp.verify((sp.sender == self.data.admin) |
            (~self.data.revoke &
                   ((params.amount<= self.data.funded) |
                   (sp.send(to_,amount))
                   (_balance = self.data.funded - params.amount))))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
                        
