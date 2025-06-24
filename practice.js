


function addOne(add, list=[]){
    list.push(add);
    console.log(list);
    return function makeNull(){
        list = null;
        return list;
    }
}

const d = addOne(1);

console.log(d());
