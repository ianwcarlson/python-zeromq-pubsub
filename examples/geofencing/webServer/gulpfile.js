var gulp = require('gulp');
var jshint = require('gulp-jshint');
var clean = require('gulp-clean');
 
var srcFiles = [
	'app/*.js',
	'node_modules/leaflet/dist/leaflet.css',
	'node_modules/leaflet/dist/leaflet.js',
	'node_modules/leaflet-draw/dist/leaflet.draw.js',
	'node_modules/leaflet-draw/dist/leaflet.draw.css'
];

var srcImages = [
	'node_modules/leaflet-draw/dist/images/*'
];

gulp.task('lint', function() {
    return gulp.src('app/*.js')
	.pipe(jshint())
	.pipe(jshint.reporter('default'));
});
 
gulp.task('copySource', function(){
	return gulp.src(srcFiles)
	.pipe(gulp.dest('dist/'));
});

gulp.task('copyImages', function(){
	return gulp.src(srcImages)
	.pipe(gulp.dest('dist/images/'))
})

gulp.task('clean', function () {
    return gulp.src('dist/', {read: false})
        .pipe(clean());
});

gulp.task('default', ['lint']);

gulp.task('build', ['copySource', 'copyImages']);