/*
Activity : Student Mark Analysis
Problem Statement :
A school has recorded 10 student marks in an array.
Your task is to analyze the marks using loop and if statements.

Marks
let marks = [85, 92, 78, 90, 88, 76, 95, 89, 84, 91];

Requirements:
use loop to iterate through all the marks
use an if statement to check whether each student has passed or failed.
Pass: Marks 50 or above
Fail: Marks below 50

Display the results in the console in the following format:
Student 1: 85 - Pass
Student 2: 42 - Fail

Count the total number of students who passed and failed

After the loop, display:
Total Passed: X
Total Failed: Y
*/

let marks = [85, 42, 78, 90, 38, 76, 55, 29, 84, 49];
let passed = 0;
let failed = 0;
let max = 0;
let less = 100;


for (let i = 0; i < marks.length; i++) {
    if (marks[i] >= 50) {
        console.log("Student " + (i + 1) + ": " + marks[i] + " - Pass");
        passed++;
    } else {
        console.log("Student " + (i + 1) + ": " + marks[i] + " - Fail");
        failed++;
    }
    if(max<marks[i]){
        max=marks[i];
    }
    if(less>marks[i]){
        less = marks[i];
    }
}

console.log("Total Passed: " + passed);
console.log("Total Failed: " + failed);
console.log("Highest Marks: " + max);
console.log("Least score: "+less);