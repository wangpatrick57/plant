#!/bin/python3
def assert_with_prints(value, target, value_title):
    assert value == target, f'{value_title} is not {target}'
    print(f'success, {value_title} = {target}')

if __name__ == '__main__':
    assert_with_prints(5, 5, 'foo')
