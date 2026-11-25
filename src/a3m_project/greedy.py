import random


def time_stamp(N):
    return [0 for _ in range(N)]


class Problem:
    def _ratio_of_arrays(self):
        # Avoid division by zero and regularize individual scores.
        return [(i, p / (e + 0.5)) for i, (p, e) in enumerate(zip(self.P, self.E))]

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
        # Count current profit.
        profit = sum(p for p, on in zip(self.P, self.time_stamp) if on == 1)

        while profit < self.T:
            indexes_left = [
                idx for idx, ratio in self.sorted_ratios
                if idx not in self.used_indexes
            ]

            if not indexes_left:
                raise ValueError(
                    f'El greedy se quedó sin índices con beneficio {profit}. '
                    f'El objetivo era {self.T}.'
                )

            best_index = indexes_left[0]
            self.used_indexes[best_index] = True

            left, right, is_candidate = self._is_candidate(best_index)
            if not is_candidate:
                continue

            ranges = self._possible_ranges(best_index, left, right, is_candidate)

            # Choose the best range using its global profit/energy ratio.
            best_score = -1
            best_range = None

            for start, end in ranges:
                range_profit = sum(self.P[start:end + 1])
                range_energy = sum(self.E[start:end + 1])
                score = range_profit / (range_energy + 0.1)

                if score > best_score:
                    best_score = score
                    best_range = (start, end)

            # Apply the selected range and update profit.
            start, end = best_range
            for i in range(start, end + 1):
                self.time_stamp[i] = 1
                print(self.time_stamp)
                self.used_indexes[i] = True
                profit += self.P[i]

        return profit


if __name__ == '__main__':
    stamp = time_stamp(30)
    P = [random.randint(0, 10) for _ in stamp]
    E = [random.randint(0, 10) for _ in stamp]
    print('E is ', E)
    print('P is ', P)

    L = 1
    U = 7
    T = 100

    problema = Problem(stamp, L, U, P, E, T)
    profit = problema.iterate()
    energy = sum(e for e, on in zip(E, problema.time_stamp) if on == 1)

    print('--------------------')
    print('RESULTADO:', problema.time_stamp)
    print('PROFIT:', profit)
    print('ENERGY:', energy)
