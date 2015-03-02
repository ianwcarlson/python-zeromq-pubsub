var gulp = require('gulp');
var jshint = require('gulp-jshint');
var clean = require('gulp-clean');
 
var srcFiles = [
	'app/*.js',
	'clientLibs/leaflet/dist/leaflet.css',
	'clientLibs/leaflet/src/Leaflet.js',
	'clientLibs/leaflet-draw/dist/leaflet.draw.js',
	'clientLibs/leaflet-draw/dist/leaflet.draw.css'
]

gulp.task('lint', function() {
    return gulp.src('app/*.js')
	.pipe(jshint())
	.pipe(jshint.reporter('default'));
});
 
gulp.task('build', function(){
	return gulp.src(srcFiles)
	.pipe(gulp.dest('dist/'));
});

gulp.task('clean', function () {
    return gulp.src('dist/', {read: false})
        .pipe(clean());
});

gulp.task('default', ['lint', 'clean', 'build'])