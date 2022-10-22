from collections import defaultdict
from bisect import bisect_left, bisect_right



# https://github.com/benfulton/Algorithmic-Alley/blob/master/AlgorithmicAlley/SuffixArrays/sa.py
class SuffixArray:
    @staticmethod
    def suffix_array_manber_myers(data):
        result = []

        def sort_bucket(input_data, bucket, order=1):
            dictionary = defaultdict(list)
            for i in bucket:
                key = input_data[i:i+order]
                dictionary[key].append(i)
            for k, value in sorted(dictionary.items()): # pylint: disable= unused-variable
                if len(value) > 1:
                    sort_bucket(input_data, value, order*2)
                else:
                    result.append(value[0])
            return result

        return sort_bucket(data, (i for i in range(len(data))))


class MatchFinder:
    def __init__(self, data):
        self.data = data
        self.sa_left = 0
        self.sa_right = 8000 if len(data) < 8000 else len(data)-1
        self.sa = SuffixArray.suffix_array_manber_myers(
            data[self.sa_left: self.sa_right+1]
        )

    def sa_ref(self, start, length=1):
        # Returns the real data corresponding to relative sa_left
        # sa_left
        return self.data[self.sa_left + start : self.sa_left + start + length]

    def find_longest_match(self, i):
        if i >= self.sa_right and i != 0:
            self.sa_left = i - 4000
            self.sa_right = i + 4000
            self.sa = SuffixArray.suffix_array_manber_myers(
                self.data[self.sa_left: self.sa_right + 1]
            )
        left, right = self.binary_search_left_right(i)
        if left == -1:
            return None

        best_length = 0
        best_dist = None
        for sa_i in range(left, right + 1):
            dist = i - self.sa_left - self.sa[sa_i]
            if  dist <= 2:
                continue
            if 2 <= dist < 4000:
                length = 1
                for len_i in range(1, 15):
                    if len(self.data) <= i+length:
                        break  # new
                    #print("len", len(self.data), "i+l", i+length)  # new
                    if self.data[i+length] == self.data[i-dist+length]:
                        if i+length < len(self.data):
                            length += 1
                    else:
                        break  # new
                if length > best_length:
                    best_dist, best_length = dist, length
        if best_length >= 2:
            return (best_dist, best_length)
        else:
            return None

        # search the longest matching pattern from the region

    def bbinary_search_left_right(self, i :int) -> tuple:
        """ Searches the lfetmost and rightmost match in the suffix array

        Args:
            i (int): index to real data

        Returns:
            tuple: (left, right)
        """

        left_ret, right_ret = -1, -1
        # search left
        l, r = 0, len(self.sa) - 1
        while l < r:
            m = (l + r) // 2
            if self.sa_ref(m) < self.data[i]:
                l = m + 1
            else:
                r = m
        if self.sa_ref(l) == self.data[i]:
            left_ret = l

        # search right
        l, r = 0, len(self.sa) - 1
        while l < r:
            m = (l + r) // 2 + 1
            if self.sa_ref(m) > self.data[i]:
                r = m - 1
            else:
                l = m
        if self.sa_ref(l) == self.data[i]:
            right_ret = l
        
        return (left_ret, right_ret)
    def bcinary_search_left_right(self, i :int) -> tuple:
        ret_left , ret_right = -1, -1
        a = [self.sa_ref(x) for x in self.sa]
        ret_left = bisect_left(a, self.data[i])
        if self.sa_ref(self.sa[ret_left]) != self.data[i]:
            return (-1, -1)
        ret_right = bisect_right(a, self.data[i]) -1
        return (ret_left, ret_right)

    def binary_search_left_right(self, i: int) -> tuple:
        target = self.data[i: i+2]
        return (
            self._bisect_left(target),
            self._bisect_right(target)
        )

    def _bisect_left(self, target):
        l, r = 0, len(self.sa) - 1
        while l < r:
            m = (l + r) // 2
            if self.sa_ref(
                self.sa[m], 2
            ) < target:
                l = m + 1
            else:
                r = m
        return l if self.sa_ref(
                self.sa[l], 2
            ) == target else -1

    def _bisect_right(self, target):
        l, r = 0, len(self.sa) - 1
        while l < r:
            m = (l + r) // 2 + 1
            if self.sa_ref(
                self.sa[m], 2
            ) > target:
                r = m - 1
            else:
                l = m
        return l if self.sa_ref(
                self.sa[l], 2
            )  == target else -1
    
