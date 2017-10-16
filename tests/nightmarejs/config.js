module.exports = {
  timeout: '5s',
  url: 'http://demo-client:demo-pass@webinvoices-local.dev/bg/',

  registerUser: 'nightmare@testing.com',
  registerPass: 'test1234',
  
  getUrl: function(path) {
    return this.url + path;
  },
}
