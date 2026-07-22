document.addEventListener("DOMContentLoaded", function(event) {
    // Sadece id_content alanını CKEditor'e dönüştür
    if (document.getElementById("id_content")) {
        CKEDITOR.replace('id_content', {
            height: 400,
            removeButtons: 'PasteFromWord'
        });
    }
});
