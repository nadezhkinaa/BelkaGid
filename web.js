function validate() {
    var userlogin = document.forms["form"]["login"].value;
    var userpassword = document.forms["form"]["password"].value;
    
// Проверяем, что логин и пароль не пустые
    if (userlogin.trim() === '' || userpassword.trim() === '') {
        alert("Поля заполни");
        return false; // Отменяем отправку формы
    }

    // Проверка дополнительных условий, например, длины пароля
    if (userpassword.length < 6) {
        alert('Пароль должен содержать не менее 6 символов.');
        return false; // Отменяем отправку формы
    }

    // Все проверки пройдены, форма валидна
    return true;
}