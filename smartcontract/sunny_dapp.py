"""
Insurance dApp
===================================

This dApp is an example of an insurance contract that pays out in case of
an external event, that is signalled by an oracle.

It has the following entities: the owner, customer, insurer (can be the owner
or a third party) and the oracle. The owner can initialize an agreement.
The oracle signals the result of the event, after which the customer,
insurer or owner can claim to pay out the insured amount/premium.
The oracle will also be paid for its services/costs.

In case the oracle fails to signal the result, the owner can refund both the
customer and insurer with the 'refundAll' operation.

"""
from boa.blockchain.vm.Neo.Runtime import Log, Notif