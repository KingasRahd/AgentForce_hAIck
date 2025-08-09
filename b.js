// Node.js
const { spawn } = require("child_process");
const sam={'query':"JavaScript File Info"}
const py = spawn("python", ["sag.py", `${sam.query}`,"fghj"]);
py.stdout.on("data",function(data){
console.log(data.toString())
})
