import * as axios from 'axios'

export function sample () {
  return axios.get('/api/sample').then((resp) => {
    console.log('response:', resp)
    return resp.data
  })
}

export function postit (data) {
  return axios.post('/api/preferences', data).then((resp) => {
    console.log('response:', resp)
    return resp.data
  })
}
