from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import my_utils

legend = """
    iteration: %d
    eeta: %g
    theta: %s
    loss_function: %s
    threshold: %g
    loss: %g
    """


def hypothesis_plot(x, y):
    ax = plt.subplot(gs[0, :])
    ax.set_title('Hypothesis Function and Scatter Plot')

    x_line = np.linspace(xlim[0], xlim[1], 200)
    x_line.shape = [200, 1]
    x_line = np.insert(x_line, 0, 1.0, axis=1)
    theta = np.zeros([x.shape[1], ])
    y_line = np.matmul(theta, np.transpose(x_line))

    x = np.delete(x, 0, axis=1)
    x_line = np.delete(x_line, 0, axis=1)

    plt.xlabel("Acidity")
    plt.ylabel("Density")
    plt.xlim(xlim)
    plt.ylim(ylim)

    plt.scatter(x, y)
    hypothesis_function, = plt.plot(x_line, y_line, '#FF4500')

    return hypothesis_function, ax


def update_hypothesis_plot(theta, cur_legend):
    x_line = np.linspace(xlim[0], xlim[1], 200)
    x_line.shape = [200, 1]
    x_line = np.insert(x_line, 0, 1.0, axis=1)
    y_line = np.matmul(theta, np.transpose(x_line))
    hthetax.set_ydata(y_line)
    hplot.legend([cur_legend])


def plot_error_surface():
    ax = fig.add_subplot(gs[1, 0], projection='3d')
    ax.set_title("3D surface of Error Function")
    surf = ax.plot_surface(theta0, theta1, jtheta, cmap='viridis')
    ax.set_zlim(-1, 100)
    ax.set_xlabel('theta0')
    ax.set_ylabel('theta1')
    ax.set_zlabel('jtheta')

    ax.zaxis.set_major_formatter(FormatStrFormatter('%.01f'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.01f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.08f'))

    init_theta = np.zeros([X.shape[1], ])
    init_error = mean_squared_error(init_theta)

    error_3d, = ax.plot([0], [0], [init_error], marker='o', markersize=3, color="#FF4500")
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    return error_3d


def update_error_surface(theta):
    xs, ys, zs = error_3d._verts3d
    xs = np.append(xs, theta[0])
    ys = np.append(ys, theta[1])
    zs = np.append(zs, mean_squared_error(theta))
    error_3d.set_xdata(xs)
    error_3d.set_ydata(ys)
    error_3d.set_3d_properties(zs)


def plot_error_contours():
    ax = fig.add_subplot(gs[1, 1])
    ax.set_title("Contours of Error Function")
    cs = ax.contour(theta0, theta1, jtheta, 10)
    # plt.clabel(cs, inline=1)

    ax.set_xlabel('theta0')
    ax.set_ylabel('theta1')

    ax.xaxis.set_major_formatter(FormatStrFormatter('%.08f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.01f'))

    init_theta = np.zeros([X.shape[1], ])
    init_error = mean_squared_error(init_theta)

    error_cs, = ax.plot([0], [0], marker='o', markersize=3, color="#FF4500")
    # Add a color bar which maps values to colors.
    # fig.colorbar(surf, shrink=0.5, aspect=5)

    return error_cs, cs, ax


def update_error_contour(theta):
    levels = np.append(cs.levels, mean_squared_error(theta))
    cs_plot.contour(theta0, theta1, jtheta, np.sort(levels))
    error_cs.set_xdata(np.append(error_cs.get_xdata(), theta[0]))
    error_cs.set_ydata(np.append(error_cs.get_ydata(), theta[1]))


def mean_squared_error(theta):
    j_theta = 0.5 * np.sum(np.square(Y - theta @ np.transpose(X)))
    return j_theta
    # or
    # z = np.linalg.norm(y - theta @ np.transpose(x))
    # j_theta = 0.5 * z * z


def change_in_theta(theta, old_theta):
    difference = np.absolute(np.subtract(theta, old_theta))
    return difference[np.argmax(difference)]


def change_in_error(theta, old_theta):
    return abs(mean_squared_error(theta) - mean_squared_error(old_theta))


def update_plots(theta, cur_legend):
    update_error_surface(theta)
    update_error_contour(theta)
    update_hypothesis_plot(theta, cur_legend)


def bgd(x, y, eeta, max_iter, threshold, loss_function="change_in_theta"):
    num_examples = x.shape[0]
    num_features = x.shape[1] - 1

    theta = np.zeros([num_features + 1, ])
    old_theta = np.zeros([num_features + 1, ])
    gradient = np.zeros([num_features + 1, ])

    iter = 0
    while True:
        iter += 1

        for jth_feature in range(0, num_features + 1):

            gradient_wrt_jth_feature = 0.0

            for ith_example in range(0, num_examples):
                gradient_wrt_jth_feature += (y[ith_example] - theta @ x[ith_example]).flatten()[0] * x[ith_example][jth_feature]

            gradient[jth_feature] = gradient_wrt_jth_feature
            theta[jth_feature] += eeta * gradient_wrt_jth_feature

        if loss_function == "change_in_theta":
            loss = change_in_theta(theta, old_theta)
        elif loss_function == "change_in_error":
            loss = change_in_error(theta, old_theta)
        elif loss_function == "error":
            loss = mean_squared_error(theta)
        elif loss_function == "gradient":
            gradient = np.abs(gradient)
            loss = gradient[np.argmax(gradient)]

        print(iter, theta, loss)

        cur_legend = legend % (iter, eeta, str(theta), loss_function, threshold, loss)
        update_plots(theta, cur_legend)
        plt.pause(0.02)
        # plt.savefig("bgd/%d.png" %iter)
        # TODO this should be before updation
        if (loss < threshold or iter == max_iter):
            break

        old_theta = np.array(theta)

    print("GDA solution")
    print(legend % (iter, eeta, str(theta), loss_function, threshold, loss))


def normalize(x):
    mean = np.mean(x, axis=0)
    std = np.std(x)
    return np.apply_along_axis(lambda x: (x - mean) / std, 1, x)


X, Y, xlim, ylim = my_utils.read_files("linearX.csv", "linearY.csv")

theta0 = np.arange(-1, 2, 0.01)
theta1 = np.arange(0, 0.0026, 0.0001)
theta0, theta1 = np.meshgrid(theta0, theta1)
jtheta = np.zeros(theta0.shape)

# TODO do this using some numpy trick
for i in range(0, len(jtheta)):
    for j in range(0, len(jtheta[0])):
        jtheta[i][j] = mean_squared_error(
            np.array([theta0[i][j], theta1[i][j]]))

gs = gridspec.GridSpec(2, 2)
# fig = plt.figure(figsize=(1920/96, 1080/96), dpi=96) # forcing it to be of size 1920x1080
fig = plt.figure()
hthetax, hplot = hypothesis_plot(X, Y)
error_3d = plot_error_surface()
error_cs, cs, cs_plot = plot_error_contours()

mng = plt.get_current_fig_manager()
# mng.full_screen_toggle()
mng.resize(*mng.window.maxsize())

bgd(X, Y, 0.021, 100, 0.0000000001, loss_function="change_in_theta")
# bgd(X, Y, 0.001, 100, 0.0000001, loss_function="gradient")
# bgd(X, Y, 0.01, 50000, 0.000119480, loss_function="error")
# bgd(X, Y, 0.01, 50000, 0.000000000001, loss_function="change_in_error")

plt.show()