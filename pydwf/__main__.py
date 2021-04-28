#! /usr/bin/env python3

"""
This is the "pydwf" support tool that can be executed as "python -m pydwf".
"""

import zipfile
import io
import base64
from collections import Counter
import argparse

from pydwf import DigilentWaveformsLibrary
from .dwf_function_signatures import dwf_function_signatures, dwf_version

_zipped_directory_data = {
    'pydwf-examples':
        "UEsDBAoAAAAAAIW4nFIAAAAAAAAAAAAAAAAPABwAcHlkd2YtZXhhbXBsZXMvVVQJAAPKzYlgYs+JYHV4"
        "CwABBOgDAAAE6AMAAFBLAwQUAAIACACFuJxSPl5CQVsFAAC7EgAAGgAcAHB5ZHdmLWV4YW1wbGVzL0Fu"
        "YWxvZ0lPLnB5VVQJAAPKzYlg1M2JYHV4CwABBOgDAAAE6AMAAJVY3W7bNhS+91OcKheVUkdxUnQDDHhD"
        "1nZFsC4pmnS7KAKBsWibgERqJJUfBHmnPcOebIcUqX+7joEgEnn4ne8cHn4kdfAKjkslj28ZP6b8DopH"
        "vRH87WTC8kJIDZrl1D8TuS6IVHQyWUmRo2l6vwLX94GtWUa5/pvc0ZWQufrMbiWRj5VpSnORlJplTDOq"
        "/JgV42liu1J6x5Z0Ch/w5YN9vhD6d1Hy9KOUQk4mKV1VIISTTKwThk8FC6u388sIjn6BC8HpfAL4C4LA"
        "IHGlJdHoT28onFlTOD++hFXJl5oJbGD6MZ7YIdddk7Mv57AhCk5+hpxiRlI1hZN3IFZwv2HLDaaCQqlo"
        "CowjOlOWnIM6hCqEo4ze0cyPn1edAEcgqaI6jOr3peArti4lDSMY+4WHEVxcXn+cAxd6zK0HUproUiHy"
        "GI+AcnKb0WCEUNVzzleixapqvOowrdo+jbRd9Vz38llNMKiyMDOvIC8zzYqMwnJDOKeZ8kGYcSuRZeKe"
        "8bXvhX9KKh89cZv8Qoo7ltK0FYUzfo9l08lu1XxBcjpsdTE70h8JTq33ibOimEKuOOkEeJnfUmmefT8X"
        "Kf0BbWPiuBOeAs76njFc4MBxwqanN1GtHpytnZ3DAtu7tlpA3flve7BFsIOBLxK3SKu4/SKO/bqwrWFd"
        "f1dV0dB02qm1ujmCRYMxKOW6ZIdWTRxt3KFdt7YLybC+gr6NTa7ynCD2P5jD03MQG00keiSoKNqF6jwP"
        "gEdRe2nZBWxDb0jGO+mi8X4s9wGrjDt4Ua8OvIwBHMBXiutHaSdtUBYpKrpdklnWEg8L4F6TpVGA9jSO"
        "KIOLZFymjPI/Pdfw8zqEjoexGNCupoG7G30wq0kSvqa9sfOJX4G+neN6HyFtZaADGdVDjb5sjdauge5A"
        "k1CbhJacdWSszst7p2AHmIYQ/9CwlZAIDNnUNLlUWZRhnqzbaTcjb06m3ZmadlIwbUUVRT1e0aRuMJm2"
        "lr00t0Y3Oa6TZZPsfiO59rLb49/4iYaQDPO8G3I4Ez+ARBmsYcchvdC/BHWNGribqFGFF/G0i7KiuoVn"
        "syO8HHgXVac5e4K6qq7xO2UdNXXbjG9jwRs42VKWPfBunXW1sKWEtckeSDa5u5GMyR5IdVVtR/Ime6CZ"
        "aop381rTfVLVLqJttBqTvQFhFzPV3oQGEjNy2cDDoGa8FMhCUpKKUo/dPTq7UFU6CzhF0f129Rv8KTjT"
        "zfbQ27P2V//vsxs7kq26g18tIGj5CRr1k4QpCl+xcvEyZy9UYfCN04eCLs2Joj6tIkocdE85Dswcag32"
        "ncg0WaNGL0spqZFuc67VNC8o3rTwBmOyHozsiwfwWYgCDIUMtVpTKcsCnVcbD96p8CpwLUvakN7/NFAP"
        "KdVtYhiqF2nGLOoAkLxQLxOdkwbAZOLlqnXa3+aCp2c8Oc3jn1bP8P2vG/P41jzmZ/b51Dz/9+/7m8F+"
        "W22gdR6mTUSHcDKbzeLZ1HJsVb6piVhllBbhLH43m7n6zwnjYeRK2t76pYnJfQGIz+S6zLEAvtieEDf/"
        "pWSFuVQv2ldv9I/lYmS2uYKf9y/gvl4sVEzSNCEOPXyNLYxgXPa48hpFGLvU4vWv+LihWbEIKoPWecY4"
        "8h8j3HnOOTBDMQbnx/4znuqDvZaPTfmZTxuLrV81wiZ/90xvBl8yQhw+tQ7jTgQREOVIdQ8nI982KrO4"
        "lpld9iPyNDqcPixpobd9ZpkPToGizFJ7MTQBWqfgP9XQB4Yu1372HPIf9PFWEJme+yU+wPQWjQqYa11q"
        "FMZeOI0AobQltpaTBBYoa0liyjFJnKZVtTn5H1BLAwQUAAIACACFuJxSq5kc3P4DAABXCQAAHQAcAHB5"
        "ZHdmLWV4YW1wbGVzL1Byb3RvY29sQ0FOLnB5VVQJAAPKzYlg1M2JYHV4CwABBOgDAAAE6AMAAJVW227j"
        "NhB991dMFRSRUVmRuy22cOEWadICQRfpIg3QvAmUOI6JlUiVpHzZxf77Di/yLc4WFQKEEmfOnLn74hu4"
        "6o2+qoS8QrmCbmuXSr4ZjUTbKW3BihaHM9PPHdMGR6OFVi2J8vUC4t2teBYNSvsPW+FC6da8E5VmehtE"
        "Obaq7K1ohBVoBp2FkLz0VxxXosYMbunl1p/vlf1D9ZL/rrXSoxHHRQCpmSw7rayqVVOyTqT0YQyTX+Be"
        "SZyNgJ4kSRyONFYzi2CXCDfX9zBowaKXtRVKMmKzzUde55GEnAuWNcfC1+/vYMmMR1moplFrIZ/hLbRI"
        "ceIm99rXTQNq4WRaChJCb5BDhSQc4Seg0aBNx/DimcS7/+QZccilvx1SBp1qmKYr/+pwHMoRAmWLEVHU"
        "ZlC3m6isw+GQhsEGaws8hqET0pDLGiiM0rTCQvr4NAYmORGuUawQ0gf6wAW9Op4HRs45GozswDizDHxx"
        "2Bh7Vz4QKmHn7VeQBhIeSEirzgFlMFF6ktE9VR4F8iMOehrEAmrWNJSqtbBL+IhauRLvW1LPh0oK+aMi"
        "y2MGw4cLoPD1nQ93rdq2l6JmLgg+YtPvf4QPlbDmymCd7xFi7ui6KIq8GO9uDlNZ7Ey8U6qrWP0BHp+A"
        "3Ht4yqBSxJSsDEm6u/rLJQouChcSqUAi+UPCtZLSZZNBt9waItdAM8CtKWN7VqEkDsjozTGN31xDIxjL"
        "tHXF7yIds5jBGqHtjT0McLw0xoWj2vogez1Kjy+N0Dsh6qu7W8B/e6JHsJPpIa10Ms2g8H9VknyNTkzp"
        "WTburrNnqOhTKsaJF4FBSrwywI1FyZFTu9BAsWTAFVvmbNvejGEe43WSM+gljTpXk6h131nkMwLokNLP"
        "my31GbXQYRu1aAx7xtg/gmALf1ovqZThUfdxsLknypJMQrVXfpoVP2w+J7kbucymAr6FYjOl6irGOcpa"
        "cUzHO90Y1unbIawRbC/xP93+aa/ZaXI3TR6CS3zH89Nn+NkneU7HPXR8DfjxJcD7l51DwfArrCKfPQm3"
        "rHLTIHZpkVMU9jcCvpvDNOyRlgmZjmchY36haTI6LLf8Oo6A9/4m5WhqLXwFzY/2Su/9C2P/xc7Ik/EB"
        "fM44L4fRkl7SFyrOUvZthfoyA0lXZn75Kx2X2HTzJAhAEBhMnEy2oSGcLtGPhvw/Z8oMk8rq7b563MKe"
        "v7qrD0rFN8Tpfk5JPfMG8yMXaCmYyGpvyps7u7HjiI8j7Ib2t1fCjWvU134CzE4r7Ub1DaeJF35GeFO7"
        "mY8b4UbDkISI/CduK8U0vxv68gXmILFvXcKS3E0Mh+/wRrQ1ylLSWi1LmFMXlqWrp7JMAloortEXUEsD"
        "BBQAAgAIAIW4nFIP8NTTrAQAAKUOAAApABwAcHlkd2YtZXhhbXBsZXMvQW5hbG9nT3V0Q29udGludW91"
        "c1BsYXkucHlVVAkAA8rNiWDUzYlgdXgLAAEE6AMAAAToAwAArVdfb9s2EH/Xp2Ddh0qtq9hsMawG3KFL"
        "GvShyAokwx6GgaClk01UIjWSSuIW/e47ipIsyXbcIDNgW+Ld/e4vj8fnz8hZZfTZSsgzkLek3NqNkm+C"
        "QBSl0pZwvS65NtC+y6oot4QbIssgyLQqUCK9y0hDvhBrkYO0f/FbyJQuzGex0lxvp+SD5Lla/1HZK5XC"
        "lFz+eXU+JRd32bXlFjxSCoVilRW5sAJMC5kJmbKalMKtSFD2Al8u6ucrZS9VJdOPWisdBEGSc2OI4UWZ"
        "g14EBD8pZIQxIYVlLDSQZ1OSGfxq+LcCmWwjz+Y+jhpnhiyRY7TYcjta+zxk+YqkGXneKCdoNNwHnQVr"
        "sMxTTGOEXCCP7Wm3CCDLmGsu1xB6zGmL/YrIiJy1FnYyKbfcixkhQ0tejs19SSh+kV6KaGzvKxQMukUN"
        "ttKyRgwCZ3Idcl5njanKlpXFKBqrqwLzy3gpQt6mFL2ocZINlxJylmBOnDsdQ1yvhJFnE9mYE0O3C0Sp"
        "MTDh5GYDxGecbFy9qQaOeGNaCEPshuMbl2QFpDKQEiw8XBSmdiGeRCMfvRE72zQYsOHreWPd+ae5S2Xz"
        "TPF57gl1ZczfUXgzRpBY0h8lX+VwjUgIMCr3+JxrLUBPyY2uIDogfVnJxAolT8m7bRN/yfn2IEib9lMo"
        "mYlOuUCf6AL9X1ygp11oNjtLNi5tzVvotvh8NpvFs2jERQ9xzSPcufhHPn0jhdLYY4wiW1WRO5HnuF8A"
        "3wvAmpJrLET52mDTEglREusMaYkqIW42u9+RPavi/t5/O3v3yyG/XTwuUPTBtDns6Iga+lg19GfU7KQL"
        "bizoLito5hg/UTIT60qD96EuE9cPLdfWo91t8GyoCYtd38EIMRfOygwahl8KOz2elT7ISqMdLJ4DgIdH"
        "2IdfdudNfKPFeg0a0giBUsdGH2bbIdeQLkYM2yxWSveaK2N7r4nSuiqtU7E8kIbrzsEjiYj6GulQIx1q"
        "pI/TSI9q7FTWLbrnF3nmTjfsq/vu9Uj0oAA9JLBr972W7/awz8KCfF/MZz8Gv27vHqVOYjducBsOcNsC"
        "e0y6pgcQHhn+XiAzgLTpTbPxIq0XD8bcaSLvh5qHIdvnXhI6e/vrYs/8ngkDiY4RD9FD4PQR4LQG70kM"
        "3OoseH8k8Tc49JgMsAqxwX7/0fQ1PNpVe8yTedyluIWLogHWidbbSQ2EntaGh/7Rp/hH9/yjp/yjh/yj"
        "P+nfyf7vZsCC41jZTnf1PUC71tLcCeIPel1Pg19qSpiCSbQo3RCwnLgh3Y2L2EZ3iggeElbISmGfLdGW"
        "FU++EpW1Q7PT3M5rXlvM05TxRk34AlcEzxleQlagX+AQjSSzfPEbPm4gL5cTz0A8g0N253N7KWnGyUl7"
        "uKEsetMoqv+cKtOOqVZvd8l0d5zl0etNuAv6nbCbvTtLiOJT0p6Q3EWIZcJKMIZlODctc16sUj7iQJM4"
        "Th2gseEdo/w96YL7e5VhiV2LbzD5J3JXNK97WJCnp3ovFe+G+1oe7hMo7bGr197wfq6qPMVRyV/faq2k"
        "vb7BPd7v5NolOhDucibRF8bcwTthzJUcYxOP6Osv+A9QSwMEFAACAAgAhbicUiUJI7TKBQAAJA4AAB0A"
        "HABweWR3Zi1leGFtcGxlcy9Qcm90b2NvbFNQSS5weVVUCQADys2JYNTNiWB1eAsAAQToAwAABOgDAACt"
        "V21v2zYQ/u5fcXMwRFod1bKbtDPmDa6drkaT2IiNdkMWCIxE20QlUiOpOO62/74jKckvadaimJFA1pHP"
        "c688no++g+eFks/vGH9O+T3kG70SvNtoNJvNxlyALDjoFVOQ0ExALsVSkqwFKyE+QpED4TAY/XbRfXEK"
        "WuBGCgNOUrGEEVOxuKdyA0TBQqSpWKteowEAv0pR8AR+OsHPz+Wbkb9/BuZTyt8Ph0Y4Gk/a+DhxwuHM"
        "yLyroV/JTmB8NQ8/K+2U+O4WPxtNSmFnVzgoheGOcHhhI9BgWS6kBs0yWn0ncpkTqWijsZAiw4gl6wWU"
        "ayO2ZCnl+gO5pwshM3XB7iSRmxaM1guzqEk6KfQ4SalDm7BGhWYp04yqimbBeBLZpYTes5giHF9G9vuV"
        "0G9MzM6lFLLRSOgCFNVRLhRS3NNIFXmebqJ7kWqypB6x+RhPWlBKerBIBdF+z3gN1XIQrwjnNL0SCZ1R"
        "7bVbgH+h/6VNYc17sJVycpfaXUhirbT+qJxFWEVaxCKNSM48FPiuMAADbtzkSkuiqa2m2XQM1XZYFDzW"
        "TKAGpjdwt4FYoDUo4ktTfTu1SOKYpinFAFNNJcaHKyEDp2WOtGUm9ukH+LLCag1/BIStRKKCyiyHPIIP"
        "FArlLKtUMY7lXciTNZPO3AyDA97leDZBixK4nMzGWDIUjcCqMX6ljFPll9YgIhrOOEAf2kaDYYhXLD9R"
        "NEXX4GY4g1vwsDqhDD60/RqJZfoOkWGNTEX8EdznBhcPkOEWac3qQ6dC2vcaORocIDs7SONZH7o10rxv"
        "kZMDZNffOjq/HlzN3pxfz3+fnlsLKrKw3vJ6PJ9F0/Pr6MPkeoQrr/bCFM3mg+u5idWBdDIFS7Pj3+jc"
        "WNnYZUbK82sbryO4nL3GYyaVdjuwDANJ8SB5/lawkPTPgvJ4Y8r4tG0/Qds3aPLAsiIrA17vM4UnZFIW"
        "ZEI0UStKdbCltABDV6XPd5HDWLqEO8ac8RpiaMrTVmXO34PY3H0OEbbqjB0gTNgNooawJK2O9KNOFbxl"
        "y5Vv0VtlYBC22B9xhF/kKNXvcNQkWdlbqiSW8UHkcDq56CP3cPp20A+3CAw4lRWkyrLvvDUHcD/RppMH"
        "KqU099pB2G6X6c4l43Xuj+Dcdi/sA0QVkmbY0RV4WB1wfOlEx3DHtDn808kHrNbh/AIkXTKF7cYPSpI3"
        "Riv2KY39e4Xug14LA8M2zxMWm15A4HgtmUY6kVPsDtjdQCxQrLCG0AADDmpPXU/wyrLHDu2XSdV7PQNL"
        "z50PLOgc2ynFkjdwq+maksR7+jC2Hp/CFty0H9pt+BvaD52kBa9u/SctCp+0KKxCeyFEDgXHKw/DgOGS"
        "Ra5p4pxcr/D2hLksaHklOMiUSnOZoj8kEYU2EaqCrdCobgeCwDxfBjugr4u+oTwIflakmuVl8NWW8lsy"
        "8D9nIXZZ6Hbs7bz3VyblmxNjL+8HpkzvQEsro2/C3svb3R245lX7btq38KxG3YS38AN0Ts9Q1u28PHvl"
        "w/dwdnraPYMTJ9jSbPZoOns03a+n+bRH82KP5vSLNDWPO/zNP+QNxuu2utp7xtu/emf/GHPd85N9NgNT"
        "jUSj5hau4f8nvwXYa/rNZgunq0Kt+qaGy7knI4x71YxjJ0eJZldTZDCQy8I0mKld8RKqYslyU4z9vXGo"
        "UDhkmfp8NBeZwWXN9OrpCSho+jvaA5IkESnVescoYSSNeJHdUXncAo5Lqn/8C35d0TTvN90GcBsqC6pJ"
        "F9yE2ixbp8Gid6Ui+zCqVNVatdz06ribwbn/5MzsbSvaenc4FHsIb1mFwZ4LvvnJ4bZsVdlz8R9jstsf"
        "bKflbtD199CfH19LXOIuuxkOsxZEH2Ka66em9t5h5Q1FkSbAhZv83W+tavKnD8xMuFUKS+Z3dHMniEzG"
        "VQt9xFnt2HZZW6NmNjH8hq/BFhBFnGQ0iqDfh2YUmWKNoqZjc5Xb+BdQSwMEFAACAAgAhbicUiGc+kDP"
        "DwAAry8AACQAHABweWR3Zi1leGFtcGxlcy9BbmFsb2dJblJlY29yZE1vZGUucHlVVAkAA8rNiWDUzYlg"
        "dXgLAAEE6AMAAAToAwAAtVp5b9vIFf+fn2JWRmGylRhbixSoFyqQ2smuga03tdMERTYQRuRQIkJxWB6W"
        "tYt89/7eHOTwkLPtokaA2MN59zlv5uwb9qKpyhebNH8h8kdWHOudzL/1vNlsdiP2ksmE1TvBXuU8k9vb"
        "nM1KEckyTvPtjO1lLFjS5FGdSnxP62PoeQ/Nfs/Lo7fQP573bpdWLCZcW5GLkteiYlW6BUDFZM7qgzTY"
        "f2pqluZVXTZ7kdcs2vE8F9jE85hFvKibEpBgZt8HA1MdlGeh5ixOqyLjR3CqJABwk9WMAx/blrzYsaai"
        "b3teF5mss3QD5t/IEpstv7VkB1l+Jpg0r0Uei3jOIgn8ERAp4gvZtJyys0sCMR/S3F0nGToIr/2yPAGx"
        "BDM3oorKtCDlWm1qjX7Yidxw37ONo7xDWu/Ux9m9steM8ejfTVqlhE0Zbs4OghWlKHgp1E7NBZAUjkjg"
        "2/PTBPqo0lLEAavLdLsVJatEXYMB6Lkmbqqal7VG49DRPHJYL8s6QW/zEEpM0i0M6gcQ9E481YodcA7U"
        "nGVSFuywE+AMq9gMUo1squzIElFHOxbzmrOklHtF0pF7c1TEFFlLDLzVTeW/KxsBasod8Q+SC/hizBpg"
        "z0a7A2yAx+UVuzkkD1gT4Y3MRcjuZE364rV2lIxXNWthlKBwbPhOyfMqEWXluQpRfCvgXIi4Ip1syAoy"
        "ElUlYujiVUIqIKl6SJV6toICJJElfJawURgMNK6BXDXoFe0F0DZT8tNHzwpY70ohWN7sN2D3CuqGRioK"
        "fP7I04xvMvhKJiuYSEWiLMumIMVVfF9kojJhU4gyUXHRcaN8Q4FqyEZBWgLVTjZZTPL/IkoZsttkJE0p"
        "8DtF/V7CFTZAYvya517Ec4LlUSThzsqSRh//fPjbYskg/GfSL63E4jGNBPPTUISaKc07XAgURB4dySNq"
        "Kdku3e6COYM8cHqo3HE3fPaqTB7ICcnzZFPCwWEsmA8JZa9MtOdHhAa0KfMFiWWEhY6UeKCy40Uhch03"
        "LJaR8lttTyB6TBFpgGbbJo15DqaxDnHjTEc7EEgAlkoHJF7VIByr2npkT3+ekZJyrqNuyIDIipU5X0jt"
        "bMYF7S5HbKV6oIw+Z0fyHkTpkza85Tcmd4vTbZpRAh4xdIBKwKgSQilG6WVGbjGzPqTVz6rPacHkow6A"
        "/XdaXvw7EK4DqQv+b/klnUMcSOP5SZplNh0qf7N4lb/c8buK8syrqmr2vW2OQ1u3pHRIHGoDnbcxcK43"
        "sG36qMuQiRgKlEcUvzYeurABs54mhXhj/tvrRQV1BWzTJMgMSpmVaMGMQ8tNzdOc8pJKnhSpWjcqjm9g"
        "Eh8O2v219JW/et3K5Z91nENLx/iQIBI2JSoyS4kOeZtiv+pKt8oXO/5oVLNHBiOW4TQc/pUkaZQCKjuC"
        "/V/AmBLHg/TFEdoq+XGOQOWxVaxxOuU8KJswmckcOt/obbCnAiWraDdBebXNRi+F6Jjl47RouZ9O1HMj"
        "Y9VsFoqSsqyHWkKC5SpfgLdYZKnxNyBE8rYho/LlBEOWYQhQSIinoh6tRsSxnbL/ptHyqMLgazxrRMYW"
        "jvhHg37d5p2gNb9CCfaqOq2bWpieBbsqsOq1XRfTqIx9sSzUauvvVDNpFVLFXYXUCXDeMpekJbhLxKEF"
        "pMQF79vyEo4bzz0yGO2sZQ3f7Vzd7m9pHBB6prPLkBrFUyREPIiPDsjIAweWe1Gne6F8j5NdKDZKFTbo"
        "H7cpaZpkNLolIW2SQkZQNZZqqDbjnn8mU5eiSzu2USmkKSaUSnJ4NJQWp1GtKGm3BN64iWjBQ8cYocjr"
        "KuyQ7pRmZRm7BjFCJbpnOWOvuYOhFHtEOLDa/EzyGKahkTnbC06yxMRvBcPncTU3Xq6TbdeuoWExgr41"
        "cj7024ZSZCguj2RIz1XLXlImCKnP9zxkBllSRG7RDVbC/k3c2N9NuKM2FXbJ6ZyLI/1Gn4us9jzldzr5"
        "mL03pjx84I+CGpjqR52U5l3vf6ea0jf/vLvG4vU//v7Tzes5e3d/+/3D/bX+5d2/3mIJYf5OC/GQyULM"
        "27gH8O2P717fa/LUwa8btHbQChUYzUeS5vFafbIhQaecG/U7Ors3SPHx67JEPvVikbC2T11rda/RvKM9"
        "9rlles66D11U91bJxghpEs5ZlUmCFjq48hh+YIRrS4naZZgyF+aQRA2A7cYvdSJFVp7+vgyVOQnl9Q+X"
        "bMUu2Jlp+MwOFa1wapQDzs41oXPbGOl0Ijp05Gt/uYAqt+gQqYRqzEtgvnwes8IbalZyOiau+oYOr7Ez"
        "FaXe0aozRLMnan9xGTDgv6c/2AYNT3sYDIcAhPx1TrH7gL2M+RB8rkjCZ6jjn9j/xlQOgnD3k++FD+B8"
        "EsgaF1Au0JT9p+BfWTc4Dd96yhT8T8phxkKOfWoC+O2OV0ZBPeC/XIQXwW9Q6fK/VOnyf1Hp8neqdPk7"
        "Vbr8PSptgTuNnrGHYx7tSpmjbTKJvA0X1ApdDcyCOZjhZGDGHLoiHHVc6eN1le6brOa5UEfhcMDUHg0H"
        "cqJVBazc8aHAde6ifKEp+5RLNFtBy8YAaXdQV16jza9zY9nkKpP6thLNR93NnPX6n7mtPusk49u5SWCO"
        "jdtsSHptCjuS0IzPu2w8mlfovEhHUNSW7mjvFGc9Rioov+S17nLVFCilMnns8iaOfS6TmiP6sattP7Fi"
        "i4vwJXq6fo93xmwlphbB7RncWuy2KCF70MMUdMr0aRIthKx6fc2OZ4k6WmHNTMfgK3ksD+GI50w8wuXw"
        "syL3ZKMfpHKDVe9E3/FeZrXNtmfMqU7ulMgZvPRbZKcCuTVDf2gHeyuTi/DVuCrMZz+vIYt4Yt1QrOps"
        "0c2R9Kc2W/k9YDddTYG9STMTMQMw3UeENyJK0eQ8g+Ge51uVBIYYXg7yKkAcDf1d6pxl2pxQT2eC/v7E"
        "yY6auj86PfQhtMf8qBzGZLWeEwVfcfEzZuLO+lhipgMnjB46kB+EzlQW1MxiylSPKWkaZuIQUUHu4Kvp"
        "pO5AZtbGAQ2jZLPdsYv34VjrBvmDbMpIKdC0h7BULaJalnYUGpyEvdaETJo8ve/dsWgpUN8Zvo634hm0"
        "SKKpKYD+oEMN79PqGdC2cQfkMMmchvqRAtUFUZF7ev8PR6oOokorAkIWuLwI+oHNqr2aXu7VmANW2rUg"
        "/SPWgYZSmZ5zGfsKKMfJFjyLmozmB+MjILmU4NGunzBUm9js13bXipXUiY8cfpgW2wqHWkXZS8ri6vky"
        "YApct7LOS5Wm1Pphh1OKyhpXzOt02d/9J9393uZRKYa5z0gcdsBFmea1P/v465dP7L49xf/6pdVIGIaz"
        "UA91/T6luauTIPCccLuFE1t5yQLZYGpijufOoHzqloBKorkmQe1xmO7s8PFTt6pmAZaftRqgrQaL3XS4"
        "1Wk/b7b9xBsc4W1D2fUovVm2Nrpw+HLs0y0qhvXcezU99e9t9WkODelbnp0x9/CTHnsPV1shgzFBO2jv"
        "szehOXjRFLVnwDrdTsC2H/uEkeunqLBvYJ4rb9wHvKLhdEwT026cSYd6HomdzGJR6gh2Z6zhBBrVyyYy"
        "y+RBdy32/G+HxyEVjB1/FPl5zR5FmSYp5DqK2rlaSSs76kVED8bIzzNAX51ckhchzfZ8f9q8y2BOW3Ke"
        "ByNMloQa2se+izj4qqa7QfBX1N3Nx7gZ2g0OvWPI7hrqIDRcN3utEDqFummluwqbcA227yaQfRD6Fq9o"
        "TGus5rYGoWDLGz2s1dP0ascL8WwULYMxx4Pt2iqPiJnos/9xEENqyD1oqE6SC55vGj8FoWo+UFGF/1X7"
        "DqiMTWzzzKo/bb6aVmo7JG0HwmZqaMbLz0SQsa8dCbqTQINDHy3cqwd9CtrAGz53o183o1K9GBM72Q/2"
        "UhHYwGl4raga/bjZ78QUcoQLJhH/FQW0KqPtSsTONiTAOMGOY84txQv24dX93e3d9/jNKcZqfk7g36BY"
        "x000vik8XazHPLg1e8Rkl87/J04je53X4vndLHd1rddrXHd3JuqGQyEpnQtgdRdh3lfQLDtnfk5ZwGSN"
        "tvsjZ21cd+8lA+dqxh/HH9SH+tF+YH91e6O+8szYfq3v61Z9uIUL94zO73569xr/OVcAVP7gVjABBHIM"
        "4f96FV4mX/4QfMc+C1H0u7tO9SMnHthi9L0nxrwnxZxdXtBB/o8DWV+wwbYT/WNf9+a3jz1cV596LtB2"
        "9MaSFKykB1VZTEIaZTPVHk5F9Z/I3rykw7PvMhxAgmHL73TSWR1GWeIkFVrZlmmv3aK1Oq0z4c/altfN"
        "gWe/fvk575nvi02tdAuDv374Jfg5N8P1lo0r/WXanM+07aMR2HhGNhqDDbLGydxMoj6hCIrMnymD9AZM"
        "5iD+sfr0c27+UG6c20ObuofvTuZkxnbyP+uUPM7YLt3e/RfxAHqzgTmOZq/R6cf3vR2/QcR079NQbDQV"
        "o2nrePXrrGt8FxP4LidWR9IQ+LfhxZx92055fpMg/OkxS3NBp280NKvz8jyY2LNTe3rH+nZ3jxG6cvPr"
        "eRu/V2ro+4nmpJksV+dSBdg5UgepfzVrb5HQvMkqmAVfx7bssG2Qus8ZG2FbMh/eFAxtnomtbpij1awp"
        "qIGHQLt6uK3gDfqyS7H41o6V6W7UD8zxTl1H0vncXk2Gr8qtOru+VV/8uHsjt1IPFulwqwqVO7Lqbs/1"
        "+6E2GkLLjyYU8jhec0PBny0WWhmLNjRnczZbJNUMaqiPhVglmeTQGfjmKH4rZOWLC2XdnciK1exhUIh1"
        "H2dfz6hXdJR4QmOKE0xo7hfaGWeMbDBblDN2gomLEGxYDvRxtL2E7trIr9BELaDmemFUNVM0nxRNHmlt"
        "V7UskcfoGD+z5G40WE/DxFlVr2YWlZ2LllsqPoa++o84qGwup8vj1cl7Y7urLo9X/SlkJTJ6htZ1yHbk"
        "oN9YtQ8j6aUX1fPukNbWi7+p9zkP6S80mOxBg00ciGoa8LQjCUI4vFb2wf28D4sKWOeiqtb0bmWV8f0m"
        "5oMdLXb1Cm/6y8cpLj8FdErXpAeDkfYqB8rUG8J2aWIjiuVw420+hbF/OweYl6jdZL9weB1Ck2Geq5sN"
        "mhi+1O9somOk3n2NnzAOLzEGNNsbPdBchi+nThJn7EFXmm6vudHQrer0c2O0rbEEe++Lgp6nKOTvXRT0"
        "SOYp3Tf7k7zp28JnLloc3sxey5g31Yva6Wz3nNVe4tkH1L7uV/pDxKnr00H3939/2DCYf6EzCKsM7bG/"
        "RM1UocrTWh3dOdvoey9992kfeW3o5caxfWYzJf1AaRMXksohxx3X2E/NmslRz11B0wOnoj71bOTKG5mQ"
        "jmm51E9P9Lty+/REPKW1LUJoHtbrHEG+XtN0YbZeUyFcr2cao66K3n8AUEsDBBQAAgAIAIW4nFKrIyTW"
        "XAUAAOkMAAAdABwAcHlkd2YtZXhhbXBsZXMvUHJvdG9jb2xJMkMucHlVVAkAA8rNiWDUzYlgdXgLAAEE"
        "6AMAAAToAwAAlVdtj9pGEP7Or5hwqrAbcAwcNKIhEYJri3pvuqNJpevJWvAaVmd2rd31AZfmv3d2bWPM"
        "JZfUSmQ8O/vM7Mwzs3Mnr+BNquSbOeNvKH+EZKdXgndrtXq9XpsJkCkHvWIKQroWkEixlGTdhJUQD5Am"
        "QDiMJn+fd097oAUqUhhxEoslTJhaiEcqd0AURCKOxUYNajUA+F2KlIfwroXP+/zLyD++BvPk8o/jsRE6"
        "l2MXXy37wPj2uWx6OWt/Vdo5lr6H28mVEU6mV+1D4SgX+sV2FI7PbQRqbJ0IqUGzNS1+E7lMiFS0Vouk"
        "WGPEwk0E+dqELVlMuf5EHmkk5Fqds7kkcteEySa6Jhi7bJOJZpBqFjPNqCp2R4yHgV0K6SNbUNyFHxP7"
        "+1Lo30yozqQUslYLaQSK6iARCiEeaaDSJIl3waOINVlSh9g0TK+akEsGEMWCaHdgDgvFsrdYEc5pfClC"
        "eku14zcB/7Xd7ym197hHqpSTeWy1EMR6ac/DOosAyaPFQsQBSZiDgiakigYk1gEJQ0mVGsBciDj3EKNv"
        "Ds+VlkRTS63b6ykUIBClfKGZQLtM7zzLLJihksmAJjFMO+NSeYQ7V0jEdhvWFAkeKq8wku1k0TNnrNyu"
        "oe+5EIbgb3tdu0RjRb+t1A4zYHQjQDIZGZzsnUsYhxO/VJiMUKF9rNAuIcYXk+DmbDQB1HMObb17h9mC"
        "f9Gi71e0P91MZ2cvaOfguOrhEubLLQUYc6oXqzyLezXMgxGd+ubxfBf9vSBbwG94+OMJyGIhZMj4smgF"
        "IdFErSjV3oEpEl6ShyNktYiNJI/VgTwke/lklDtoStFTMaWJ43tt38/FJ/CRShbt0DLRsKENiaQh8UPu"
        "T9mocq7goRNkF8UQGVMbyTS9Qe+cw3A34c4E9n5fElldBizEbQXCXfv+zr/f86hUeWWIQHslSRLJuHbq"
        "l2LfNCPbCwW3dC2y5G8/D/zO9surumd6CNGHOXTdI7jy+yUSH5ifYVPGts5NZDYMqyHVNl2tFu5u4e5W"
        "4YhITIV9qJcmqqR/AfS7iHsQpFoqefadg/1QdH4F22uMwTUlKpV0jY1XeS8ErQhYTpgz26squ8HBUoDG"
        "RSZqwJxpwFK8vvp0dhOMZ+fo7ZIpTaVbctpSx6nUneVNJ2yaQnt7vzd4LkQCKce2j6AIItNE0zBD2qzw"
        "4oCZTOmgjM0JGEpCH+Y7jdeEvTqK4BSeHASm28FgbYgs2tv/43m3gzzvl7kmW6ZMCVepXjtYN+2l0MIS"
        "gNf7PagIP0On10dZt/NL/60LP0G/1+v2oZUJSphdBaZTgen+OMxTBea0AtP7Lsxxjf4j7zBA90W0B+a0"
        "nwf9L8bd7P1k33u2kW0T1/D/k9tEZobDer2JV26qVkOT1PwyXBPGHTfPsJ0iJLpdTBTeSC5Tw8Nru+KE"
        "VC0ksyUzrNyGqcKbF0Rkq+zZTWfr72Ayw8ZM45gieSjyxcvLObPuIXsCkpt1GihhJA54up5T2WgCxyU1"
        "bHzAnysaJ8N6pgCZQuFBMfXkva+o7q9aeNYTEJrYm3zYUFpIGmgM197eX8hcVKaSm3Mf9gHH3MQuFhIW"
        "AdaIMJ03Immsj7XaoYudRGbTaX4HFC6a42ECck/ty/iqiiah5a5sd2bOG35zxDtoxDYBx8Ocg9ub1qBX"
        "ibJrJuRMpdpZXxrvMn2vnPK6Xtet7P762JXvC7MxY2qGMOvR0b2RQdHtgib6WzPos2ttLNI4BC6yOTb7"
        "g6GYY+kWj8GXBfdy5D/pbi6wXU2LZvgMs9Ao+6UtLtP0Db7NI157QcDJmgYBDIdQDwJTZUFQz9Cykqv9"
        "B1BLAwQUAAIACACFuJxS0C562B4EAADsDwAAGwAcAHB5ZHdmLWV4YW1wbGVzL0RpZ2l0YWxJTy5weVVU"
        "CQADys2JYNTNiWB1eAsAAQToAwAABOgDAAC9V21v2zYQ/q5fcVOBRSocxW2yADPgDcWSDcaGNkAL9KNA"
        "SWeZqEUKFJXUKPrfdyQlW7JlOXGx6YtE3fG548OHL/fqJ7iqK3WVcHGF4hHKjV5Jce15vCil0qB5ge03"
        "U3nJVLVtKyYyWXjeUsmCOmZPS2gsdzznaxT6M3vEpVRF9Q9PFFMb55phIeNa8zXXHKu2z5KLLLamDB95"
        "ihO4o8ad/X4v9Z+yFtm9UlJ5XoZLB5JRHM3WMZcxK3nQNBcfQrj8Dd5LgTMP6PF932CJSiumEfQKbYbk"
        "CourD7CsRaq5FIwS2kSe7fJpz+fdwwJWrII3v0KBRFFWzVpHhQg5ClQ83bNdgsIKdRA2rVSKJc9rhds/"
        "lWa6rqhp2/c8X+kWg9JkGp6k+gJSwPVbKLnYActal7W+FyxZ40IsZWCHzIUesH+kFFw7RvtjZhzDAc+/"
        "TLJDQMdD7MAHUAfwuDgCZw0fGz5ak7WN8XJ7M87L7c0JZsjh2dwcAxsL1A0xzNBhzy1HR0yOpX0jqdyx"
        "sF0GUSs/+7tU5Bn4D0SX47CqS7vyXCaXbvwQ8AijCWjFjTgx7C+PmR92wLrfPhyQDwHJNuE6hMg+MINv"
        "36fJt9n0+m3y3Y/M1sC0cXoNPviTTuaH+g5PBiMtDAa7vekEg+npYIbZsD/OAwYJDp5WPF3t0ccrYETX"
        "Y0MkbZoIQuotn1n4bApJG/sMnkuhXYjhqVh9As9lsJH0KQKtBA07KSstc5I2dcUfucibzJ5B1JDKziRq"
        "TGVD+jqTo3P1ZYRFixm0hBVth8/gZkg+Z3IzIp8h4ZxJzUuEkzIBCUJdYQZ0LNttcZST7Z7645x0jrDw"
        "eJQf5aR3CIxz4sI2l4nTLLjjY5CHl7LQntfhWJwBJl7Kw+7EG2Kiomtm3JziFKmC+fjWZDux9fqYc8u6"
        "Q38FrrPp0Yi+2jtnD+8ULbqLpdXG3UTNY1Y2J4bM/TnH4M10Gu6M5nH36jY514rMy3WYToCm4zVdfUL4"
        "eTuMHsJ+Zi6nDm7Yc/+/lvR2gMiyhKVfetT39DSc3n+uqn7E/j9TCUXVGrEMptEvNGnWSlULzUBndsdE"
        "sa/T0JUyBeMiCJsrrK2wFDHTVlvRO5XXBRVTD9YSZFilipfmRjbvlTV1xXJ7inbqm8V+ddNuDhYrYlkW"
        "swY+uKA/nIopURcJqosJCDJV84vf6XOF63LuOwdwDt1IptYDV7b5zaoxfWkUTSD7MqG2tU5vSZjScX60"
        "auxMxBPXq4NKMaDuExsw6g0hNCeDc+kvsMHa0fpFuxLS9sCvKZb6WCW6Q20k+oes15m97pkcbRxoq1n8"
        "SuWuyNsZaJD/xk0imcoWQqNSdakPMFsPc893LoQlMnNNMvgGz+NLiGPBCoxjmM/Bj2OjqTj2HZoTmPcv"
        "UEsDBBQAAgAIAIW4nFKU2cnXDQMAAKsKAAAgABwAcHlkd2YtZXhhbXBsZXMvZGVtb191dGlsaXRpZXMu"
        "cHlVVAkAA8rNiWDUzYlgdXgLAAEE6AMAAAToAwAAzVY9b9swEN31K67OEAkwhHQN4AJBnAId6i4tMgSF"
        "QEtHm61EqiQVJzD833vUp2lLcVF0qAfboO7evXv3QQVcqwLK12zHQRSl0haWO/4gq+JeSS42nyRXQZDm"
        "zBhYYqGW+CxSXCn7UVUye9Ba6fDhJcXSCiWj2wDoU5JxEGTIgQuZJRm50ZfzCynMHAxqwfKEYqxRJ6bE"
        "VHCB2WKlJM4hreNWmjnEhAsr0ZiEVzKtDShGHeQKvm4RCC9GAopTomPDCJydc4R1JfLMAAPL1jmC4g5Y"
        "Ymoxg4aMAbtlFlJGxgi/KmJFzyoj5IaeDNg9ponryHSUdAiLMwYNO8F9swXcNNrU+mhBlrOVgqXYiByl"
        "hUf2jFzpwvTcuNM3nkW9l2bC4GQN2rietKSaMyCSTz3LxmBVPw+bWAkVCV9IOqXh+ASEpKByg+FRKtH3"
        "PsGJMoIw4Ao15HsFd60xNMawYwakstA7xb3xiXLvFvB+QDpS73OVW1FSZS9pOG+jvAKROhb0COzumYm8"
        "7pPW9Rb2h3gWOzhGz+cwi38oIcOClaHGUs9HlY7o48Ffqllnh7lBP8sr+FKirPtQyfy15RV7Nl6xqMOa"
        "yvhY49qP6E5jkImM2bqpnzxo1xher8y70J4IkWsY12RIs4vhqECuvGO+bkIm+qltuLY3qNLhQDU6mayj"
        "krrtMPSkL8H+0HdgO2ZdpV1twwkip8X9b3pnRJbLY9NbH02LrvvN12rQMNwfor9T6p+MgdvLI7zfHIlB"
        "kqebYXFN3zDnu0ujrbSst3wbTxEhf3N2F9I34+nF4Ho60nXcOj0i7ESeA76wQkgERv89N6AcoBTpz3YZ"
        "YHNtbZmpD7Zis0VDjdyAx0F/RzUo/hXlTu7ri2okgzXhJD7lRkggECfLlFUbu7OqzVw3jWF5l0pj0F3p"
        "9Ro6ceGKUPf+ack0K9CijiX9wu1pgu6dJRyJffpu0eNEI2z7h47x2SvRYYrxIMV07cPzJCNvyU0Wom1P"
        "OGPbhf3wRnn8yZqMsRgr2yXXC2k32f3BLM0neUXBb1BLAwQUAAIACACFuJxStFnF17MDAADCCAAAIQAc"
        "AHB5ZHdmLWV4YW1wbGVzL0FuYWxvZ091dFNpbXBsZS5weVVUCQADys2JYNTNiWB1eAsAAQToAwAABOgD"
        "AACNVm1v4zYM/p5fwUs/zNlSJe1hwNDhPhzSK67Y0A27bvfRUGw60WZLrkTnZcP++0hbdl6uGS5AAVmi"
        "HpIPH1K9egOzJvjZ0tgZ2g3Ue1o7+3Y0MlXtPAGZCvt1pWk9GhXeVWyWbwuI+/dmZUq09FlvsHC+Cj+b"
        "pdd+P4X3Vpdu9UtDTy7HKTz8/rSYwv22GPYf8xI7xBwrlzZkSkMGQw9dGJun7VGOG5Mxxj1/3LfrJ0cP"
        "rrH5B++dH41yLDqQQgdKdeshdQ0lunc2uRuNgH9X8BsGJNBlCdlaW4tlUO3JYKq8WCTXNxOA7tLi4w28"
        "g3lc3/L6pkdbOFuYVeMRlo7WwD7rhgZkYEogvDSaz7fMUDyfwtawsWECYIlrvTFixlGRi7C5N2xNawRj"
        "mRRdQjArDhA2umywC/gq2jIXYqoJtggWN+hBZ9RwhnsIpKWQaxNa/1IhWKFFr8k4+wY+I/zZBBLnEU18"
        "Rl+6qrkiTS5BwB+ulLjXJlu36a24UGIbM3ZF+zWWnMZQchRlBIwnHaaCZ4nFhLjHHpDdb/Wec4fceMyI"
        "wz6kP8AfhddV6guuWwoYWZfBAS9L1JKZq3ArJzV6SV9b+jFicdJk7Ao0B2JXXIsI9U3osds8JPvIIEep"
        "/+LE5+p7UApuoGLxtGhS6Hg9Zd3iTm4lLJypKKZX36nOLDfGQ2MzKcUnrn5yAnDWQWqhvTfou05Sn1pR"
        "TV5BlQoIWv87Rz1vQfXYKWxyIcIPVi97xK+M8Nk3HFrHi8eXBm22l6ZRc2b949/dCaWBXL3VxILi5lJd"
        "e2Xc1cQKlnbrzOa8lkmkKmcdOWuyJGKzGLlo4uyIXnrFHK4Z5mCy2bHNLZfw23asqcyF5Lb/qA2viP+G"
        "yA/EbPanF1k2/39xuHkFzy62zbGsY6M5C6iZhtgqtHWDqqfS1G2LHt0edHqEf2jWKGt1SXLve0uuaafQ"
        "C2Xc7CZfB3F7GeKYhL6238n87DdNcag578/n87vhTH55080qZj4hKeRBNpMTw9obS8n4n7sf1NviXyid"
        "q8MsYKbgVx7oQSY1eVdeL2TSvDSG1Fi1A4GSPoDZ4G1yin2syuP9Uw1T9xBVmmXRd7w8le8uvpK9ksnv"
        "D1m3b8P545cw0AR0gO7zjKPXnr7OUB1ewPYK7jKs6dJLeoCNbC5cU+bAjdQG1DqC/jXGnWl1Nj5B/gn3"
        "S6d9/iiE+aamLzB7C56Q0YSxbC6TWPAFj/8FKSBNra4wTUUX4zQVWtN03MF1HI/+A1BLAwQUAAIACACF"
        "uJxSlsjNrMIDAADsCAAAHgAcAHB5ZHdmLWV4YW1wbGVzL1Byb3RvY29sVUFSVC5weVVUCQADys2JYNTN"
        "iWB1eAsAAQToAwAABOgDAACVVW1v2zYQ/u5fcVM+RMYUxe4woAtgFNnSAsGKrshcLN8ESjzFRCVSIKnY"
        "btH/vuObrbgN2vqLKfLuubfn7s5+gcvR6MtayEuUjzDs7UbJ32Yz0Q9KW7Cix3Rm+mFg2uBs1mrVkyjf"
        "thDfbsSD6FDa/9gjtkr35q2oNdP7IMqxV9VoRSesQJN0WiF55Z84PooGC7ihjxt/fqfsGzVK/lprpWcz"
        "jm0EYdpWg1ZWNaqr2CBydzO/mgH9sixzCNJYzSyC3SB8uL5bQ5KHdpSNFUoycmRfzrzSmqSc95Z1J9LX"
        "729hwwz8AT1SVrgpgHUdqBa2G9FsKB8Io0EOQpItYbyHEfUCNBq0+Rx+6HcR5b/vcwSn+P518AXUwpp4"
        "pOqQTPwwVg3+6MAd9FNYkmUUFmqTMO0uaupw+J7DBjtsLPCYu0FIA1R6oORL0wsL+fp+DkxyCq1B8YiQ"
        "39EFF/TpApoY/tE0BcMHA5xZBp5gNhbRURACmw6p+kn05KwHF9Kqb4EXcKH0RUHvxGiqzCdMehpECw3x"
        "hHixFXYDn1Ar1zpjT+pl4mlgieNuGYkSbs6Acj8OoViN6vtRioa5dPncLpe/f3wBNRt5AS/fLcsJSmQE"
        "SbxYLMrF/PiUGPJycnekylQycWZ58OatUkPNmo+wvgdKxd09EU5RVORPKvzt5T+u+HC2cOmTCiRS7CTc"
        "KCkdQxgMm72hMDroEtyWWDDxPnBv6opON9GRP91YQWI1PQr54PBjxgvYIvSjsafVGHza6r0vh9ehQno6"
        "hH4O9TFOfDHN5G5i1sUPo6TR5biAWo+DRX5F+ANSxnm3pz4gik9p3qMx7AEjvwWsYOFPNDU6hLUeMYwr"
        "94uyJJP5kqfvs89fstINUmZzMS9RNopjPj/oxazlUf74kOtdVY9tizrNg4pyZkczJxspvuVicdQYNEWW"
        "Z3fBe35w4fOXkKCAAgEFJn49a+mI7dZHaTrEIV+UT6wK+HUFyzDZeyZkTjPcP/oVo8nZtG7K69g87/1L"
        "ztE0Wvjirp7M+9G7TeP56yFKo7zM5hP8knFepa7Mz+mGiFPJsa9Rnxcg6cmszl/RcYPdsMqCAASBZONk"
        "KGSRNU6X/I+G/J8zZVKPW70/EsDt0NWz63NScV+L05WZk3rhDZZPQqC5a6JXR1Pe3LeXaByZsaU/uJXq"
        "1XDn2ui5vXx1yqG/1NhxGgFht3tjh4GJO+EaN5UhIv+N+1oxzW9Tc32FmSSO/UdYkrt+9vvWZZ1GblVJ"
        "2mdVBStqpapylKqqLKAFfs3+B1BLAwQUAAIACACFuJxSqpcM31EDAABgBwAAIAAcAHB5ZHdmLWV4YW1w"
        "bGVzL0FuYWxvZ0luU2ltcGxlLnB5VVQJAAPKzYlg1M2JYHV4CwABBOgDAAAE6AMAAI1VXYvTQBR9z6+4"
        "xocm0M1WxZeFIourIIoILvogEqaZm2RkMhPno90i/nfvzCTttrsLlmXbzJx77rmfef4MLr01lxuhLlFt"
        "Ydy7XqtXWSaGURsHzHQjMxbnZycGzLLW6IGgfNfCdH4jOiFRue9si602g/0kNoaZfYJyHHTtnZDCCbSz"
        "TSsUr+MVx61ocAk39HATf3/W7r32ir8zRpssyzi2iYUpJnVXCzV6R/+tM34gvzUbRW2JWGKRIB9UeZUB"
        "ffI8D7wByhyC6xES0DoYtbViIxG8RdBtvEzmED1A0zOlUNoqi1y3vbBRR2ITWiWuPTRMSpvIHXPeFiW0"
        "XjURMhFfT7rgKHsJO+H6eLswyDi/YY4tQtbjNdgRG9EK5MAsbJn0CO+ZtFhFNe+2qMhW++4exRkD6W2D"
        "xfKeNvAjD6kw+NtTFog9VikAjtKAayqVQeeNIoMLpy+i0VZLxzoEiVvKS4gNWdNHPVOcj+UspEt0vaPe"
        "2DHDYcf2AU7+zV6oLtl5Y4LjQ54mVxYGQm9IvW9b0YiAIZ6pisDGUYomFiMUgDnoqQlB6eBUNC6GKQyG"
        "oJJMKhqLptTNwTlTHAjadWjosZq7JsmfoqkbakcHa5i7q5ou3obzooxY0Z7D17BKXRg+I9G7Ir+lWFPH"
        "k1IbhD7acimWhqkQOvUnj0G7uQOrvDwQpyolvQd9Bi0GYfF019N4wq3xeJRzQE4dGzurPFd7X1u+hPBX"
        "/dJCFfkkFP78vYI/Vy9fVy9X7V/48e1nXoUVwFwxJ4MGHe+W5w6/xiKcgsoyRnlyRr7BMNUdoTG5ZXnU"
        "GtZSZSXiWKyq1YtVmTbGwEgnrYGIi3vMhApOO626nobkS7wpONrGiDE00vpkZTxcF4+MMpWIenWuSnJW"
        "0UTX8ygWCzoRTNbKDxs0iyUourLrxRv62aMc13kCQALM4zSv1qln8qmiwZaCmRzFr+DKzhV3Zn8sddjU"
        "6yeXdHFMZFxH54u5IPNldFidhFCGrZQgR1fR3X9u6mRbHRZ2JMG7Bkf31LvgwTTR/ElOQ5TeJ9E1zO8T"
        "vKMXDk10fsL8EfcbTUvog3JojB/dA84ZQeWdIMSleNgV8+hlNOt1rdiAdR3GPK/r0G11nSe21HrZP1BL"
        "AQIeAwoAAAAAAIW4nFIAAAAAAAAAAAAAAAAPABgAAAAAAAAAEADtQQAAAABweWR3Zi1leGFtcGxlcy9V"
        "VAUAA8rNiWB1eAsAAQToAwAABOgDAABQSwECHgMUAAIACACFuJxSPl5CQVsFAAC7EgAAGgAYAAAAAAAB"
        "AAAApIFJAAAAcHlkd2YtZXhhbXBsZXMvQW5hbG9nSU8ucHlVVAUAA8rNiWB1eAsAAQToAwAABOgDAABQ"
        "SwECHgMUAAIACACFuJxSq5kc3P4DAABXCQAAHQAYAAAAAAABAAAApIH4BQAAcHlkd2YtZXhhbXBsZXMv"
        "UHJvdG9jb2xDQU4ucHlVVAUAA8rNiWB1eAsAAQToAwAABOgDAABQSwECHgMUAAIACACFuJxSD/DU06wE"
        "AAClDgAAKQAYAAAAAAABAAAApIFNCgAAcHlkd2YtZXhhbXBsZXMvQW5hbG9nT3V0Q29udGludW91c1Bs"
        "YXkucHlVVAUAA8rNiWB1eAsAAQToAwAABOgDAABQSwECHgMUAAIACACFuJxSJQkjtMoFAAAkDgAAHQAY"
        "AAAAAAABAAAApIFcDwAAcHlkd2YtZXhhbXBsZXMvUHJvdG9jb2xTUEkucHlVVAUAA8rNiWB1eAsAAQTo"
        "AwAABOgDAABQSwECHgMUAAIACACFuJxSIZz6QM8PAACvLwAAJAAYAAAAAAABAAAApIF9FQAAcHlkd2Yt"
        "ZXhhbXBsZXMvQW5hbG9nSW5SZWNvcmRNb2RlLnB5VVQFAAPKzYlgdXgLAAEE6AMAAAToAwAAUEsBAh4D"
        "FAACAAgAhbicUqsjJNZcBQAA6QwAAB0AGAAAAAAAAQAAAKSBqiUAAHB5ZHdmLWV4YW1wbGVzL1Byb3Rv"
        "Y29sSTJDLnB5VVQFAAPKzYlgdXgLAAEE6AMAAAToAwAAUEsBAh4DFAACAAgAhbicUtAuetgeBAAA7A8A"
        "ABsAGAAAAAAAAQAAAKSBXSsAAHB5ZHdmLWV4YW1wbGVzL0RpZ2l0YWxJTy5weVVUBQADys2JYHV4CwAB"
        "BOgDAAAE6AMAAFBLAQIeAxQAAgAIAIW4nFKU2cnXDQMAAKsKAAAgABgAAAAAAAEAAACkgdAvAABweWR3"
        "Zi1leGFtcGxlcy9kZW1vX3V0aWxpdGllcy5weVVUBQADys2JYHV4CwABBOgDAAAE6AMAAFBLAQIeAxQA"
        "AgAIAIW4nFK0WcXXswMAAMIIAAAhABgAAAAAAAEAAACkgTczAABweWR3Zi1leGFtcGxlcy9BbmFsb2dP"
        "dXRTaW1wbGUucHlVVAUAA8rNiWB1eAsAAQToAwAABOgDAABQSwECHgMUAAIACACFuJxSlsjNrMIDAADs"
        "CAAAHgAYAAAAAAABAAAApIFFNwAAcHlkd2YtZXhhbXBsZXMvUHJvdG9jb2xVQVJULnB5VVQFAAPKzYlg"
        "dXgLAAEE6AMAAAToAwAAUEsBAh4DFAACAAgAhbicUqqXDN9RAwAAYAcAACAAGAAAAAAAAQAAAKSBXzsA"
        "AHB5ZHdmLWV4YW1wbGVzL0FuYWxvZ0luU2ltcGxlLnB5VVQFAAPKzYlgdXgLAAEE6AMAAAToAwAAUEsF"
        "BgAAAAAMAAwArwQAAAo/AAAAAA=="
}

def extract_zip_to_directory(target):
    zipfile.ZipFile(io.BytesIO(base64.b64decode(_zipped_directory_data[target]))).extractall()

def show_version():
    """Show DWF library version number."""

    dwf = DigilentWaveformsLibrary()
    print("DWF library version: {}".format(dwf.getVersion()))

def summarize_api():

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

def list_devices(use_obsolete_api: bool, list_configurations: bool):
    """List devices supported by the DWF library."""

    dwf = DigilentWaveformsLibrary()

    num_devices = dwf.enum.count()

    if num_devices == 0:
        print("No Digilent Waveform devices found.")

    for device_index in range(num_devices):

        devtype = dwf.enum.deviceType(device_index)
        is_open = dwf.enum.deviceIsOpened(device_index)
        username = dwf.enum.userName(device_index)
        devicename = dwf.enum.deviceName(device_index)
        serial = dwf.enum.serialNumber(device_index)

        if num_devices == 1:
            header = "Device information for device #{} ({} device found)".format(device_index, num_devices)
        else:
            header = "Device information for device #{} ({} of {} devices found)".format(device_index, device_index+1, num_devices)

        print(header)
        print("=" * len(header))
        print()
        print("  device .......... : {}".format(devtype[0]))
        print("  version ......... : {}".format(devtype[1]))
        print("  open ............ : {}".format(is_open))
        print("  username ........ : {!r}".format(username))
        print("  devicename ...... : {!r}".format(devicename))
        print("  serial .......... : {!r}".format(serial))
        print()
        if use_obsolete_api:

            ai_channels = dwf.enum.analogInChannels(device_index)
            ai_bufsize = dwf.enum.analogInBufferSize(device_index)
            ai_bits = dwf.enum.analogInBits(device_index)
            ai_frequency = dwf.enum.analogInFrequency(device_index)

            print("  Analog-in information (obsolete API)")
            print("  ------------------------------------")
            print()
            print("  number of channels ...... : {!r}".format(ai_channels))
            print("  buffer size ............. : {!r}".format(ai_bufsize))
            print("  bits .................... : {!r}".format(ai_bits))
            print("  frequency ............... : {!r}".format(ai_frequency))
            print()

        if list_configurations:

            configuration_data = {}

            num_config = dwf.enum.configCount(device_index)

            for configuration_index in range(num_config):
                for configuration_parameter in DwfEnumConfigInfo:
                    configuration_parameter_value = dwf.enum.configInfo(configuration_index, configuration_parameter)
                    configuration_data[(configuration_index, configuration_parameter)] = configuration_parameter_value

            print("  Configuration:          {}".format("  ".join("{:8d}".format(configuration_index) for configuration_index in range(num_config))))
            print("  ----------------------  {}".format("  ".join("--------" for configuration_index in range(num_config))))
            for configuration_parameter in DwfEnumConfigInfo:
                print("  {:22}  {}".format(configuration_parameter.name, "  ".join("{:8d}".format(configuration_data[(configuration_index, configuration_parameter)]) for configuration_index in range(num_config))))
            print()


def extract_examples():
    raise NotImplementedError()

def extract_html_documentation():
    raise NotImplementedError()

def extract_pdf_documentation():
    raise NotImplementedError()

def main():

    parser = argparse.ArgumentParser(
        prog = "python -m pydwf",
        description="Utilities for the pydwf package.",
    )
    subparsers = parser.add_subparsers()

    # If no command is given, execute the toplevel parser's "print_help" method.
    parser.set_defaults(execute=lambda args: parser.print_help())

    # Declare the sub-parser for the "version" command.
    parser_version = subparsers.add_parser("version",
        description="Show version of the DWF library.",
        help="show version of the DWF library")
    parser_version.set_defaults(execute=lambda args: show_version())

    # Declare the sub-parser for the "ls" command.

    parser_ls = subparsers.add_parser("ls", aliases=["list", "list-devices"],
        description="List Digilent Waveforms devices.",
        help="list Digilent Waveform devices")
    parser_ls.add_argument('-c', '--list-configurations', action='store_true',
                        help="for each device, printing its configurations", dest='list_configurations')
    parser_ls.add_argument('-u', '--use-obsolete-api', action='store_true',
                        help="for each device, print analog-in parameters obtained using obsolete FDwfEnumAnalogIn* API calls", dest='use_obsolete_api')
    parser_ls.set_defaults(execute=lambda args: list_devices(args.list_configurations, args.use_obsolete_api))

    # Declare the sub-parser for the "examples" command.
    parser_extract_examples = subparsers.add_parser("examples", aliases=["pydwf-examples", "extract-examples"],
        description="Extract pydwf example scripts to \"pydwf-examples\" directory.",
        help="extract pydwf example scripts to \"pydwf-examples\" directory")
    parser_extract_examples.set_defaults(execute=lambda args: extract_zip_to_directory("pydwf-examples"))

    # Parse command-line arguments.
    args = parser.parse_args()

    # Execute the selected command.
    args.execute(args)

if __name__ == "__main__":
    main()
