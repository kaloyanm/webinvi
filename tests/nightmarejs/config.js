module.exports = {
  nightmareOptions: {
    show: false,
    typeInterval: 20,
  },
  timeout: '10s',

  url: 'http://demo-client:demo-pass@webinvoices-local.dev/bg/',

  registerUser: 'nightmare@testing.com',
  registerPass: 'test1234',

  testUser: 'user5@demo.com',
  testPass: 'test1234',

  getUrl: function(path) {
    path = path.replace(/^\/bg\//, '')
    return this.url + path;
  },
}
