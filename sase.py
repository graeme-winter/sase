from dials.array_family import flex
import math


def energy_intensity_for_run(run):
    energy = "%s_energy.txt" % run
    intensity = "%s_intensity.txt" % run

    for rx, ry in zip(open(energy), open(intensity)):
        x = flex.double(map(float, rx.strip().split(",")))
        y = flex.double(map(float, ry.strip().split(",")))

        # only yeild useful spectra
        if flex.max(y) > 0:
            yield x, y


def filter_energy(energy, intensity, energy_range):
    sel = (energy >= energy_range[0]) & (energy <= energy_range[1])

    total_intensity = flex.sum(intensity)
    average = flex.sum(intensity.select(sel)) / sel.count(True)
    return average / total_intensity


def analyse(run, energy_min, energy_max):
    from matplotlib import pyplot

    means = []
    for energy, intensity in energy_intensity_for_run(run):
        mean = 100 * filter_energy(energy, intensity, (energy_min, energy_max))
        means.append(mean)

    mean = sum(means) / len(means)
    var = sum((v - mean) ** 2 for v in means)

    sorted_mean = sorted(means)

    pyplot.plot(means)
    pyplot.plot(sorted_mean)
    pyplot.show()


if __name__ == "__main__":
    import sys

    analyse(sys.argv[1], 7998, 8002)
