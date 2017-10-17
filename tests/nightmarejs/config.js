module.exports = {
  nightmareOptions: {
    show: true,
    typeInterval: 20,
    width: 1024,
    height: 768,
  },
  timeout: '10s',

  url: 'http://demo-client:demo-pass@webinvoices-local.dev/bg/',

  registerUser: 'nightmare@testing.com',
  registerPass: 'test1234',

  testUser: 'user5@demo.com',
  testPass: 'test1234',

  getUrl: function(path) {
    if (path.match(/^https?:\/\//)){
      return path;
    }
    path = path.replace(/^\/bg\//, '')
    return this.url + path;
  },
}
