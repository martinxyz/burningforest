# import cairocffi as cairo
import cairo
import math
import numpy


def expand(system):
    limit = system.get('limit', 2000)
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
            raise ValueError('expansion too long')
            # break
    return s  # [:limit]


surface = None
ctx = None
def render(system):
    global surface, ctx
    w, h = system.get('w', 200), system.get('h', 200)
    s = expand(system)
    if surface is None:
        # surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        surface = cairo.ImageSurface(cairo.Format.ARGB32, w, h)
        ctx = cairo.Context(surface)

    ctx.save()
    # clear
    # ctx.set_source_rgba(255, 8, 255, 255)
    # ctx.paint()

    ctx.set_line_width(3)

    line_length = system.get('lineLength', 20)
    phi_step = system.get('angle', 20) / 360 * 2 * math.pi
    line_width = system.get('lineWidth', 2)
    scale_step = system.get('scaleStep', 1.2)
    x = w / 2
    y = 3 * h / 4
    phi = system.get('angle0', -180) / 360 * 2 * math.pi

    ctx.move_to(x, y)
    stack = []
    for c in s:
        if c == '?': pass
        elif c == '+': phi += phi_step
        elif c == '-': phi -= phi_step
        elif c == '>':
            line_width *= scale_step
            line_length *= scale_step
        elif c == '<':
            line_width /= scale_step
            line_length /= scale_step
        elif c == '[': stack.append((x, y, phi, line_width, line_length))
        elif c == ']':
            if stack:
                x, y, phi, line_width, line_length = stack.pop()
        else:
            ctx.set_line_width(line_width)
            ctx.move_to(x, y)
            # ctx.set_line_width(0.1 + random.random() * 5)
            x += line_length * math.cos(phi)
            y += line_length * math.sin(phi)
            if c != ' ':
                ctx.line_to(x, y)

                # causes out of memory:
                # ctx.set_line_cap(cairo.LINE_CAP_ROUND)

                ctx.stroke()

                # causes out of memory:
                # ctx.arc(x, y, line_width, 0, 2*math.pi)
                # ctx.fill()

    res = numpy.ndarray(
      shape=(h, w, 4),
      dtype=numpy.uint8,
      buffer=surface.get_data()
    )[:,:,3]
    res = res.copy()
    ctx.restore()
    surface = None
    ctx = None
    return res


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
