addTaskButton = document.querySelector(".add-task-btn");
closeModalButton = document.querySelector(".close-modal-btn");
modal = document.querySelector(".modal");

addTaskButton.onclick = function () {
    modal.showModal();
}


closeModalButton.onclick = function () {
    modal.close();
}
