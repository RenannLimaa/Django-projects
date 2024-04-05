const addTaskButton = document.querySelector(".add-task-btn");
const closeModalButtons = document.querySelectorAll(".close-modal-btn");
const addTaskModal = document.querySelector(".add-task-modal");
const modals = document.querySelectorAll(".modal");

const taskButtons = document.querySelectorAll(".task-list");
const editTaskModal = document.querySelector(".edit-task-modal");
const editTaskForm = document.querySelector("#edit-task-form");

addTaskButton.onclick = function () {
        addTaskModal.showModal();
}

closeModalButtons.forEach(button => {
    button.addEventListener('click', function() {
        const modalToClose = button.closest('.modal');
        if (modalToClose) {
            modalToClose.close();
        }
    });
});

function saveTask() {
    const addTaskUrl = document.getElementById('edit-task-form').dataset.addTaskUrl;
    document.getElementById('edit-task-form').action = addTaskUrl;
    document.getElementById('edit-task-form').submit();
}

function deleteTask() {
    const deleteTaskUrl = document.getElementById('edit-task-form').dataset.deleteTaskUrl;
    document.getElementById('edit-task-form').action = deleteTaskUrl;
    document.getElementById('edit-task-form').submit();
}

function formatDate(inputDate) {
    var split_string = inputDate.split(','); 
    var datePart = split_string[0];
    var year = split_string[1]; 

    var date = [datePart, year].join(",");
    var date = new Date(date); 

        
    var month = (date.getMonth() + 1).toString().padStart(2, '0');
    var day = date.getDate().toString().padStart(2, '0');
    var year = date.getFullYear();

    return year + '-' + month + '-' + day 
}

taskButtons.forEach(taskButton => {
    taskButton.addEventListener('click', function () {
        const titleInput = editTaskForm.querySelector("#title");
        const descriptionInput = editTaskForm.querySelector("#description");
        const dueDateInput = editTaskForm.querySelector("#due-date");


        const taskName = taskButton.dataset.taskName;
        const taskDescription = taskButton.dataset.taskDescription;
        const taskDueDate = taskButton.dataset.taskDueDate;

        titleInput.value = taskName;
        descriptionInput.value = taskDescription;
        dueDateInput.value = formatDate(taskDueDate);

        editTaskModal.showModal();
    });
});
