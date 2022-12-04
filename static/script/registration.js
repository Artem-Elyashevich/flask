function goRegistration(){
    const btn = document.querySelector('.btn__go');
    

    btn.addEventListener('click', () => {
        window.location.href = 'http://127.0.0.1:5000/registration';
    })

}
goRegistration();