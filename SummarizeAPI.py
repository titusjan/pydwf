#! /usr/bin/env python3

from collections import Counter

from pydwf.dwf_function_signatures import dwf_function_signatures

def report_type_usage():

    class typespec_count_attributes:
        def __init__(self):
            self.counter = Counter()

        def __getattr__(self, name):
            self.counter[name] += 1

    typespec = typespec_count_attributes()

    function_signatures = dwf_function_signatures(typespec)

    print("API summary: types used in API function signatures")
    print("==================================================")
    print()

    for (seqnr, (name, num_occurences)) in enumerate(typespec.counter.most_common(), 1):
        print("{:2}  {:30}  {:3}".format(seqnr, name, num_occurences))

    print()

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

    print("API summary: functions by category")
    print("==================================")
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
    report_type_usage()
    report_api_categories()

if __name__ == "__main__":
    main()
