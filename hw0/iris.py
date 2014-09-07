#!/usr/bin/env python
from numpy import array
from matplotlib import pyplot as plot

SOURCE_FILE = "iris.data"


class Iris(object):
    def __init__(self, data_str):
        data = data_str.split(",")
        self.sepal_length_mm = int(float(data[0]) * 10)
        self.sepal_width_mm = int(float(data[1]) * 10)
        self.pedal_length_mm = int(float(data[2]) * 10)
        self.pedal_width_mm = int(float(data[3]) * 10)

        # Trim "Iris-" and the trailing "\n"
        self.species = data[4][5:-1]
        self._measurements = None

    @property
    def sizes_array(self):
        if not self._measurements:
            self._measurements = array([
                self.sepal_length_mm, 
                self.sepal_width_mm, 
                self.pedal_length_mm,
                self.pedal_width_mm
            ])
        return self._measurements

    def __repr__(self):
        return ("%s"
                "\n\t%fmm sepal length"
                "\n\t%fmm sepal width"
                "\n\t%fmm pedal length"
                "\n\t%fmm pedal width\n"
                % (self.species, self.sepal_length_mm,
                    self.sepal_width_mm, self.pedal_length_mm,
                    self.pedal_width_mm))


class IrisData(object):
    @classmethod
    def species_color(cls, species):
        if species.lower() == "setosa":
            return "r"
        elif species.lower() == "versicolor":
            return "g"
        elif species.lower() == "virginica":
            return "b"
        else:
            raise AttributeError("Invalid species %s" % species)

    @classmethod
    def attribute_name(cls, index):
        try:
            return [
                "Sepal Length",
                "Sepal Width",
                "Pedal Length",
                "Pedal Width"
            ][index]
        except IndexError as e:
            print e

    def __init__(self, iris_list):
        self.attributes = array([iris.sizes_array for iris in iris_list])
        self.species = array([iris.species for iris in iris_list])


def load_data(infile):
    data = []
    for line in infile:
        try:
            data.append(Iris(line))
        except ValueError as e:
            pass
    return IrisData(data)


def draw_scatter_plots(data):
    colors = [IrisData.species_color(c) for c in data.species]
    plot_num = 1
    for i in range(4):
        for j in range(4):
            print "%d-%d" % (i, j)
            draw_one_scatter(data, j, i, plot_num, colors)
            plot_num += 1
    plot.show()
    plot.savefig("iris-scatterplot.png")


def draw_one_scatter(data, x, y, num, colors):
    plot.subplot(4, 4, num)
    if x == y:
        plot.text(0.1, 0.5, IrisData.attribute_name(x))
    else:
        #plot.xlabel(IrisData.attribute_name(x) + "mm")
        #plot.ylabel(IrisData.attribute_name(y) + "mm")
        xs = array([row[x] for row in data.attributes])
        ys = array([row[y] for row in data.attributes])
        plot.scatter(xs, ys, c=colors)


def main():
    with open(SOURCE_FILE, "r") as infile:
        data = load_data(infile)
    draw_scatter_plots(data)

if __name__ == "__main__":
    main()
