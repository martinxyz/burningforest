import cairo
import math
import numpy
import random


def expand(system):
    limit = system.get('limit', 5000)
    s = system['axiom']
    rules = system['rules']
    iterations = system.get('iterations', 3)

    for i in range(iterations):
        s_new = ''
        for c in s:
            # s_new += random.choice(rules.get(c, [c]))
            s_new += rules.get(c, c)
        s = s_new
        if len(s) > limit:
            break
    return s[:limit]


def render(system):
    w, h = system.get('w', 200), system.get('h', 200)
    s = expand(system)
    surface = cairo.ImageSurface(cairo.Format.ARGB32, w, h)
    ctx = cairo.Context(surface)
    ctx.set_line_width(3)

    line_length = system.get('lineLength', 20)
    phi_step = system.get('angle', 20) / 360 * 2 * math.pi
    x = w / 2
    y = 3 * h / 4
    phi = - math.pi

    ctx.move_to(x, y)
    stack = []
    for c in s:
        if c == '?': pass
        elif c == '+': phi += phi_step
        elif c == '-': phi -= phi_step
        elif c == '[': stack.append((x, y, phi))
        elif c == ']':
            if stack:
                x, y, phi = stack.pop()
        else:
            ctx.move_to(x, y)
            ctx.set_line_width(0.1 + random.random() * 5)
            x += line_length * math.cos(phi)
            y += line_length * math.sin(phi)
            if c != ' ':
                ctx.line_to(x, y)
                ctx.stroke()

    return numpy.ndarray(
      shape=(h, w, 4),
      dtype=numpy.uint8,
      buffer=surface.get_data()
    )[:,:,3]


if __name__ == '__main__':
    system = {
        'angle': 10,
        'axiom': 'GGGGGG',
        'rules': {
            'G': 'G++[F]',
            'F': '-----F---[G]'
        }
    }
    buf = render(system)
    import scipy.misc
    scipy.misc.imsave('render-test.png', buf)
