import tkinter as tk
import numpy as np
import catan
import board
import constants

PLAYER_COLORS = constants.PLAYER_COLORS


# SCREEN_HIGHT = 1080
# SCREEN_WIDTH = 1920

# constant Hexagon radius for catan GUI
HEX_RADIUS = 5/60*1080
SCREEN_HIGHT = HEX_RADIUS*8 +10
SCREEN_WIDTH = HEX_RADIUS*10*.875 +10

# RESOURCE_COLORS correspond the RESOURCE_NAMES constant from the Catan class
RESOURCE_COLORS = ["khaki", "saddle brown", "gray", "gold2", "dark green", "lawn green"]

def hexagon_coordinates2(a, center_x=0, center_y=0):
    """ Hexagon with horizontal edges
     # https://www.quora.com/How-can-you-find-the-coordinates-in-a-hexagon
    :param
    - a is the radius of the hexagon
    - center_x, center_y are the center coordinates of the hexagon
    :return: x,y coordinate vector for tkinter create polygon coordinates


    Let the length of the sides of the regular hexagon be  a  units.
        ⇒  The coordinates of vertex  A  and vertex  D  are  (a,0)  and  (−a,0)  respectively.
        Each interior angle of a regular hexagon is  120o.
        ⇒  The triangle formed by each side and the lines joining the end points of the side to the circumcentre are equilateral.
        ⇒  The circumradius of the hexagon is  a  units.
        ⇒  The coordinates of vertex  B  are  (acos60o,asin60o)=(a2,3√a2).
        ⇒  The coordinates of vertex  self.C  are  (acos120o,asin120o)=(−a2,3√a2).
        ⇒  The coordinates of vertex  E  are  (acos240o,asin240o)=(−a2,−3√a2).
        ⇒  The coordinates of vertex  F  are  (acos300o,asin300o)=(a2,−3√a2)."""
    x_angle = a / 2
    y_angle = np.sqrt(3) * a / 2
    return [-x_angle + + center_x,
            -y_angle + center_y, x_angle + + center_x, -y_angle + center_y,
             a + center_x, 0 + center_y, x_angle + center_x, y_angle + center_y, -x_angle + center_x,
            y_angle + center_y, -a + center_x, 0 + center_y]

    # return [a + center_x, 0 + center_y, a / 2 + center_x, np.sqrt(3) * a / 2 + center_y, -a / 2 + center_x,
    #         np.sqrt(3) * a / 2 + center_y, -a + center_x, 0 + center_y, -a / 2 + center_x,
    #         -np.sqrt(3) * a / 2 + center_y, a / 2 + center_x, -np.sqrt(3) * a / 2 + center_y]


def hexagon_coordinates(a, center_x, center_y):
    """Hexagon with vertical edges"""
    cor = hexagon_coordinates2(a, center_y, center_x)
    # return [cor[1], cor[0], cor[3], cor[2], cor[5], cor[4], cor[7], cor[6], cor[9], cor[8], cor[11], cor[10]]
    # return [cor[1], cor[0], cor[3], cor[2], cor[5], cor[4], cor[7], cor[6], cor[9], cor[8], cor[11], cor[10]]
    cor.reverse()
    return cor


class GUIboard:
    def __init__(self, board):
        """

        :param board: from the catan class
        :return: GUI visualisation
        """
        self.window = tk.Tk()

        self.window.title("Catan game State")



        self.C = tk.Canvas(self.window, bg="light blue", height=SCREEN_HIGHT, width=SCREEN_WIDTH)

        # xs = np.concatenate(
        #     [(HEX_RADIUS * 0.875) * (np.arange(3) * 2 + 3)] + [(HEX_RADIUS * 0.875) * (np.arange(4) * 2 + 2)] + [
        #         (HEX_RADIUS * 0.875) * (np.arange(5) * 2 + 1)] + [(HEX_RADIUS * 0.875) * (np.arange(4) * 2 + 2)] + [
        #         (HEX_RADIUS * 0.875) * (np.arange(3) * 2 + 3)])
        xs = [(HEX_RADIUS * 0.875) * (np.arange(3) * 2 + 3)] + [(HEX_RADIUS * 0.875) * (np.arange(4) * 2 + 2)] + [
                (HEX_RADIUS * 0.875) * (np.arange(5) * 2 + 1)] 
        xs.append(xs[1])
        xs.append(xs[0])
        xs = np.concatenate(xs)
            

        # ys = [HEX_RADIUS] * 3 + [HEX_RADIUS * 2.5] * 4 + [HEX_RADIUS * 4] * 5 + [HEX_RADIUS * 5.5] * 4 + [
        #     HEX_RADIUS * 7] * 3
        ys = []
        size = 3
        for i in range(5):
            ys += [HEX_RADIUS+(HEX_RADIUS*1.5*i)] * size
            if i < 2:
                size +=1
            else:
                size -=1


        for i in range(19):
            x = xs[i]
            y = ys[i]
            tile = board.terrains[i+1]
            t = str(tile.resource_num) + ' ' + catan.RESOURCE_NAMES[tile.resource]
            # added +5 to move it right and down; to give space at sides
            coord = hexagon_coordinates(HEX_RADIUS, x+5, y+5)
            self.C.create_polygon(coord, fill= RESOURCE_COLORS[tile.resource])
            self.C.create_text(x, y, font="Times 15 italic bold",
                        text=t)
            
            # pass the coordinates to the edges and intersections
            coord_i = 0
            OFFSET = 4
            for i in tile.intersections:
                if not hasattr(i, 'coords'):
                    # x, y, x, y
                    i.coords = [coord[coord_i] - OFFSET, coord[coord_i + 1] - OFFSET, coord[coord_i] + OFFSET, coord[coord_i + 1] + OFFSET]
                coord_i += 2
            
            coord_e = 0
            for e in tile.edges:
                if not hasattr(e, 'coords'):
                    # x, y, x, y
                    e.coords = [coord[coord_e], coord[coord_e + 1]]
                    if coord_e+2 >= len(coord):
                        e.coords += [coord[0], coord[1]]
                    else:
                        e.coords += [coord[coord_e + 2], coord[coord_e + 3]]
                coord_e += 2

            # self.C.update
        # display the edges and intersections
        for i in board.intersections.values():
            self.C.create_oval(i.coords, fill='black')
        for e in board.edges.values():
            self.C.create_line(e.coords, fill='black', width=4)
        
        self.C.pack()

        # test:
        # self.C.create_oval(board.intersections[30].coords, fill='purple')
        # self.C.create_line(board.edges[30].coords, fill='purple', width=4)
        # self.C.update()
    

    def update_GUI(self, board):
        self.C.create_oval(board.intersections[30].coords, fill='purple')
        self.C.create_line(board.edges[30].coords, fill='purple', width=4)
        self.C.update()

    # def buy_road(self, edge_num, player):
    #     self.C.create_line(board.edges[edge_num], fill=player_colors[player], width=4)
        self.C.update()

if __name__ == '__main__':
    board = catan.CatanBoard().board
    g = GUIboard(board)
    input('continue')
    try:
        g.update_GUI(board)
    except:
        pass
    g.window.mainloop()

    print('Debug complete')
