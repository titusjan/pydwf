#! /usr/bin/env python3

from collections import Counter

from pydwf.dwf_function_signatures import dwf_function_signatures

class typespec_count_attributes:
    def __init__(self):
        self.counter = Counter()

    def __getattr__(self, name):
        self.counter[name] += 1

typespec = typespec_count_attributes()

function_signatures = dwf_function_signatures(typespec)

if False:
    for name, num_occurences in typespec.counter.most_common():
        print(name, num_occurences)

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

cc_false = 0
cc_true = 0
for category, counter in categories.items():
    c_false = counter[False]
    c_true  = counter[True]
    cc_false += c_false
    cc_true += c_true
    print("{:19}    active {:3}    obsolete {:3}    total {:3}".format(category, c_false, c_true, c_false + c_true))
print("-------------------    ----------    ------------    ---------")
print("TOTAL                  active {:3}    obsolete {:3}    total {:3}".format(cc_false, cc_true, cc_false + cc_true))
