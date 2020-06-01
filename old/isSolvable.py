def isSolvable(seq):
        seq = list(seq) 
        N = int(len(seq) ** 0.5)
        
        def countInv(seq):
            # function to count the number of inversions
            numinv = 0
            for i in range(0,N**2,1):
                for j in range(i+1,N**2,1):
                    if seq[i] != N**2 and seq[j] != N**2 and seq[i] > seq[j]:
                        numinv += 1
            return numinv
        
        def blankRow(seq):
            #function to find row of the blank tile (counting from bottom)
            return N - ((seq.index(N**2)) // N + 1)
        def isEven(num):
            # returns if number is even
            return num % 2 == 0
        def isOdd(num):
            # returns if number is odd
            return num % 2 == 1

        numinv = countInv(seq)
        # If grid is odd, return true if inversion 
        # count is even. 
        if isOdd(N):
            return isEven(numinv)
        else: # grid is even 
            pos = blankRow(seq)
            if isEven(pos):
                return isEven(numinv)
            else:
                return isOdd(numinv)


test1 = [9,1,3,4,2,6,7,5,8] # 4 moves
test2 = [6,5,4,1,7,3,9,8,2] # 26 moves
test3 = [7,9,13,1,14,16,8,15,3,6,10,5,2,11,12,4] # 58 moves 
test4 = [15,14,1,6,9,11,4,12,16,10,7,3,13,8,5,2] # 52 moves --> https://rosettacode.org/wiki/15_puzzle_solver#A.2A_with_good_heuristic
test5 = [2,8,3,1,6,4,7,9,5] # Not Solvable # 18 moves --> https://www.d.umn.edu/~tcolburn/cs2511/slides.new/state_space_search/benchmarks.xhtml
test6 = [8,6,7,2,5,4,3,9,1] # 31 moves --> http://kevingong.com/Math/SixteenPuzzle.html
test6b = [6,4,7,8,5,9,3,2,1] # 31 moves --> http://kevingong.com/Math/SixteenPuzzle.html
test7 = [7,14,16,9,10,2,11,13,6,15,4,12,5,1,8,3] # 54 moves -- > https://www.d.umn.edu/~tcolburn/cs2511/slides.new/state_space_search/benchmarks.xhtml
test8 = [5,1,2,3,6,16,7,4,9,10,11,8,13,14,15,12] # 8 moves -- > https://www.d.umn.edu/~tcolburn/cs2511/slides.new/state_space_search/benchmarks.xhtml
test9 = [7,8,4,11,12,14,10,15,16,5,3,13,2,1,9,6] # 50 moves -- > https://www.d.umn.edu/~tcolburn/cs2511/slides.new/state_space_search/benchmarks.xhtml
test10 = [1,5,9,13,2,6,10,14,3,7,11,15,4,8,12,16] # lower bound 40 moves --> https://www.ic-net.or.jp/home/takaken/nt/slide/solve15.html
test11 = [15,11,13,12,14,10,8,9,7,2,5,1,3,6,4,16] # solvable? # 80 moves --> https://puzzling.stackexchange.com/questions/24265/what-is-the-superflip-on-15-puzzle
test12 = [15,14,8,12,10,11,9,13,2,6,16,1,3,7,4,5]
# for puz in [test1,test2,test3,test4,test5,test6,test6b,test7,test8,test9,test10,test11,test12]:
#     print(puz,isSolvable(puz))
print(isSolvable([1,2,3,4,5,6,7,8,9]))