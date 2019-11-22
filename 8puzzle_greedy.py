"""
PROBLEM SOLVING 8 PUZZLE WITH GREEDY ALGORITHM IN PYTHON
Jarot Achid Alvian
433780
MMI - UGM
"""
import itertools
import collections

class Node:
    """
    Class untuk menyimpan node solver
    - variable 'puzzle' merupakan inisialisasi Puzzle
    - variable 'parent' merupakan node sebelum
    - variable 'action' merupakan aksi untuk menggerakkan puzzle
    """
    
    def __init__(self, puzzle, parent=None, action=None):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action
        if (self.parent != None):
            self.g = parent.g + 1
        else:
            self.g = 0

    @property
    def score(self):
        """
        mengembalikan score atau nilai f yang merupakan hasil dari g+h
        """
        return (self.g + self.h)

    @property
    def state(self):
        """
        mengembalikan hashable dari dirinya
        """
        return str(self)

    @property
    def path(self):
        """
        Untuk membuat path dari Root parent
        """
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)

    @property
    def solved(self):
        """
        Mengambil nilai apakah puzzle sudah selesai atau belum
        """
        return self.puzzle.solved

    @property
    def actions(self):
        """
        Mengembalikan action dari fungsi actions di kelas puzzle
        """
        return self.puzzle.actions

    @property
    def h(self):
        """
        mengembalikan nilai h
        h merupakan biaya estimasi pergerakan yang didapatkan dengan fungsi manhattan
        """
        return self.puzzle.manhattan

    @property
    def gg(self):
        """
        mengembalikan nilai g
        """
        #return self.g
        return 0

    @property
    def f(self):
        """
        Mengembalikan nilai f yang merupakan hasil dari h + g
        """
        return self.h + self.g
        

    def __str__(self):
        return str(self.puzzle)


class Solver:
    """
    Class untuk solving 
    parameter start merupakan awal dari puzzle
    """
    def __init__(self, start):
        self.start = start


    def solve(self):
        """
        Menggunakan BFS untuk pencarian solusi dan 
        mengembalikan PATH dari solusi yang ditemukan apabila ditemukan
        """

        """ header """
        print()
        print("======================================================")
        print("RANGKAIAN PROSES BFS")
        print("======================================================")
        print("Jns_Node Num. Action - F(G+H) -> Result_Solving")
        print("------------------------------------------------------")
        print()

        """ Data awal dimasukkan ke collections """
        queue = collections.deque([Node(self.start)])
        """ Buat variable seen untuk memasukkan data node yang sudah di-loop """
        seen = set()
        """ Masukkan root ke variable seen """
        seen.add(queue[0].state)
        
        """
        loop untuk solving problem untuk puzzle yang baru 
        Maximal 4 variasi penyelesain atas, bawah, kiri, kanan
        """
        no_parent = 1
        space = ""
        space_child = ""

        """ BFS"""
        while queue:

            """Sorting child berdasarkan nilai F yang paling kecil, jadi nilai terkecil akan di ekstrak paling awal"""
            queue = collections.deque(sorted(list(queue), key=lambda node: node.f))

            """ masukkan nilai terkecil dan hapus dari queue ke variable node """
            node = queue.popleft()

            """ mencetak header dan PARENT puzzle """
            print(space + "PARENT " + str(no_parent) + ". " +  str(node.action) +" - " +str(node.f) + "(" + str(node.h)+ ") -> " + str(node.solved))
            #print(space + "PARENT " + str(no_parent) + ". " +  str(node.action) +" - " +str(node.f) + "("  + str(node.g)+ "+"  + str(node.h)+ ") -> " + str(node.solved))
            print_puzzle(node, space)

            """ mengembalikan path node apabila sudah ketemu solusi """
            if node.solved:
                return node.path

            """ Load node menurut action yang bisa dilakukan apabila solusi belum ditemukan"""
            print()
            print(space_child + "LIST CHILDS   : ")
            no_child = 1
            for move, action in node.actions:
                """ Buat variable child untuk menyimpan node child """
                child = Node(move(), node, action)

                """ mencetak header dan CHILD puzzle """
                print(space_child + "Child " +  str(no_parent) + "." + str(no_child) + ". " + str(child.action) +" - " + str(child.f) + "("  + str(child.h)+ ") -> " + str(child.solved))
                #print(space_child + "Child " +  str(no_parent) + "." + str(no_child) + ". " + str(child.action) +" - " + str(child.f) + "("  + str(child.g)+ "+"  + str(child.h)+ ") -> " + str(child.solved))
                print_puzzle(child, space_child)

                """
                Check apakah state TIDAK ADA dalam variable seen?
                - masukkan child state ke variable queue paling kiri
                - masukkan child state ke variable seen
                """
                if child.state not in seen:
                    queue.appendleft(child)
                    seen.add(child.state)
                
                """counting"""
                no_child+=1

            """ counting dan print null """
            no_parent+=1
            space+=" "
            space_child+=" "
            print()
            print()


class Puzzle:
    """
    Kelas untuk 8-puzzle
    """

    def __init__(self, board):
        self.width = len(board[0])
        self.board = board

    @property
    def solved(self):
        """
        Mengembalikan hasil compare antara inputan board puzzle dengan goal
        jika sama akan mengembalikan true, jika tidak false
        """
        N = self.width * self.width
        return str(self) == ''.join(map(str, range(1,N))) + '0'

    @property
    def actions(self):
        """
        mengembalikan nilai 'moves' yang berupa list[] 
        dalam prosesnya kelas melakukan looping list dari 'action' (kanan, kiri, bawah, atas)
        sehingga hasil dari loop yang berupa action dan hasilnya di simpan dalam list[] moves
        """
        def create_move(at, to):
            return lambda: self._move(at, to)

        moves = []
        for i, j in itertools.product(range(self.width),
                                      range(self.width)):
            direcs = {'Kanan':(i, j-1),
                      'Kiri':(i, j+1),
                      'Bawah':(i-1, j),
                      'Atas':(i+1, j)}

            for action, (r, c) in direcs.items():
                if r >= 0 and c >= 0 and r < self.width and c < self.width and \
                   self.board[r][c] == 0:
                    move = create_move((i,j), (r,c)), action
                    moves.append(move)
        return moves

    @property
    def manhattan(self):
        """
        mengembalikan nilai H atau BIAYA ESTIMASI PERGERAKAN
        dengan inputan sebuah kondisi board 
        """
        distance = 0
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    x, y = divmod(self.board[i][j]-1, 3)
                    distance += abs(x - i) + abs(y - j)
        
        return distance

    def copy(self):
        """
        mengembalikan nilai puzzle baru yang sama
        """
        board = []
        for row in self.board:
            board.append([x for x in row])
        return Puzzle(board)

    def _move(self, at, to):
        """
        mengembalikan puzzle baru
        dengan menukarkan 'at' dan 'to' atau men-swipe nilai ke kotak kosong
        """
        copy = self.copy()
        i, j = at
        r, c = to
        copy.board[i][j], copy.board[r][c] = copy.board[r][c], copy.board[i][j]
        return copy

    def __str__(self):
        return ''.join(map(str, self))

    def __iter__(self):
        for row in self.board:
            yield from row


def print_puzzle(datas, separator):
    """
    melakukan cetakan puzzle
    dengan masukan data raw puzzle dan separator di depannya
    """
    x=1
    boards = ""
    for board in str(datas):
        boards += board + ""
        if(x%3==0) :
            print(separator + "|" + boards + "|")
            boards = ""
        else :
            boards += " "   
        x+=1

"""
Menjalankan aplikasi 
"""

""" deklarasi state awal pada board """
board = [[0,2,3],[1,4,5],[7,8,6]]

""" me-masukkan board ke dalam class puzzle """
puzzle = Puzzle(board)

""" Mencari solusi solusi dengan kelas solver """
solver = Solver(puzzle)
""" Node solusi disimpan dalam variable solver_datas """
solver_datas = solver.solve()

""" Menampilkan hasil jadi dari puzzle """
print()
print("======================================================")
print("RANGKAIAN URUTAN PUZZLE")
print("------------------------------------------------------")
steps = 0
for data in solver_datas:
    print("STEP " + str(steps+1) + " ")
    print("- Geser      : " + str(data.action))
    print("  F(G+H)     : " + str(data.score) +  " (" + str(data.h) + ")")
    print("  solved     : "+ str(data.solved))
    print_puzzle(data, "               ")
    steps += 1
print()
print("------------------------------------------------------")
print("TOTAL STEP   : " + str(steps) + " step")
print("======================================================")