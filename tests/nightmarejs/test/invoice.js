const Nightmare = require('nightmare')
const assert = require('chai').assert
const Config = require('../config')

describe('Invoice Add/Edit/Delete', function() {
  // Recommended: 5s locally, 10s to remote server, 30s from airplane ¯\_(ツ)_/¯
  this.timeout(Config.timeout)

  let nightmare = new Nightmare(Config.nightmareOptions)
  after(function() {
    nightmare.halt()
  });

  describe('Test invoice functionality', () => {
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


    let addedInvoiceUrl = null;
    it('add invoice', done => {
      nightmare.goto(Config.getUrl('invoices/invoice/'))
        .wait(1000)
        .type('#id_client_name', 'Въкат Амян')
        .type('#id_client_eik', null)
        .type('#id_client_eik', '87654321')
        .type('#id_client_dds', null)
        .type('#id_client_dds', '87654321')
        .type('#id_client_city', null)
        .type('#id_client_city', 'Село Бело')
        .type('#id_client_address', null)
        .type('#id_client_address', 'ул. Първа 1')
        .type('#id_client_mol', null)
        .type('#id_client_mol', 'Въкат Амян')
        .type('input[name=form-0-name]', 'Домати')
        .type('input[name=form-0-quantity]', null)
        .type('input[name=form-0-quantity]', '10')
        .type('input[name=form-0-measure]', 'кг')
        .type('input[name=form-0-unit_price]', '1')
        .type('#id_payment_iban', '342384623468')
        .type('#id_payment_swift', 'BPBIBGSF')
        .type('#id_payment_bank', 'Allen-Mcclure')
        .type('#id_accepted_by', 'Доматояден червей')
        .type('#id_created_by', 'Доматопродавен червей')
        .click('button[type=submit]')
        .wait(3000)
        .evaluate(() => {
          return {
            errorCount: $('.error').length,
            url: window.location.href,
            total: $('#total').val()
          }
        })
        .then(data => {
          addedInvoiceUrl = data.url

          assert.equal(data.errorCount, 0, 'There are form errors')
          assert.equal(data.total, '10', 'Total price incorrect')
          done();
        })
        .catch(done)
    })

    it('edit invoice', done => {
      nightmare.goto(Config.getUrl(addedInvoiceUrl))
        .wait(1000)
        .click('#add-item')
        .type('input[name=form-1-name]', 'Чушки')
        .type('input[name=form-1-quantity]', null)
        .type('input[name=form-1-quantity]', '10')
        .type('input[name=form-1-measure]', 'кг')
        .type('input[name=form-1-unit_price]', '2')
        .wait(1000)
        .click('button[type=submit]')
        .wait(1000)
        .evaluate(() => {
          return {
            errorCount: $('.error').length,
            total: $('#total').val()
          }
        })
        .then(data => {
          assert.equal(data.errorCount, 0, 'There are form errors')
          assert.equal(data.total, '30', 'Total price incorrect')
          done();
        })
        .catch(done)
    })

    it('delete invoice', done => {
      nightmare.goto(Config.getUrl(addedInvoiceUrl))
        .wait(1000)
        .click('#delete-button')
        .wait(1000)
        .click('.positive.button')
        .evaluate((addedInvoiceUrl) => {
          let deleted = true;
          // Check that the link is not in the invoices table
          $('td > a').each(function (idx, el) {
            if (addedInvoiceUrl.endsWith(el.href)){
              deleted = false;
            }
          });
          return {
            errorCount: $('.error').length,
            deleted: deleted,
          }
        }, addedInvoiceUrl)
        .then(data => {
          assert.equal(data.errorCount, 0, 'There are form errors')
          assert.isTrue(data.deleted, 'failed to delete invoice')
          done();
        })
        .catch(done)
    })

  })

})
