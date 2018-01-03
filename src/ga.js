function choose (chars, p) {
  let s = ''
  do {
    let i = Math.floor(Math.random() * chars.length)
    s += chars[i]
  } while (Math.random() > p)
  return s
}

export function createSample () {
  return {
    iterations: Math.ceil(Math.random() * 5),
    angle: 1 + 180 * Math.random(),
    lineLength: 20 * Math.random(),
    axiom: 'S',
    rules: {
      'S': choose('+-SL[]', 0.1),
      'L': choose('+-SAKL[]', 0.1),
      'A': choose('+-JKLA', 0.1)
    }
  }
}
