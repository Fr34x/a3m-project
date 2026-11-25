import random


def time_stamp(N):
    return [0] * N


class Problem:
    def __init__(self, time_stamps, L, U, P, E, T, epsilon=0.5):
        self.time_stamp = time_stamps
        self.L = L
        self.U = U
        self.P = P
        self.E = E
        self.T = T
        self.epsilon = epsilon

        if len(P) != len(E) or len(P) != len(time_stamps):
            raise ValueError('P, E and time_stamps must have the same length.')
        if not 1 <= L <= U or epsilon <= 0:
            raise ValueError('Expected 1 <= L <= U and epsilon > 0.')

        self.ranges = self._generate_ranges()

    def _generate_ranges(self):
        """Generate every possible run and cache its profit and energy."""
        ranges = []
        n = len(self.time_stamp)

        for start in range(n):
            range_profit = 0
            range_energy = 0

            for end in range(start, min(start + self.U, n)):
                range_profit += self.P[end]
                range_energy += self.E[end]

                if end - start + 1 >= self.L and range_profit > 0:
                    ranges.append((start, end, range_profit, range_energy))

        return ranges

    def _is_compatible(self, start, end):
        """Check that the run does not overlap or touch an existing run."""
        left = max(0, start - 1)
        right = min(len(self.time_stamp), end + 2)
        return not any(self.time_stamp[left:right])

    def _can_extend(self, idx):
        """Check whether activating idx extends or merges existing runs."""
        stamp = self.time_stamp
        if not 0 <= idx < len(stamp) or stamp[idx]:
            return False

        left = idx - 1
        right = idx + 1
        while left >= 0 and stamp[left]:
            left -= 1
        while right < len(stamp) and stamp[right]:
            right += 1

        length = right - left - 1
        return 1 < length and self.L <= length <= self.U

    def _extend_best(self, remaining_profit):
        """Apply the best feasible single-index expansion."""
        candidates = [
            i for i in range(len(self.P))
            if self.P[i] > 0 and self._can_extend(i)
        ]
        if not candidates:
            return 0

        idx = max(candidates, key=lambda i:
                  min(self.P[i], remaining_profit) / (self.E[i] + self.epsilon))
        self.time_stamp[idx] = 1
        return self.P[idx]

    def iterate(self):
        profit = sum(p for p, on in zip(self.P, self.time_stamp) if on)

        # Incompatible ranges can never become compatible again.
        candidates = [r for r in self.ranges if self._is_compatible(r[0], r[1])]

        while profit < self.T:
            if not candidates:
                extra_profit = self._extend_best(self.T - profit)
                if extra_profit == 0:
                    raise ValueError(
                        f'El greedy se quedó sin rangos ni expansiones con beneficio {profit}. '
                        f'El objetivo era {self.T}.'
                    )
                profit += extra_profit
                continue

            remaining_profit = self.T - profit

            # Recompute the score after every selection.
            def score(run):
                start, end, p, e = run
                return min(p, remaining_profit) / (e + self.epsilon)

            start, end, p, e = max(candidates, key=score)

            for i in range(start, end + 1):
                self.time_stamp[i] = 1

            profit += p

            # Remove overlapping or adjacent ranges in O(1) per range.
            candidates = [
                r for r in candidates
                if r[1] < start - 1 or r[0] > end + 1
            ]

        return profit


if __name__ == '__main__':
    random.seed(140)
    stamp = time_stamp(30)
    P = [random.randint(0, 10) for _ in stamp]
    E = [random.randint(0, 10) for _ in stamp]
    print('E is ', E)
    print('P is ', P)

    L = 2
    U = 7
    T = 100

    problema = Problem(stamp, L, U, P, E, T)
    try:
        profit = problema.iterate()
    except ValueError as error:
        print(error)
        profit = sum(p for p, on in zip(P, stamp) if on)

    energy = sum(e for e, on in zip(E, problema.time_stamp) if on)

    print('--------------------')
    print('RESULTADO:', problema.time_stamp)
    print('PROFIT:', profit)
    print('ENERGY:', energy)
    print('FEASIBLE:', profit >= T)
