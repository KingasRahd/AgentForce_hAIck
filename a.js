const { exec } = require('child_process');

exec('python helper.py', (error, stdout, stderr) => {
    if (error) {
        console.error(`Error: ${error.message}`);
        return;
    }
    if (stderr) {
        console.error(`Stderr: ${stderr}`);
        return;
    }
    

    const obj=JSON.parse(stdout);

 console.log("new Output:",obj[3]);
})