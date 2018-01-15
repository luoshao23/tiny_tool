import numpy as np

class Klotski(object):
    """docstring for Klotski"""

    def __init__(self, num):
        self.num = num
        self.max = 999

        temp = np.arange(num*num)
        np.random.shuffle(temp)
        temp[temp.argmax()] = self.max
        self.array = temp.reshape(num, num)
        self._print()

    def series_move(self, steps, verbose=False):
        if len(steps)%3 != 0:
            raise KeyError
        else:
            start = 0
            for _ in range(steps/3):
                self.move(steps[start:start+3])
                start += 3

    def move(self, drct, step=1):

        KEY = {'\x1b[A': 'up',
               '\x1b[B': 'down',
               '\x1b[D': 'left',
               '\x1b[C': 'right'  }

        if drct not in KEY:
            raise KeyError
        method_name = '_move_' + KEY[drct]
        method = getattr(self, method_name, lambda: 'nothing')

        x, y = self.ind()
        method(x, y, step)
        self._print()

    def ind(self):
        max_ind = self.array.argmax()
        x, y = divmod(max_ind, self.num)
        return x, y

    def _move_up(self, x, y, step):
        # x, y = self.ind()
        if x < self.num - 1:
            end = min(x + step, self.num - 1)
            self.array[x:end, y] = self.array[x+1:end+1, y]
            self.array[end, y] = self.max

    def _move_down(self, x, y, step):
        # x, y = self.ind()
        if x > 0:
            start = max(x - step, 0)
            self.array[start+1:x+1, y] = self.array[start:x, y]
            self.array[start, y] = self.max

    def _move_left(self, x, y, step):
        # x, y = self.ind()
        if y < self.num - 1:
            end = min(y + step, self.num - 1)
            self.array[x, y:end] = self.array[x, y+1:end+1]
            self.array[x, end] = self.max

    def _move_right(self, x, y, step):
        # x, y = self.ind()
        if y > 0:
            start = max(y - step, 0)
            self.array[x, start+1:y+1] = self.array[x, start:y]
            self.array[x, start] = self.max

    def _print(self):
        print
        for row in self.array:
            strs = '|'
            for a in row:
                if a == self.max:
                    strs += '%2s|' % '*'
                else:
                    strs += '%2d|' % a
            print strs
        print

    def _check_win(self):
        ac = self.array.ravel('C')
        ac = ac[1:] - ac[:-1]
        if all(ac[:-1]) or all(a[1:]):
            return True
        ac = self.array.ravel('F')
        ac = ac[1:] - ac[:-1]
        if all(ac[:-1]) or all(a[1:]):
            return True
        return False



def main():
    tab = Klotski(4)
    inputs = 'None'

    while tab._check_win():
        inputs = raw_input('Input: ')
        tab.move(inputs)

if __name__ == '__main__':
    main()
