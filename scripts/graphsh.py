#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

class GraphShell:
    def __init__(self):
        self._understood_command = True
        self._mounted_fpath = None
        self._el = None
        self._adj_set = None
        self._nodes = None

    def gsh_read(self):
        return input('gsh $ ')

    def gsh_tick(self, command):
        splitted = command.strip().split(' ')
        head = splitted[0]
        args = splitted[1:]

        if head == 'q' or head == 'quit':
            quit()
        elif head == 'mount':
            self.mount_graph(args[0])
        elif head == 'info':
            self.graph_info()
        else:
            print('did not understand command')

    def mount_graph(self, mount_gtag):
        self._mounted_gtag = mount_gtag
        mount_fpath = get_gtag_graph_path(mount_gtag)
        self._mounted_el = clean_el(read_in_el(mount_fpath))
        self._mounted_adj_set = read_in_adj_set(mount_fpath)
        self._mounted_nodes = read_in_nodes(mount_fpath)
        print(f'successfully mounted {mount_gtag}')
        self.graph_info()

    def graph_info(self):
        num_nodes = len(self._mounted_nodes)
        num_edges = len(self._mounted_el)
        print(f'{self._mounted_gtag}: {num_nodes}n {num_edges}e')

    def run(self):
        while True:
            try:
                command = self.gsh_read()
                self.gsh_tick(command)
            except Exception as e:
                print(f'failed: {e}')


if __name__ == '__main__':
    gsh = GraphShell()
    gsh.run()
