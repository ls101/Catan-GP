from PIL import Image, ImageTk
import tkinter as tk
import numpy as np
import catan
import board
import constants

PLAYER_COLORS = constants.PLAYER_COLORS


# SCREEN_HIGHT = 1080
# SCREEN_WIDTH = 1920

# constant Hexagon radius for catan GUI
HEX_RADIUS = 90
# HEX_RADIUS = 5/60*1080
SCREEN_HIGHT = HEX_RADIUS*8 +10
SCREEN_WIDTH = HEX_RADIUS*10*.875 +10

# RESOURCE_COLORS correspond the RESOURCE_NAMES constant from the Catan class
RESOURCE_COLORS = ["khaki", "saddle brown", "gray", "gold2", "dark green", "lawn green"]
RESOURCE_IMAGES = ["images/desert.png", "images/brick.png", "images/ore.png", "images/hay.png", "images/wood.png", "images/sheep.png"]

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

        self.board = board
        self.icons = []

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

        self.imgs = []
        for i in range(19):
            x = xs[i]
            y = ys[i]
            tile = board.terrains[i+1]
            # added +5 to move it right and down; to give space at sides
            x +=5
            y +=5
            coord = hexagon_coordinates(HEX_RADIUS, x, y)
            self.C.create_polygon(coord, fill=RESOURCE_COLORS[tile.resource])


            self.img = Image.open(RESOURCE_IMAGES[tile.resource])
            self.img = self.img.resize((HEX_RADIUS*2, HEX_RADIUS*2), Image.ANTIALIAS)
            self.imgs.append(ImageTk.PhotoImage(self.img, master=self.C))
            self.C.create_image(x, y, image=self.imgs[i], anchor=tk.CENTER)


            self.C.create_text(x, y, font="Times 30 italic bold",
                        text=tile.resource_num)
            
            # pass the coordinates to the edges and intersections
            coord_i = 0
            OFFSET = 2
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

    def buy_road(self, player, edge_num):
        # updates an edge to reflect the road color
        self.C.create_line(self.board.edges[edge_num].coords, fill=PLAYER_COLORS[player], width=5)
        self.C.update()

    def buy_settlement(self, player, edge_num):
        # updates an intersection to reflect the settlement
        # first, enlarge the circle
        add_offset = 10
        coords = self.board.intersections[edge_num].coords
        new_coords = []
        new_coords.append(coords[0] - add_offset)
        new_coords.append(coords[1] - add_offset)
        new_coords.append(coords[2] + add_offset)
        new_coords.append(coords[3] + add_offset)
        self.C.create_oval(new_coords, fill=PLAYER_COLORS[player], outline='')

        # add icon
        self.img = Image.open('images/house.png')
        self.img = self.img.resize((25, 25), Image.ANTIALIAS)
        # add image to end of list (to ensure all icons are displayed).
        # then, display the last icon from the list - this one
        self.icons.append(ImageTk.PhotoImage(self.img, master=self.C))
        cur_icon = len(self.icons)-1
        self.C.create_image(coords[0], coords[1], image=self.icons[cur_icon], anchor=tk.CENTER)

        self.C.update()

    def buy_city(self, player, edge_num):
        # updates an intersection to reflect the city
        # first, enlarge the circle
        add_offset = 15
        coords = self.board.intersections[edge_num].coords
        new_coords = []
        new_coords.append(coords[0] - add_offset)
        new_coords.append(coords[1] - add_offset)
        new_coords.append(coords[2] + add_offset)
        new_coords.append(coords[3] + add_offset)
        self.C.create_oval(new_coords, fill=PLAYER_COLORS[player], outline='')

        self.img = Image.open('images/city.png')
        self.img = self.img.resize((30, 30), Image.ANTIALIAS)
        # add image to end of list (to ensure all icons are displayed).
        # then, display the last icon from the list - this one
        self.icons.append(ImageTk.PhotoImage(self.img, master=self.C))
        cur_icon = len(self.icons)-1
        self.C.create_image(coords[0], coords[1], image=self.icons[cur_icon], anchor=tk.CENTER)

        self.C.update()

    def restrict_edge(self, edge_num):
        # updates an intersection to reflect its restricted status
        coords = self.board.intersections[edge_num].coords

        self.img = Image.open('images/x.png')
        self.img = self.img.resize((30, 30), Image.ANTIALIAS)
        # add image to end of list (to ensure all icons are displayed).
        # then, display the last icon from the list - this one
        self.icons.append(ImageTk.PhotoImage(self.img, master=self.C))
        cur_icon = len(self.icons)-1
        self.C.create_image(coords[0], coords[1], image=self.icons[cur_icon], anchor=tk.CENTER)

        self.C.update()


if __name__ == '__main__':
    board = catan.CatanBoard().board
    g = GUIboard(board)
    # input('continue')
    try:
        g.update_GUI(board)
    except:
        pass
    g.window.mainloop()

    print('Debug complete')
    # print(g.icon)
