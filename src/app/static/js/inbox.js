document.addEventListener("DOMContentLoaded", function () {
    const receivedMessageList = document.getElementById('receivedMessageList');
    const sentMessageList = document.getElementById('sentMessageList');
    const selectedMessageContent = document.getElementById('selectedMessageContent');
    
    function handleTabClick(messageList) {
        messageList.addEventListener('click', function (event) {
            const listItem = event.target.closest('li');

            if (listItem) {
                const sender = listItem.dataset.sender;
                const messages = listItem.dataset.messages.split(',');
                const timestamp = listItem.dataset.timestamp;
                const label = listItem.dataset.label;

                // Updates the selected conversation on the right
                $('#selected-card-body').removeClass('d-flex align-items-center justify-content-center')
                selectedMessageContent.innerHTML = `<h6 class="text-muted">${timestamp}</h6><h5>${label}: ${sender}</h5><hr>`;

                messages.forEach(message => {
                    const messageDiv = document.createElement('div');
                    messageDiv.textContent = message.trim();
                    selectedMessageContent.appendChild(messageDiv);
                });

                // Remove active class from other list items
                const listItems = messageList.getElementsByTagName('li');
                for (const item of listItems) {
                    item.classList.remove('active');
                }

                // Add active class to the clicked list item
                listItem.classList.add('active');
            }
        });
    }
    // Handles click events for both tabs
    handleTabClick(receivedMessageList);
    handleTabClick(sentMessageList);
});