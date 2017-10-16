const Nightmare = require('nightmare')
const assert = require('chai').assert
const Config = require('../config')

console.log(assert);
describe('Non login tests', function() {
  // Recommended: 5s locally, 10s to remote server, 30s from airplane ¯\_(ツ)_/¯
  this.timeout(Config.timeout)

  let nightmare = null
  beforeEach(() => {
    nightmare = new Nightmare(Config.nightmareOptions)
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

  describe('/login (Forgotten password)', () => {
    it('should try to recover password', done => {
      let link = '.message ._flex-1:nth-child(2) a';
      let input = '#id_username_or_email';
      let el = '#pass-link-sent';

      nightmare
        .goto(Config.getUrl('login/'))
        .wait(link).click(link)
        .wait(input).type(input, Config.testUser)
        .click('#submit-id-submit')
        .wait(2000).exists(el)
        .end()
        .then((element) => {
          assert.isOk(element, 'element exists');
          done();
        })
        .catch(done)
    })
  })

})
