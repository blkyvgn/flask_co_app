const csrftoken = document.querySelector('meta[name="csrf-token"]').content
const fetchHeaders = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken,
}

