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


def time_stamp(N):
    time_stamp = [0 for _ in range(N)]
    return time_stamp

class Problem:

    def _ratio_of_arrays(self):
        return [(i, p / e) for i, (p, e) in enumerate(zip(self.P, self.E))]

    def __init__(self, time_stamps, L, U, P, E, T):
        self.time_stamp = time_stamps
        self.L = L
        self.U = U
        self.P = P
        self.E = E
        self.T = T
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
        # count current profit
        profit = sum(p for p, on in zip(self.P, self.time_stamp) if on == 1)

        while profit < self.T: 

            indexes_left = [
                idx for idx, ratio in self.sorted_ratios
                if idx not in self.used_indexes
            ]

            if not indexes_left:
                raise ValueError(
                    f"El greedy se quedó sin índices con beneficio {profit}. "
                    f"El objetivo era {T}."
                )

            best_index = indexes_left[0]
            self.used_indexes[best_index] = True

            left, right, is_candidate = self._is_candidate(best_index)
            if not is_candidate:
                continue

            ranges = self._possible_ranges(best_index, left, right, is_candidate)

            # chose best range score
            best_score = -1
            best_range = None
            for start, end in ranges:
                score = sum(self.ratios[i][1] for i in range(start, end + 1))
                if score > best_score:
                    best_score = score
                    best_range = (start, end)

            start, end = best_range
            for i in range(start, end + 1):
                self.time_stamp[i] = 1
                self.used_indexes[i] = True
                profit += self.P[i]

        return profit
            
             
            
# if __name__ == "__main__":
#     # Index: 0  1  2  3  4  5  6  7  8
#     stamp = [1, 1, 0, 0, 0, 0, 0, 1, 1]
#     P =     [1, 1, 1, 1, 8, 1, 1, 1, 1]
#     E = [2] * len(stamp)

#     problema = Problem(stamp, L=2, U=3, P=P, E=E)

#     idx, ratio = problema.sorted_ratios[0]
#     assert (idx, ratio) == (4, 4.0)

#     left, right, is_candidate = problema._is_candidate(idx)
#     assert (left, right, is_candidate) == (3, 5, True)

#     ranges = problema._possible_ranges(idx, left, right, is_candidate)
#     assert ranges == [(3, 4), (4, 5), (3, 5)]

#     # Index 2 must stay zero because index 1 is already on.
#     left, right, is_candidate = problema._is_candidate(2)
#     assert not is_candidate
#     assert problema._possible_ranges(2, left, right, is_candidate) == []

#     print("tests passed, valid ranges for index 4:", ranges)




#     T = 14
#     profit = problema.iterate(T)
#     energy = sum(e for e, on in zip(E, problema.time_stamp) if on == 1)

#     print("final stamp:", problema.time_stamp)
#     print("profit:", profit)
#     print("energy:", energy)

#     assert problema.time_stamp == [1, 1, 0, 1, 1, 1, 0, 1, 1]
#     assert profit == 14
#     assert energy == 14

import random


stamp = time_stamp(150)
P = [random.randint(1, 10) for _ in stamp]
E = [random.randint(1, 10) for _ in stamp]
print("E is ", E)
print("P is ", P)
L=7
U=16
T=500
problema = Problem(stamp,L, U, P, E, T)
problema.iterate()
print("--------------------")
print("RESULTADO:", problema.time_stamp)