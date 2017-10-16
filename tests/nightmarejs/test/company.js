const Nightmare = require('nightmare')
const assert = require('chai').assert
const Config = require('../config')

describe('Company Add/Edit/Delete', function() {
  // Recommended: 5s locally, 10s to remote server, 30s from airplane ¯\_(ツ)_/¯
  this.timeout(Config.timeout)

  let nightmare = new Nightmare(Config.nightmareOptions)
  after(function() {
    nightmare.halt()
  });


  describe('Test company functionality', () => {
    it('login with existing user', done => {
      nightmare.goto(Config.getUrl('login/'))
        .wait(1000)
        .type('#id_username', Config.testUser)
        .type('#id_password', Config.testPass)
        .click('#submit-id-submit')
        .wait(1000)
        .evaluate(() => {
          return $('a:contains("Изход")').length;
        })
        .then(logoutCount => {
          assert(logoutCount > 0, 'Logout button missing');
          done();
        })
        .catch(done)
    })


    let addedCompanyUrl = null;
    it('add company', done => {
      nightmare.goto(Config.getUrl('invoices/list/'))
        .click('nav > div> div > a.item:nth-child(3)') // Click 'companies'
        .wait(1000)
        .click('main > div>div> div > a:nth-child(2)') // click 'Add company'
        .wait(1000)
        .type('#id_name', 'Кошмарна компания')
        .type('#id_name_tr', 'Nightmare company')
        .type('#id_city', 'Пандемониум')
        .type('#id_city_tr', 'Pandemonium')
        .type('#id_address', 'ул. Лава 168')
        .type('#id_address_tr', 'Lava str. 168')
        .type('#id_mol', 'Азраел Ефтимов')
        .type('#id_mol_tr', 'Azrael Eftimov')
        .type('#id_eik', '2345678387')
        .type('#id_dds', '2345678387')
        .click('#submit-id-submit')
        .wait(1000)
        .evaluate(() => {
          var links = $('a:contains("Кошмарна компания")');
          // if (links.length != 1) {
          //   return Promise.reject('Add company/ company missing or present more than once after add')
          // }
          return links.attr('href') ;
        })
        .then(link => {
          assert.isString(link, 'Missing link for newly added company');
          addedCompanyUrl = link;
          done();
        })
        .catch(done)
    })
    it('edit company', done =>{
      nightmare
        .goto(Config.getUrl(addedCompanyUrl))
        .wait(1000)
        .type('#id_name', null)
        .type('#id_name', 'Кошмарната компания')
        .type('#id_name_tr', null)
        .type('#id_name_tr', 'The Nightmare company')
        .click('#submit-id-submit')
        .wait(1000)
        .evaluate(() => {
          var links = $('a:contains("Кошмарната компания")');
          return links.attr('href') ;
        })
        .then(link => {
          assert.isString(link, 'Missing link for Edited company');
          done()
        })
        .catch(done)
    });

    it('delete company', done =>{
      nightmare
        .goto(Config.getUrl(addedCompanyUrl))
        .click('#delete-button')
        .evaluate(() => {
          var links = $('a:contains("Кошмарната компания")');
          // if (links.length != 1) {
          //   return Promise.reject('Add company/ company missing or present more than once after add')
          // }
          return links.attr('href') ;
        })
        .then(link => {
          assert.notExists(link, 'Delete company failed');
          done();
        })
        .catch(done)

    })
  })

})
