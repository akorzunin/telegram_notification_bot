
# import __init__
from modules.utils.util_classes import TreshholdType


def check_rule(
    treshold_type: str,
    trigger_value: float, 
    current_value: float,
    ):
    if(treshold_type == 'higher'):
        # alert if current value is higher than trigger value
        return True if current_value >= trigger_value else False
    elif(treshold_type == 'lower'):
        # alert if current value is lower than trigger value
        return True if current_value <= trigger_value else False
    else: raise Exception("TreshholdType is not correct")
    breakpoint()

if __name__ == '__main__':
    import __init__
    from modules.utils.util_classes import TreshholdType
    tr = TreshholdType('lower')
    print(check_rule(tr, 20, 19)) # True