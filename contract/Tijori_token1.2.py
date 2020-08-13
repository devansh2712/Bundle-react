# Fungible Assets - FA12
# Inspired by https://gitlab.com/tzip/tzip/blob/master/A/FA1.2.md

import smartpy as sp

class TIJORI_DEFI(sp.Contract):
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

    @sp.entry_point
    def getBalance(self, params):
        sp.transfer(self.data.balances[params.arg.owner].balance, sp.tez(0), sp.contract(sp.TNat, params.target).open_some())

    @sp.entry_point
    def getAllowance(self, params):
        sp.transfer(self.data.balances[params.arg.owner].approvals[params.arg.spender], sp.tez(0), sp.contract(sp.TNat, params.target).open_some())

    @sp.entry_point
    def getTotalSupply(self, params):
        sp.transfer(self.data.totalSupply, sp.tez(0), sp.contract(sp.TNat, params.target).open_some())

    @sp.entry_point
    def getAdministrator(self, params):
        sp.transfer(self.data.administrator, sp.tez(0), sp.contract(sp.TAddress, params.target).open_some())

class Viewer(sp.Contract):
    def __init__(self, t):
        self.init(last = sp.none)
        self.init_type(sp.TRecord(last = sp.TOption(t)))
    @sp.entry_point
    def target(self, params):
        self.data.last = sp.some(params)

if "templates" not in __name__:
    @sp.add_test(name = "TIJORI Testing")
    def test():

        scenario = sp.test_scenario()
        scenario.h1("TIJORI DEFI TESTING")

        scenario.table_of_contents()

        # sp.test_account generates ED25519 key-pairs deterministically:
        admin = sp.test_account("Administrator")
        aryan = sp.test_account("aryan")
        devansh   = sp.test_account("devasnh")

        scenario.show([admin, aryan, devansh])

        c1 = TIJORI_DEFI(admin.address)

        scenario += c1
        scenario += c1.mint(address = aryan.address, value = 12).run(sender = admin)
        scenario += c1.mint(address = aryan.address, value = 3).run(sender = admin)
        scenario += c1.mint(address = aryan.address, value = 3).run(sender = admin)
        scenario += c1.transfer(from_ = aryan.address, to_ = devansh.address, value = 4).run(sender = aryan)
        scenario.verify(c1.data.balances[aryan.address].balance == 14)

        scenario += c1.transfer(from_ = aryan.address, to_ = devansh.address, value = 4).run(sender = devansh, valid = False)
        
        scenario += c1.approve(spender = devansh.address, value = 5).run(sender = aryan)
        scenario += c1.transfer(from_ = aryan.address, to_ = devansh.address, value = 4).run(sender = devansh)
        scenario += c1.transfer(from_ = aryan.address, to_ = devansh.address, value = 4).run(sender = devansh, valid = False)
        scenario += c1.burn(address = devansh.address, value = 1).run(sender = admin)
        scenario.verify(c1.data.balances[aryan.address].balance == 10)
        scenario += c1.burn(address = devansh.address, value = 1).run(sender = aryan, valid = False)
        scenario += c1.setPause(True).run(sender = admin)
        scenario += c1.transfer(from_ = aryan.address, to_ = devansh.address, value = 4).run(sender = aryan, valid = False)
        scenario.verify(c1.data.balances[aryan.address].balance == 10)
        scenario += c1.transfer(from_ = aryan.address, to_ = devansh.address, value = 1).run(sender = admin)
        scenario += c1.setPause(False).run(sender = admin)
        scenario.verify(c1.data.balances[aryan.address].balance == 9)
        scenario += c1.transfer(from_ = aryan.address, to_ = devansh.address, value = 1).run(sender = aryan)

        scenario.verify(c1.data.totalSupply == 17)
        scenario.verify(c1.data.balances[aryan.address].balance == 8)
        scenario.verify(c1.data.balances[devansh.address].balance == 9)

        view_balance = Viewer(sp.TNat)
        scenario += view_balance
        scenario += c1.getBalance(arg = sp.record(owner = aryan.address), target = view_balance.address)
        scenario.verify_equal(view_balance.data.last, sp.some(8))

        
        view_administrator = Viewer(sp.TAddress)
        scenario += view_administrator
        scenario += c1.getAdministrator(target = view_administrator.address)
        scenario.verify_equal(view_administrator.data.last, sp.some(admin.address))

        view_totalSupply = Viewer(sp.TNat)
        scenario += view_totalSupply
        scenario += c1.getTotalSupply(target = view_totalSupply.address)
        scenario.verify_equal(view_totalSupply.data.last, sp.some(17))

        view_allowance = Viewer(sp.TNat)
        scenario += view_allowance
        scenario += c1.getAllowance(arg = sp.record(owner = aryan.address, spender = devansh.address), target = view_allowance.address)
        scenario.verify_equal(view_allowance.data.last, sp.some(1))