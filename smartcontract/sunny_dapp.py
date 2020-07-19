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
from boa.blockchain.vm.Neo.Runtime import Log, Notify, GetTrigger, CheckWitness
from boa.blockchain.vm.Neo.Blockchain import GetHeight, GetHeader
from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.blockchain.vm.Neo.TriggerType import Application, Verification
from boa.blockchain.vm.Neo.Storage import GetContext, Get, Put, Delete
from boa.code.builtins import list


# -------------------------------------------
# DAPP SETTINGS
# -------------------------------------------

OWNER = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
# Script hash of the token owner

THRESHOLD = 50
# Threshold of relative sunshine duration percent on a given day

# -------------------------------------------
# Events
# -------------------------------------------

DispatchAgreementEvent = RegisterAction('agreement', 'agreement_key')
DispatchResultNoticeEvent = RegisterAction('result-notice', 'agreement_key', 'weather_param', 'oracle_cost')
DispatchClaimEvent = RegisterAction('pay-out', 'agreement_key')
DispatchTransferEvent = RegisterAction('transfer', 'from', 'to', 'amount')
DispatchRefundAllEvent = RegisterAction('refund-all', 'agreement_key')
DispatchDeleteAgreementEvent = RegisterAction('delete', 'agreement_key')


def Main(operation, args):

    """
    This is the main entry point for the dApp
    :param operation: the operation to be performed
    :type operation: str
    :param args: an optional list of arguments
    :type args: list
    :return: indicating the successful execution of the dApp
    :rtype: bool
    """
    trigger = GetTrigger()

    if trigger == Verification():

        # if the script that sent this is the owner
        # we allow the spend
        is_owner = CheckWitness(OWNER)

        if is_owner:

            return True

        return False

    elif trigger == Application():

        if operation == 'deploy':
            if len(args) == 6:
                dapp_name = args[0]
                oracle = args[1]
                time_margin = args[2]
                min_time = args[3]
                max_time = args[4]
                fee = args[5]
                d = Deploy(dapp_name, oracle, time_margin, min_time, max_time)

                Log("Dapp deployed")
                return d
            else:
                return False

        elif operation == 'name':
            context = GetContext()
        