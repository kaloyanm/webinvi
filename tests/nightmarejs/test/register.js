const Nightmare = require('nightmare')
const assert = require('assert')
const Config = require('../config')

describe('User registration', function() {
  // Recommended: 5s locally, 10s to remote server, 30s from airplane ¯\_(ツ)_/¯
  this.timeout(Config.timeout)

  let nightmare = null
  beforeEach(() => {
    nightmare = new Nightmare({show: true})
  })

  describe('Register a new user', () => {
    it('should register a new user', done => {
      nightmare.goto(Config.getUrl('registration/'))
        .wait(1000)
        .type('#id_username', Config.registerUser)
        .type('#id_password1', Config.registerPass)
        .type('#id_password2', Config.registerPass)
        .click('#submit-id-submit')
        .wait(2000)
        .end()
        .then(function (result) { assert.equal(200, result.code); done() })
        .catch(done)
    })
  })

})
