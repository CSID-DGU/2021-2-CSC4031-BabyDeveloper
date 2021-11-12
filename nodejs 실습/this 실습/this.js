const {odd, even} = require('./var');

console.log(odd);
console.log(this);
console.log(this === module.exports);

function a() {
    console.log(this === global);
}

a();
