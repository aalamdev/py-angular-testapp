var fs = require('fs')
fs.readFile(process.argv[2], 'utf8', function (err,data) {
  if (err) {
    return console.log(err);
  }
  var result = data.replace(new RegExp(process.argv[3], 'g'), process.argv[4]);
  fs.writeFile(process.argv[2], result, 'utf8', function (err) {
     if (err) return console.log(err);
  });
});
