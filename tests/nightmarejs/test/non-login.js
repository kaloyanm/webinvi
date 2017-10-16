const Nightmare = require('nightmare')
const assert = require('assert')
const Config = require('../config')

describe('Non login tests', function() {
  // Recommended: 5s locally, 10s to remote server, 30s from airplane ¯\_(ツ)_/¯
  this.timeout(Config.timeout)

  let nightmare = null
  beforeEach(() => {
    nightmare = new Nightmare()
  })

  describe('/ (Home Page)', () => {
    it('should load without error', done => {
      // your actual testing urls will likely be `http://localhost:port/path`
      nightmare.goto(Config.getUrl(''))
        .end()
        .then(function (result) { assert.equal(200, result.code); done() })
        .catch(done)
    })
  })

  describe('/login/', () => {
    it('should load without error', done => {
      nightmare.goto(Config.getUrl('login/'))
        .end()
        .then(function (result) { assert.equal(200, result.code); done() })
        .catch(done)
    })
  })

  describe('/registration/', () => {
    it('should load without error', done => {
      nightmare.goto(Config.getUrl('registration/'))
        .end()
        .then(function (result) { assert.equal(200, result.code); done() })
        .catch(done)
    })
  })

  describe('/contact/', () => {
    it('should load without error', done => {
      nightmare.goto(Config.getUrl('contact/'))
        .end()
        .then(function (result) { assert.equal(200, result.code); done() })
        .catch(done)
    })
  })

})
