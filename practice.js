const test = {
    testOne: 1,
    testTwo: 2,
    testThree: 3
}

for (const [key, value] of Object.entries(test)){
    console.log(key, value);
    
}