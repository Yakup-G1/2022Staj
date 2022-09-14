import matplotlib.pyplot as plt

# Draw multiple points.
def draw_multiple_points():

    # x axis value list.
    x_number_list = [1, 4, 9, 16, 25]

    # y axis value list.
    y_number_list = [1, 2, 3, 4, 5]

    # Draw point based on above x, y axis values.
    plt.scatter(x_number_list, y_number_list, s=10)

    # Set chart title.
    plt.title("Extract Number Root ")

    # Set x, y label text.
    plt.xlabel("Number")
    plt.ylabel("Extract Root of Number")
    plt.show()

if __name__ == '__main__':
    draw_multiple_points()