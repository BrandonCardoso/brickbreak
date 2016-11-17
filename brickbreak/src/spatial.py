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
        for point in [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]:
            cell = (math.floor(point[0] / self.cell_width),
                    math.floor(point[1] / self.cell_height))
            if not cell in cells:
                cells.append(cell)

        return cells

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