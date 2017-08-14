module.exports = {
	plugins: [
		require('css-mqpacker'),
		require('autoprefixer')({
      browsers: [
        'last 2 versions'
      ]
    }),
		require('cssnano')({
			reduceIdents: {
				keyframes: false
			},
			discardUnused: {
				keyframes: false
			}
		})
	]
};
