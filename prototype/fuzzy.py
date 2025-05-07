class leven:
    @staticmethod
    def _levenshtein_distance(sequence_1, sequence_2):
        edits = [[x for x in range(len(sequence_1) + 1)] for y in range(len(sequence_2) + 1)]
        
        for i in range(1, len(sequence_2) + 1):
            edits[i][0] = edits[i - 1][0] + 1
            
        for i in range(1, len(sequence_2) + 1):
            for j in range(1, len(sequence_1) + 1):
                if sequence_2[i - 1] == sequence_1[j - 1]:
                    edits[i][j] = edits[i - 1][j - 1]
                else:
                    edits[i][j] = 1 + min(edits[i - 1][j - 1], edits[i - 1][j], edits[i][j - 1])
             
        return edits[-1][-1]
    
    @staticmethod
    def ratio(seq_1, seq_2):
        distance = leven._levenshtein_distance(seq_1, seq_2)
        max_len = max(len(seq_1), len(seq_2))
        
        if max_len == 0:
            return 100
        
        return round((1 - distance/max_len) * 100)
    
    @staticmethod
    def partial_ratio(seq_1, seq_2):
        if len(seq_1) > len(seq_2):
            seq_1, seq_2 = seq_2, seq_1
        
        best = 0
        
        for i in range(len(seq_2) - len(seq_1) + 1):
            window = seq_2[i : i + len(seq_1)]
            distance = leven._levenshtein_distance(window, seq_1)
            
            best = max(best, distance)
            
        return distance
    
    @staticmethod
    def token_set_ratio(seq_1, seq_2):
        set1 = set(seq_1.lower().split())
        set2 = set(seq_2.lower().split())
        
        intersection = set1 & set2
        diff1 = set1 - intersection
        diff2 = set2 - intersection
        
        combined1 = " ".join(intersection | diff1)
        combined2 = " ".join(intersection | diff2)
        base = " ".join(intersection)
        
        return max(
            leven.ratio(base, combined1),
            leven.ratio(base, combined2),
            leven.ratio(combined1, combined2)
        )
    


