#!/usr/bin/env python
from numpy import array
from matplotlib import pyplot as plot

SOURCE_FILE = "iris.data"


class Iris(object):
    def __init__(self, data_str):
        data = data_str.split(",")
        self.sepal_length_cm = float(data[0])
        self.sepal_width_cm = float(data[1])
        self.pedal_length_cm = float(data[2])
        self.pedal_width_cm = float(data[3])

        # Trim "Iris-" and the trailing "\n"
        self.species = data[4][5:-1]
        self._measurements = None

    @property
    def sizes_array(self):
        if not self._measurements:
            self._measurements = array([
                self.sepal_length_cm, 
                self.sepal_width_cm, 
                self.pedal_length_cm,
                self.pedal_width_cm
            ])
        return self._measurements

    def __repr__(self):
        return ("%s"
                "\n\t%0.1fcm sepal length"
                "\n\t%0.1fcm sepal width"
                "\n\t%0.1fcm pedal length"
                "\n\t%0.1fcm pedal width\n"
                % (self.species, self.sepal_length_cm,
                    self.sepal_width_cm, self.pedal_length_cm,
                    self.pedal_width_cm))


class IrisData(object):
    @classmethod
    def species_color(cls, species, full_name=False):
        color = None
        if species.lower() == "setosa":
            color = "red"
        elif species.lower() == "versicolor":
            color = "green"
        elif species.lower() == "virginica":
            color = "blue"
        else:
            raise AttributeError("Invalid species %s" % species)

        if full_name:
            return color
        else:
            return color[0]

    @classmethod
    def attribute_name(cls, index):
        try:
            return [
                "Sepal Length",
                "Sepal Width",
                "Petal Length",
                "Petal Width"
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
    plot.style.use('ggplot')
    f, subplots = plot.subplots(4, 4)
    f.suptitle("setosa=red, versicolor=green, virginica=blue")
    for i in range(4):
        for j in range(4):
            draw_one_scatter(data, j, i, subplots[i][j], colors)
    plot.show()
    plot.savefig("iris-scatterplot.png")


def draw_one_scatter(data, x, y, subplot, colors):
    if x == y:
        subplot.text(0.5, 0.5, IrisData.attribute_name(x))
    else:
        # StackOverflow helped here. I knew there was a way to grab columns from
        # the matrix, but couldn't figure it out, and was using list comprehensions
        # instead. Source:
        #   http://stackoverflow.com/questions/4455076/numpy-access-an-array-by-column
        xs = data.attributes[:,x]
        ys = data.attributes[:,y]
        subplot.scatter(xs, ys, c=colors, alpha=0.6)


def main():
    with open(SOURCE_FILE, "r") as infile:
        data = load_data(infile)
    draw_scatter_plots(data)

if __name__ == "__main__":
    main()
