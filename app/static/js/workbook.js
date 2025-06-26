const dropArea = document.getElementById("drop-area");
const fileElem = document.getElementById("fileElem");
const fileSelect = document.getElementById("fileSelect");

// Prevent default behavior
["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
  dropArea.addEventListener(eventName, e => e.preventDefault(), false);
  dropArea.addEventListener(eventName, e => e.stopPropagation(), false);
});

["dragenter", "dragover"].forEach(eventName => {
  dropArea.addEventListener(eventName, () => dropArea.classList.add("highlight"), false);
});

["dragleave", "drop"].forEach(eventName => {
  dropArea.addEventListener(eventName, () => dropArea.classList.remove("highlight"), false);
});

// Handle drop
dropArea.addEventListener("drop", handleDrop, false);
fileSelect.addEventListener("click", () => fileElem.click());
fileElem.addEventListener("change", () => {
  handleFiles(fileElem.files);
});

function handleDrop(e) {
  const dt = e.dataTransfer;
  const files = dt.files;
  handleFiles(files);
}

function handleFiles(files) {
  if (files.length > 0 && files[0].type === "application/pdf") {
    const formData = new FormData();
    formData.append("pdf", files[0]);

    fetch("/upload_pdf", {
      method: "POST",
      body: formData
    })
    .then(res => res.json())
    .then(data => {
        // Send extracted JSON to /edit_workbook and open the response as a new page
        fetch("/edit_workbook", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.text())
        .then(html => {
            // Open the HTML in a new tab
            const newWindow = window.open();
            newWindow.document.write(html);
            newWindow.document.close();
        })
        .catch(error => console.error("Failed to open workbook editor:", error));
    })
    .catch(err => {
      console.error(err);
      alert("❌ Upload failed.");
    });
  } else {
    alert("❌ Please upload a valid PDF file.");
  }
}
