
const fs = require('fs');
let fileLines = []
let outputContent = '';
const allFileContents = fs.readFileSync('within15SecRawData.txt', 'utf-8');
allFileContents.split(/\r?\n/).forEach(line =>  {
  //console.log(`Line from file: ${line}`);
  if (line.startsWith('SIM_DATA_LOG:')) {
    let cleanDataLine = line.replace('SIM_DATA_LOG: ', '');
    cleanDataLine = cleanDataLine.replace(' ', '');
    fileLines.push(cleanDataLine + '\n');
    outputContent+=(cleanDataLine + '\n');
  }
});

//console.log('fileLines: ' + fileLines.length);
//console.log('outputContent: ' + outputContent);

fs.writeFile('within15Sec.csv', outputContent, err => {
    if (err) {
      console.error(err);
    }
    // file written successfully
  });