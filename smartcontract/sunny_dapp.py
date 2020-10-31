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
            n = Get(context, 'dapp_name')
            return n

        elif operation == 'updateName':
            if len(args) == 1:
                new_name = args[0]
                n = UpdateName(new_name)
                Log("Name updated")
                return n

            else:
                return False

        elif operation == 'oracle':
            context = GetContext()
            o = Get(context, 'oracle')

            return o

        elif operation == 'updateOracle':
            if len(args) == 1:
                new_oracle = args[0]
                o = UpdateOracle(new_oracle)
                Log("Oracle updated")
                return o

            else:
                return False

        elif operation == 'time_margin':
            context = GetContext()
            time_margin = Get(context, 'time_margin')

            return time_margin

        elif operation == 'min_time':
            context = GetContext()
            min_time = Get(context, 'min_time')

            return min_time

        elif operation == 'max_time':
            context = GetContext()
            max_time = Get(context, 'max_time')

            return max_time

        elif operation == 'updateTimeLimits':
            if len(args) == 2:
                time_variable = args[0]
                value = args[1]
                t = UpdateTimeLimits(time_variable, value)
                Log("Time limits updated")
                return t

            else:
                return False

        elif operation == 'agreement':
            if len(args) == 10:
                agreement_key = args[0]
                customer = args[1]
                insurer = args[2]
                location = args[3]
                timestamp = args[4]
                utc_offset = args[5]
                amount = args[6]
                premium = args[7]
                dapp_name = args[8]
                fee = args[9]
                a = Agreement(agreement_key, customer, insurer, location, timestamp, utc_offset, amount, premium, dapp_name, fee)

                Log("Agreement added!")
                return a

            else:
                return False

        elif operation == 'resultNotice':
            if len(args) == 3:
                agreement_key = args[0]
                weather_param = args[1]
                oracle_cost = args[2]
                return ResultNotice(agreement_key, weather_param, oracle_cost)

            else:
                return False

        elif operation == 'claim':
            if len(args) == 1:
                agreement_key = args[0]
                return Claim(agreement_key)

            else:
  