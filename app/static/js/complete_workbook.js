// Email tags container
const addTagBtn = document.getElementById('add-tag');
const tagContainer = document.getElementById('email-tags');
let emailList = [];

function createInputTag(value = '') {
    const tag = document.createElement('div');
    tag.className = 'email-tag editing';

    const input = document.createElement('input');
    input.type = 'email';
    input.value = value;
    input.placeholder = 'Enter email';

    input.addEventListener('blur', () => finishEditing(tag, input.value));
    input.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
        e.preventDefault();
        input.blur();
        }
    });

    tag.appendChild(input);
    tagContainer.appendChild(tag);
    input.focus();
}

function finishEditing(tag, value) {
    const trimmed = value.trim();
    if (!trimmed || emailList.includes(trimmed)) {
        tag.remove();
        return;
    }

    emailList.push(trimmed);
    tag.className = 'email-tag';

    tag.innerHTML = `
                <span>${trimmed}</span>
                <div class="actions">
                    <button class="edit-btn">✏️</button>
                    <button class="remove-btn">❌</button>
                </div>
            `;

    tag.querySelector('.edit-btn').onclick = () => editTag(tag, trimmed);
    tag.querySelector('.remove-btn').onclick = () => {
        emailList = emailList.filter(e => e !== trimmed);
        tag.remove();
    };

    tag.onclick = () => {
        tag.classList.toggle('active');
    };
}

function editTag(tag, oldValue) {
    tag.innerHTML = '';
    tag.classList.add('editing');
    emailList = emailList.filter(e => e !== oldValue);
    const input = document.createElement('input');
    input.type = 'email';
    input.value = oldValue;
    tag.appendChild(input);
    input.focus();

    input.addEventListener('blur', () => finishEditing(tag, input.value));
    input.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
        e.preventDefault();
        input.blur();
        }
    });
}
addTagBtn.addEventListener('click', () => createInputTag());



// Style and generate button
function showNotification(message) {
    let notification = document.getElementById("loadingMessage");
    notification.innerText = message;
    notification.style.top = "20px";
    notification.style.display = "block";

    // Hide after 7 seconds (if success)
    setTimeout(() => {
        notification.style.top = "-60px";
    }, 7000);
}

function show_page(id_page) {
    
}

document.getElementById("generatePdfBtn").addEventListener("click", function () {
    // Get the initial data from the JSON passed from Flask
    let workbookData = structuredClone(workbookDataFromServer);

    for (let date_tab in workbookData) {
        // Get form inputs and update `workbookData`
        let formElement = document.getElementById("workbookForm__"+date_tab);
        let formData = new FormData(formElement);

        let checkbox_page = formElement.querySelector("#show-page");

        let date = "";
        for (let [name, value] of formData.entries()) {
            // Extract section and index
            let parts = name.split("__");
            date = parts[0];
            let section = parts[1];
            let item = parts[2];

            workbookData[date][section][item][1] = value
        }
        if (checkbox_page.checked == false) {
            delete workbookData[date];
        }
    }

    // add background info to json
    var checkBox = document.getElementById("show-background");
    if (checkBox.checked == true){
        workbookData.background = true;
      } else {
        workbookData.background = false;
    }
    // add email list to json
    workbookData.email_list = emailList;

    // add title (month) to json
    workbookData.title = document.getElementById("title").textContent;

    showNotification("⏳ Generating your PDF... Please wait.");

    // Send the updated data to Flask
    fetch("/generate_workbook_pdf", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(workbookData)
    })
    .then(response => response.blob())  // Expecting a PDF
    .then(blob => {
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement("a");
        a.href = url;
        a.download = "workbook.pdf";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        showNotification("✅ Your PDF has been generated!");
    })
    .catch(error => {
        console.error("Error:", error);
        // Hide yhe loading message
        showNotification("❌ Error generating PDF!");
    });
});



document.getElementById("previewPdfBtn").addEventListener("click", function () {
    // Get the initial data from the JSON passed from Flask
    let workbookData = structuredClone(workbookDataFromServer);

    for (let date_tab in workbookData) {
        // Get form inputs and update `workbookData`
        let formElement = document.getElementById("workbookForm__"+date_tab);
        let formData = new FormData(formElement);

        let checkbox_page = formElement.querySelector("#show-page");

        let date = "";
        for (let [name, value] of formData.entries()) {
            // Extract section and index
            let parts = name.split("__");
            date = parts[0];
            let section = parts[1];
            let item = parts[2];

            workbookData[date][section][item][1] = value
        }
        if (checkbox_page.checked == false) {
            delete workbookData[date];
        }
    }

    // add background info to json
    var checkBox = document.getElementById("show-background");
    if (checkBox.checked == true){
        workbookData.background = true;
      } else {
        workbookData.background = false;
    }
    // add email list to json
    workbookData.email_list = emailList;

    // add title (month) to json
    workbookData.title = document.getElementById("title").textContent;

    showNotification("⏳ Generating your PDF... Please wait.");

    // Send the updated data to Flask
    fetch("/generate_workbook_pdf", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(workbookData)
    })
    .then(response => response.blob())  // Expecting a PDF
    .then(blob => {
        let url = window.URL.createObjectURL(blob);
        document.getElementById("pdfFrame").src = url;
        document.getElementById("pdfOverlay").style.display = "block";
        document.getElementById("pdfModal").style.display = "block";
        showNotification("✅ Preview loaded!");
    })
    .catch(error => {
        console.error("Error:", error);
        // Hide yhe loading message
        showNotification("❌ Error generating PDF!");
    });
});
function closeModal() {
    document.getElementById("pdfOverlay").style.display = "none";
    document.getElementById("pdfModal").style.display = "none";
    document.getElementById("pdfFrame").src = "";
};

