#!/pkg/python/3.7.4/bin/python3
from bash_helpers import *

out, err = run_cmd('echo hello')
print(out, err)
