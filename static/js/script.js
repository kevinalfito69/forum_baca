function submitProfilePictureForm() {
    document.getElementById('profileForm').submit()
}
function deleteProfilePicture() {
    document.getElementById('profileForm').reset();
    submitProfilePictureForm()
}