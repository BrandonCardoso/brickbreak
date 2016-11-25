import math

class SpatialHash():
    def __init__(self, width, height, rows, columns, objects):
        self.cell_width = width/columns
        self.cell_height = height/rows
        self.hash = {}

        for x in range(0, columns):
            for y in range(0, rows):
                self.hash[x, y] = []

        for obj in objects:
            cells =  self.get_cells(obj.get_rect())
            self.add_to_cells(cells, obj)

    def get_cells(self, rect):
        cells = []

        if self.fits_in_cell(rect):
            for point in [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]:
                cell = (int(math.floor(point[0] / self.cell_width)),
                        int(math.floor(point[1] / self.cell_height)))
                if not cell in cells:
                    cells.append(cell)
        else: # rect is larger than cell size, have to checker inner points
            for point_x in range(rect.left, rect.right + self.cell_width, self.cell_width):
                for point_y in range(rect.top, rect.bottom + self.cell_height, self.cell_height):
                    cell = (int(math.floor(point_x / self.cell_width)),
                            int(math.floor(point_y / self.cell_height)))
                    if not cell in cells:
                        cells.append(cell)

        return cells

    def fits_in_cell(self, rect):
        return rect.height * rect.width <= self.cell_height * self.cell_width

    def add_to_cells(self, cells, obj):
        for cell in cells:
            self.add_to_cell(cell, obj)

    def add_to_cell(self, cell, obj):
        if cell in self.hash:
            if not obj in self.hash[cell]:
                self.hash[cell].append(obj)

    def get_nearby(self, rect):
        nearby = []
        cells = self.get_cells(rect)

        for cell in cells:
            if cell in self.hash:
                nearby.extend(self.hash[cell])

        return nearby