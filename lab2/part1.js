
// 2022-CS-31
const fs = require('fs');

const fileName = 'test_files/i.txt';

fs.readFile(fileName, 'utf8', (err, data) => {
    if (err) {
        console.error("Error: Could not open " + fileName);
        return;
    }
    console.log(data);
});