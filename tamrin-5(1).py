class Soldier:
    def init(self, soldier_type, soldier_id, x, y):
        self.soldier_type = soldier_type
        self.soldier_id = soldier_id
        self.health = 100
        self.x = x
        self.y = y

    def attack(self, target):
        if self.soldier_type == "archer":
            target.health -= 10
        elif self.soldier_type == "melee":
            target.health -= 20

        if target.health <= 0:
            print("target eliminated")


class Archer(Soldier):
    def init(self, soldier_id, x, y):
        super().init("archer", soldier_id, x, y)


class Melee(Soldier):
    def init(self, soldier_id, x, y):
        super().init("melee", soldier_id, x, y)


class Game:
    def init(self, n):
        self.n = n
        self.board1 = [[[]] * n for _ in range(n)]
        self.board2 = [[[]] * n for _ in range(n)]
        self.players = {0: [], 1: []}
        self.turn = 0
        self.IDs1 = []
        self.IDs2 = []
        
    def change_turn(self):
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0

    def create_soldier(self, soldier_type, soldier_id, x, y):
        if (self.turn == 0 and soldier_id in self.IDs1) or (self.turn == 1 and soldier_id in self.IDs2):
            print("duplicate tag")
            return

        if soldier_type == "archer":
            soldier = Archer(soldier_id, x, y)
        elif soldier_type == "melee":
            soldier = Melee(soldier_id, x, y)
        else:
            print("Invalid soldier type")
            return
        if self.turn == 0:
            self.board1[x][y].append(soldier)
            self.IDs1.append(soldier_id)
        else:
            self.board2[x][y].append(soldier)
            self.IDs2.append(soldier_id)
        self.players[self.turn].append(soldier)
        self.change_turn()


    def move_soldier(self, soldier_id, direction):
        soldier = self.find_soldier(soldier_id)
        if soldier is None:
            print("soldier does not exist")
            return

        new_x, new_y = self.calculate_new_position(soldier.x, soldier.y, direction)
        if not self.is_within_bounds(new_x, new_y):
            print("out of bounds")
            return

        if self.turn == 0: 
            self.board1[soldier.x][soldier.y].remove(soldier)
            self.board1[new_x][new_y].append(soldier)
        else:
            self.board2[soldier.x][soldier.y].remove(soldier)
            self.board2[new_x][new_y].append(soldier)
        soldier.x, soldier.y = new_x, new_y
        self.change_turn()

    def attack(self, attacker_id, target_id):
        attacker = self.find_soldier(attacker_id)
        self.change_turn()
        target = self.find_soldier(target_id)
        self.change_turn()
        if attacker is None or target is None:
            print("soldier does not exist")
            return

        distance = self.calculate_distance(attacker.x, attacker.y, target.x, target.y)

        if attacker.soldier_type == "archer" and distance > 2:
            print("the target is too far")
            return
        elif attacker.soldier_type == "melee" and distance > 1:
            print("the target is too far")
            return

        if attacker.soldier_type == "archer":
            target.health -= 10
        elif attacker.soldier_type == "melee":
            target.health -= 20

        if target.health <= 0:
            print("target eliminated")
            self.change_turn()
            if self.turn == 0: 
                self.board1[target.x][target.y].remove(target)
                self.IDs1.remove(target_id)
            else:
                self.board2[target.x][target.y].remove(target)
                self.IDs2.remove(target_id)
            self.players[self.turn].remove(target)
            self.change_turn()
        self.change_turn()

    def get_soldier_info(self, soldier_id):
        soldier = self.find_soldier(soldier_id)
        if soldier is None:
            print("soldier does not exist")
            return
print(f"health: {soldier.health}")
        print(f"location: {soldier.x} {soldier.y}")
        self.change_turn()

    def check_winner(self):
        player0_health = sum(s.health for s in self.players[0])
        player1_health = sum(s.health for s in self.players[1])

        if player0_health > player1_health:
            return "player 1"
        elif player0_health < player1_health:
            return "player 2"
        else:
            return "draw"

    def find_soldier(self, soldier_id):
        board = self.board1
        if self.turn == 1:
            board = self.board2
        for row in board:
            for soldiers in row:
                if soldiers != []:
                    for soldier in soldiers:
                        if soldier.soldier_id == soldier_id:
                            return soldier
        return None

    def calculate_new_position(self, x, y, direction):
        if direction == "up":
            return x, y - 1
        elif direction == "down":
            return x, y + 1
        elif direction == "left":
            return x - 1, y
        elif direction == "right":
            return x + 1, y

    def is_within_bounds(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.n

    def calculate_distance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)



if name == "main":
    n = int(input())
    game = Game(n)

    while True:
        command = input().split()
        if command[0] == "end":
            break
        elif command[0] == "new":
            game.create_soldier(command[1], int(command[2]), int(command[3]), int(command[4]))
        elif command[0] == "move":
            game.move_soldier(int(command[1]), command[2])
        elif command[0] == "attack":
            game.attack(int(command[1]), int(command[2]))
        elif command[0] == "info":
            game.get_soldier_info(int(command[1]))
        elif command[0] == "who" and command[1] == "is" and command[2] == "in" and command[3] == "the" and command[4] == "lead?":
            winner = game.check_winner()
            print(winner)