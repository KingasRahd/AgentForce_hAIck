const bar = document.getElementById('progress-bar');
let c=0
let prog=0;
function sam(len){   
    c++;
    let prog=Math.trunc(((c/len)*100));
    if(prog<=100){
    bar.innerText = `Your Progress : ${prog}%`;
    }
    else{
        bar.innerText = `Task Completed!!`
    }
}


