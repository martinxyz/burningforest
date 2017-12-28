export function expand (axiom, rules) {
  let result = ''
  for (let i = 0, len = axiom.length; i < len; i++) {
    let c = axiom.charAt(i)
    result += rules[c] || c
  }
  return result
}

export const terminalSymbols = new Set('-+[]{.}')

export function render (canvas, s, angle) {
  let ctx = canvas.getContext('2d')
  // ctx.fillStyle = '#ffff'
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  // ctx.fillStyle = '#0003'
  // ctx.fillRect(10, 10, 100, 100)

  ctx.lineWidth = 3

  const phiStep = angle / 360 * 2 * Math.PI
  const lineLength = 20
  let x = canvas.width / 2
  let y = 3 * canvas.height / 4
  let phi = -Math.PI / 2
  let stack = []
  for (let c of s) {
    if (c === '+') phi += phiStep
    if (c === '-') phi -= phiStep
    if (c === '[') {
      stack.push([x, y, phi])
    }
    if (c === ']' && stack.length) {
      [x, y, phi] = stack.pop()
    }
    if (c.match(/[A-Z]/)) {
      // let x0 = x, y0 = y
      ctx.beginPath()
      ctx.moveTo(x, y)
      x += lineLength * Math.cos(phi)
      y += lineLength * Math.sin(phi)
      ctx.lineTo(x, y)
      ctx.stroke()
    }
  }
}
