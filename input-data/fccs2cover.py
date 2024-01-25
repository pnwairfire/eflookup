#!/usr/bin/env python

import pandas as pd

def main():
    df = pd.read_csv('eflook_fccs_cover_8nov23.csv', dtype={'fccs_id': str, 'cover_type_id': str})
    data = df.set_index('fccs_id').to_dict()['cover_type_id']
    with open('fccs2covertype.py', 'w') as f:
        f.write('{} = '.format('FCCS_2_COVERTYPE'))
        write_ordered_data(data, f)
   
def write_ordered_data(data, f):
    # This is done so that the data python modules don't
    # change from one run of the import process to the next
    # when the underlying data hasn't changed
    if isinstance(data, dict):
        f.write('{')
        for k in sorted(data):
            f.write('"{}":'.format(k))
            write_ordered_data(data[k], f)
            # don't worry about trailing ',', since we're writing python
            f.write(',')
        f.write('}')
    else:
        if data is None:
            f.write('None'.format(data))
        else:
            f.write('"{}"'.format(data))

if __name__ == '__main__':
    main()
