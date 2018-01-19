import * as lsystem from './lsystem.js'

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

export function createGoodSamples () {
  let samples = []
  const N = 100
  for (let i = 0; i < N; i++) {
    let sample = createSample()
    sample.score = evaluate(sample)
    samples.push(sample)
  }
  samples.sort((a, b) => a.score < b.score)
  // _.sortBy(samples, 'score')
  // console.log(score)
  return samples.slice(0, N / 10)
}

function evaluate (system) {
  let canvas = document.createElement('canvas')
  let w = 67
  let h = 126

  canvas.width = w
  canvas.height = h

  lsystem.render(canvas, system)
  let ctx = canvas.getContext('2d')
  let data = ctx.getImageData(0, 0, w, h).data

  let score = 0.0
  // console.log('length', data.length)
  for (let i = 0; i < data.length; i++) {
    score += data[i]
  }

  console.log('score', score)
  return score
}
