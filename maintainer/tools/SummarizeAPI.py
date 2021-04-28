#! /usr/bin/env python3

from collections import Counter

from pydwf.dwf_function_signatures import dwf_function_signatures, dwf_version

def report_api_categories():

    class typespec_null:
        def __getattr__(self, name):
            return None

    typespec = typespec_null()

    function_signatures = dwf_function_signatures(typespec)

    categories = {}

    for (name, rettype, params, obsolete_flag) in function_signatures:
        if name.startswith("FDwfAnalogOut"):
            category = "FDwfAnalogOut"
        elif name.startswith("FDwfDevice"):
            category = "FDwfDevice"
        elif name.startswith("FDwfAnalogIn"):
            category = "FDwfAnalogIn"
        elif name.startswith("FDwfDigitalSpi"):
            category = "FDwfDigitalSpi"
        elif name.startswith("FDwfDigitalI2c"):
            category = "FDwfDigitalI2c"
        elif name.startswith("FDwfDigitalCan"):
            category = "FDwfDigitalCan"
        elif name.startswith("FDwfDigitalUart"):
            category = "FDwfDigitalUart"
        elif name.startswith("FDwfDigitalIn"):
            category = "FDwfDigitalIn"
        elif name.startswith("FDwfDigitalOut"):
            category = "FDwfDigitalOut"
        elif name.startswith("FDwfAnalogIO"):
            category = "FDwfAnalogIO"
        elif name.startswith("FDwfEnum"):
            category = "FDwfEnum"
        elif name.startswith("FDwfDigitalIO"):
            category = "FDwfDigitalIO"
        elif name.startswith("FDwfAnalogImpedance"):
            category = "FDwfAnalogImpedance"
        else:
            category = "(miscellaneous)"

        if category not in categories:
            categories[category] = Counter()
        categories[category][obsolete_flag] += 1

    print()
    print("DWF API summary: functions by category")
    print("======================================")
    print()
    print("DWF version: {}".format(dwf_version))
    print()

    total_count_false = 0
    total_count_true = 0
    for category, counter in categories.items():
        count_false = counter[False]
        count_true  = counter[True]
        total_count_false += count_false
        total_count_true  += count_true
        print("{:19}    active {:3}    obsolete {:3}    total {:3}".format(category, count_false, count_true, count_false + count_true))
    print("-------------------    ----------    ------------    ---------")
    print("TOTAL                  active {:3}    obsolete {:3}    total {:3}".format(total_count_false, total_count_true, total_count_false + total_count_true))

    print()

def main():
    report_api_categories()

if __name__ == "__main__":
    main()
