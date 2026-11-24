# [00000000] L=2 U=6 P=[273272] E=[9273482]

# Creamos lista ratio para cada index
# elegimos mejor index
# se puede ese index? 
#     si:
#         creamos todos los rangos posibles con ese index
#         operamos ratio sumado
#         elegimos el mejor-> run hecho
#     no: 
#         elegimos siguiente mejor index


# [0110000001110001110] -> check L+1 izq y derecha. Luego ver donde estan los 1s mas proximos con limite U+1.

# ((izq,null)(dr,3)) -> puedes crear rangos a la derecha hasta i+2 solamente
# es decir, podemos crear rangos de longitud 2, 3, 4, 5, 6 hacia la izq y 2 hacia la derecha conteniendo a i

def time_stamp(N):
    time_stamp = [0 for _ in range(N)]
    return time_stamp
class Problem:

    def _ratio_of_arrays(self):
        return [(i, p / e) for i, (p, e) in enumerate(zip(self.P, self.E))]

    def __init__(self, time_stamps, L, U, P, E):
        self.time_stamp = time_stamps
        self.L = L
        self.U = U
        self.P = P
        self.E = E
        self.ratios = self._ratio_of_arrays()
        self.sorted_ratios = sorted(
            self.ratios, key=lambda item: item[1], reverse=True
        )
        self.used_indexes = {}
     
    def _is_candidate(self, idx):
        stamp = self.time_stamp
        n = len(stamp)

        if not 0 <= idx < n or stamp[idx] == 1:
            return None, None, False

        left = right = idx

        while left > 0 and idx - left + 1 < self.U and stamp[left - 1] == 0:
            left -= 1

        while right < n - 1 and right - idx + 1 < self.U and stamp[right + 1] == 0:
            right += 1

        # Leave one zero between the new run and any existing run.
        if left > 0 and stamp[left - 1] == 1:
            left += 1
        if right < n - 1 and stamp[right + 1] == 1:
            right -= 1

        is_candidate = left <= idx <= right and right - left + 1 >= self.L
        return left, right, is_candidate

    def _possible_ranges(self, idx, left, right, is_candidate):
        if not is_candidate:
            return []

        ranges = []
        max_length = min(self.U, right - left + 1)

        for length in range(self.L, max_length + 1):
            first_start = max(left, idx - length + 1)
            last_start = min(idx, right - length + 1)

            for start in range(first_start, last_start + 1):
                end = start + length - 1
                ranges.append((start, end))

        return ranges
    def iterate(self):
        # checking indexes left
        profit = 0
        while(profit<self.T):
            indexes_left = [item for item in self.sorted_ratios if item not in used_indexes]

            # best index from left
            best_index = indexes_left[0]

            # left, right limits and if its a candidate
            left, right, is_candidate = self._is_candidate(best_index)
            if (is_candidate):
                ranges = self._possible_ranges(idx, left, right, is_candidate)
            else:
                pass
            
             
            
if __name__ == "__main__":
    # Index: 0  1  2  3  4  5  6  7  8
    stamp = [1, 1, 0, 0, 0, 0, 0, 1, 1]
    P =     [1, 1, 1, 1, 8, 1, 1, 1, 1]
    E = [2] * len(stamp)

    problema = Problem(stamp, L=2, U=3, P=P, E=E)

    idx, ratio = problema.sorted_ratios[0]
    assert (idx, ratio) == (4, 4.0)

    left, right, is_candidate = problema._is_candidate(idx)
    assert (left, right, is_candidate) == (3, 5, True)

    ranges = problema._possible_ranges(idx, left, right, is_candidate)
    assert ranges == [(3, 4), (4, 5), (3, 5)]

    # Index 2 must stay zero because index 1 is already on.
    left, right, is_candidate = problema._is_candidate(2)
    assert not is_candidate
    assert problema._possible_ranges(2, left, right, is_candidate) == []

    print("Tests passed. Valid ranges for index 4:", ranges)