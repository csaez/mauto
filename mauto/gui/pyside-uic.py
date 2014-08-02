import os
import sys
from pysideuic import compileUi


def convert(input_file):
    if not input_file.endswith(".ui"):
        return False
    output_file = os.path.join(os.path.dirname(input_file),
                               os.path.basename(input_file).replace(".ui", ".py"))
    with open(output_file, 'w') as fp:
        compileUi(input_file, fp, False, 4, False)
    return output_file

if __name__ == "__main__":
    convert(sys.argv[1])
