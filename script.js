const api = "/tasks";

function loadTasks(){
fetch(api)
.then(res => res.json())
.then(tasks => {

const list = document.getElementById("taskList");
list.innerHTML = "";

tasks.forEach(task => {

const li = document.createElement("li");

if(task.completed){
li.classList.add("completed");
}

li.innerHTML = `
<span>${task.title}</span>

<div>
<button onclick="completeTask(${task.id})">✔</button>
<button onclick="editTask(${task.id}, '${task.title}')">✏</button>
<button onclick="deleteTask(${task.id})">🗑</button>
</div>
`;

list.appendChild(li);

});

});
}

function addTask(){
const input = document.getElementById("taskInput");

if(input.value.trim() === "") return;

fetch(api,{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
title: input.value
})
})
.then(()=>{
input.value="";
loadTasks();
});
}

function deleteTask(id){
fetch(`${api}/${id}`,{
method:"DELETE"
})
.then(()=>loadTasks());
}

function completeTask(id){
fetch(`${api}/${id}/complete`,{
method:"PUT"
})
.then(()=>loadTasks());
}

function editTask(id,title){
const newTitle = prompt("Edit task:", title);

if(!newTitle) return;

fetch(`${api}/${id}`,{
method:"PUT",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
title:newTitle
})
})
.then(()=>loadTasks());
}

loadTasks();