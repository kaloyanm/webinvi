module.exports = {
  nightmareOptions: {
    show: true,
    typeInterval: 20,
  },
  timeout: '30s',

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
