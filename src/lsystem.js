export function expand (axiom, rules) {
  let result = ''
  for (let i = 0, len = axiom.length; i < len; i++) {
    let c = axiom.charAt(i)
    result += rules[c] || c
  }
  return result
}
