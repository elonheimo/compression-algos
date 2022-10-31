from collections import defaultdict
from typing import Tuple



class SuffixArray:
    # http://algorithmicalley.com/archive/2013/06/30/suffix-arrays.aspx
    # Function made by Ben Fulton
    @staticmethod
    def suffix_array_manber_myers(data):
        result = []

        def sort_bucket(input_data, bucket, order=1):
            dictionary = defaultdict(list)
            for i in bucket:
                key = input_data[i:i+order]
                dictionary[key].append(i)
            for _, value in sorted(dictionary.items()): # pylint: disable= unused-variable
                if len(value) > 1:
                    sort_bucket(
                        input_data, value, order*2
                    )
                else:
                    result.append(value[0])
            return result

        return sort_bucket(data, (i for i in range(len(data))))
    @staticmethod
    def longest_common_prefix(og_inp: list, sa: list) -> list:
        """Generates longest common prefix array 
        Prefixes are the longest prefix in common with i and i-1
        Therefore always lcp_array[0] = 0
        Kasai et al. (2001) Time complexity: O(n)

        Args:
            og_inp (list): original input
            sa (list): suffix array from input

        Returns:
            list: lcp_array
        """
        n = len(sa)
        rank = [0] * n
        for i in range(n):
            rank[sa[i]] = i
        lcp = [0] * n
        l = 0
        for i in range(1,n):

            i_ = sa[rank[i] - 1]

            while (i_ + l < n
                    and i + l < n
                    and og_inp[i + l] == og_inp[i_ + l]):
                l += 1
            lcp[rank[i]] = l
            l = max(0, l - 1)
        return lcp


class MatchFinder:
    def __init__(self, data):
        self.data = data
        self.sa_left = 0
        if len(data) < 8000:
            self.sa_right = len(data)-1
        else:
            self.sa_right = 8000
        self.sa = SuffixArray.suffix_array_manber_myers(
            data[self.sa_left: self.sa_right+1]
        )
        self.lcp = SuffixArray.longest_common_prefix(
            self.data[self.sa_left: self.sa_right+1], self.sa
        )
        self.left_right_sum = 0
        self.left_right_count = 0
        

    def sa_ref(self, start :int, length :int = 1) -> list:
        """Return the real data that index referencing to suffix array contains.

        Args:
            start (int): 
            length (int, optional): Defaults to 1.

        Returns:
            list: data
        """
        # Returns the real data corresponding to relative sa_left
        # sa_left
        return self.data[self.sa_left + start : self.sa_left + start + length]
    
    def find_longest_match(self, i :int) -> Tuple:
        """Find longest match in current suffix array

        Args:
            i (int): current index to byte that should be encoded<

        Returns:
            Tuple / None: Best distance from i and length of match.
        """
        if i >= self.sa_right and i != 0:
            self.sa_left = i - 4000 #
            self.sa_right = i + 4000 #
            self.sa = SuffixArray.suffix_array_manber_myers(
                self.data[self.sa_left: self.sa_right + 1]
            )
            self.lcp = SuffixArray.longest_common_prefix(
                self.data[self.sa_left: self.sa_right+1], self.sa
            )
        left, right = self.binary_search_left_right(i)
        if left == -1:
            return None

        best_length = 0
        best_dist = None
        length = 1

        for sa_i in range(left, right + 1):
            dist = i - self.sa_left - self.sa[sa_i]

            if self.lcp[sa_i] -1 < length:
                length = 1

            if 2 <= dist < 4000:

                for len_i in range(1, 15):

                    i_len = i + length
 
                    if (i_len < len(self.data) -1
                        and
                        self.data[i_len] == self.data[i_len - dist]):
                        length +=1
                    else:
                        break

                if length > best_length:
                    best_length = length
                    best_dist = dist
                    if length ==15:
                        break

        if best_length >= 2:
            return (best_dist, best_length)
        return None


    def binary_search_left_right(self, i: int) -> tuple:
        """ Searches the leftmost and rightmost match in the suffix array

        Args:
            i (int): index to real data

        Returns:
            tuple: (left, right)
        """
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
    
