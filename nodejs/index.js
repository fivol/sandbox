const http = require('http')

const server = http.createServer((req, res) => {
    res.end('Hello NodeJS V2')
})


server.listen(4000, () => {
    console.log('Sever started...')
})