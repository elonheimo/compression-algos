from collections import defaultdict

# https://github.com/benfulton/Algorithmic-Alley/blob/master/AlgorithmicAlley/SuffixArrays/sa.py


class suffixArray:
    @staticmethod
    def suffix_array_ManberMyers(data):
        result = []

        def sort_bucket(input, bucket, order=1):
            d = defaultdict(list)
            for i in bucket:
                key = input[i:i+order]
                d[key].append(i)
            for k, v in sorted(d.items()):
                if len(v) > 1:
                    sort_bucket(input, v, order*2)
                else:
                    result.append(v[0])
            return result

        return sort_bucket(data, (i for i in range(len(data))))


class MatchFinder:
    def __init__(self, data):
        self.data = data
        self.sa_left = 0
        self.sa_right = 8000 if len(data) < 8000 else len(data)-1
        self.sa = suffixArray.suffix_array_ManberMyers(
            data[0: self.sa_right+1])

    def sa_ref(self, left, length=1):
        # returns the real window from data array
        # represented by search_array
        left = self.sa_left + self.sa[left]
        #print(left, length, self.data[left: left+length])
        return self.data[left: left+length+1]

    def findLongestMatch(self, i):
        # init new suffix array if necessary
        if i >= self.sa_right and i != 0:
            self.sa_left = i - 4000
            self.sa_right = i + 4000
            self.sa = suffixArray.suffix_array_ManberMyers(
                self.data[self.sa_left: self.sa_right + 1]
            )

        # find leftmost and rightmost match from search array
        left, right = self.binarySearchLeftRight(i)
        # if no match
        if left == -1:
            return None

        best_length = 0
        best_dist = None
        for sa_i in range(left, right + 1):
            dist = i - (self.sa_left + self.sa[sa_i])
            if dist >= 2 and dist < 4000:
                length = 1
                for len_i in range(1, 15):
                    if len(self.data) <= i+length:
                        break  # new
                    print("len", len(self.data), "i+l", i+length)  # new
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

    def binarySearchLeftRight(self, i):
        left_ret, right_ret = -1, -1
        # search left
        l, r = 0, len(self.sa) - 1
        while l < r:
            m = (l + r) // 2
            #print("left", l, "right", r, "i", i)
            if self.sa_ref(m) < bytes(self.data[i]):
                l = m + 1
            else:
                r = m
        if self.sa_ref(l) == self.data[i]:
            left_ret = l

        # search right
        l, r = 0, len(self.sa) - 1
        while l < r:
            m = (l + r) // 2 + 1
            if self.sa_ref(m) > bytes(self.data[i]):
                r = m - 1
            else:
                l = m
        if self.sa_ref(l) == self.data[i]:
            right_ret = l

        return (left_ret, right_ret)
