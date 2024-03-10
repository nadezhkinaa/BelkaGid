var isValidPass = false;
var isValidEmail = false;
const form = document.querySelector('#form');
const EMAIL_REGEXP = /^(([^<>()[\].,;:\s@"]+(\.[^<>()[\].,;:\s@"]+)*)|(".+"))@(([^<>()[\].,;:\s@"]+\.)+[^<>()[\].,;:\s@"]{2,})$/iu;
const checkValidity = (input) => {
    input.classList.remove('text-field__input_valid');
    input.classList.remove('text-field__input_invalid');
    input.nextElementSibling.textContent = '';

    if (input.type == "email") {
        if (EMAIL_REGEXP.test(input.value)) {
        input.classList.add('text-field__input_valid');
        input.nextElementSibling.textContent = 'Отлично!';
        isValidEmail = true;
        }else{
        input.classList.add('text-field__input_invalid');
        input.nextElementSibling.textContent = input.validationMessage;
        isValidEmail = false;
        }
    }
    // строчная + заглавная + цифра, от 6 символов
if (input.type == "password") {
    var re = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}/;
    if (re.test(input.value)) {
        input.classList.add('text-field__input_valid');
   input.nextElementSibling.textContent = 'Отлично!';
   isValidPass = true;
        }else{
        input.classList.add('text-field__input_invalid');
   input.nextElementSibling.textContent = "Пароль должен содержать цифру, заглавную и прописную латинские буквы. Не менее 6 символов.";
       isValidPass = false;
        }
}
}


const checkValidityAll = () => {
    const inputs = form.querySelectorAll('input');
    inputs.forEach((input) => {
        checkValidity(input);
    });
}

const onCheckValidity = (e) => {
    const target = e.target;
    if (!target.classList.contains('text-field__input')) {
        return;
    }
    checkValidity(target);
}

form.addEventListener('change', onCheckValidity);
form.addEventListener('keydown', onCheckValidity);
form.addEventListener('keyup', onCheckValidity);
//checkValidityAll();


form.addEventListener('submit', (e) => {
    e.preventDefault();
    checkValidityAll();

    if (isValidEmail && isValidPass){window.location.replace("lichnkabinet.html");}


});