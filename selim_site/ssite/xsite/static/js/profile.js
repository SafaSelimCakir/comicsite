// Düzenleme formunu aç/kapat
document.getElementById('editButton').addEventListener('click', function() {
    var editForm = document.querySelector('.edit-form');
    editForm.classList.add('show');
});

document.getElementById('cancelButton').addEventListener('click', function() {
    var editForm = document.querySelector('.edit-form');
    editForm.classList.remove('show');
});

// Profil fotoğrafı yükleme
document.getElementById('profilePictureUpload').addEventListener('change', function(event) {
    var reader = new FileReader();
    reader.onload = function(e) {
        document.querySelector('.profile-img').src = e.target.result;
    };
    reader.readAsDataURL(event.target.files[0]);
});
document.querySelector('form').addEventListener('submit', function (event) {
    const newPassword = document.getElementById('id_new_password').value;
    const confirmPassword = document.getElementById('id_confirm_password').value;

    if (newPassword !== confirmPassword) {
        event.preventDefault();
        alert('Yeni şifreler eşleşmiyor!');
    }
});