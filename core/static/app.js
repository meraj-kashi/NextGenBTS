document.addEventListener('DOMContentLoaded', function() {
    var addForm = document.getElementById('add-form');
    var tableBody = document.querySelector('.fancy-table tbody');
    var messageContainer = document.getElementById('message-container');
    var removeButtons = document.querySelectorAll('.remove-button');

    addForm.addEventListener('submit', function(event) {
        event.preventDefault();

        var nameInput = document.getElementById('name-input');
        var ipInput = document.getElementById('ip-input');
        var name = nameInput.value.trim();
        var ip = ipInput.value.trim();

        if (name && ip) {
            var data = {
                name: name,
                ip: ip
            };

            fetch('/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(function(response) {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Error: ' + response.statusText);
                }
            })
            .then(function(result) {
                var newRow = document.createElement('tr');
                newRow.innerHTML = `
                    <td>${tableBody.childElementCount + 1}</td>
                    <td>${name}</td>
                    <td>${ip}</td>
                    <td>${status}</td>
                `;
                tableBody.appendChild(newRow);

                nameInput.value = '';
                ipInput.value = '';

                showMessage(result.message);
            })
            .catch(function(error) {
                console.error(error);
                showMessage('Error occurred');
            });
        }
    });

    removeButtons.forEach(function(button) {
                button.addEventListener('click', function() {
                    var itemId = this.getAttribute('data-id');

                    fetch('/remove', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ id: itemId })
                    })
                    .then(function(response) {
                        if (response.ok) {
                            return response.json();
                        } else {
                            throw new Error('Error: ' + response.statusText);
                        }
                    })
                    .then(function(result) {
                        // Remove the row from the table
                        var row = button.closest('tr');
                        row.parentNode.removeChild(row);

                        showMessage(result.message);
                    })
                    .catch(function(error) {
                        console.error(error);
                        showMessage('Error occurred');
                    });
                });
            });

    function showMessage(message) {
        // Clear any existing message
        messageContainer.innerHTML = '';

        // Create a new message element
        var messageElement = document.createElement('p');
        messageElement.textContent = message;

        // Append the message element to the container
        messageContainer.appendChild(messageElement);
    }
});