const header = document.querySelector('.header')
const popup = document.querySelector('.popup')
const authDiv = document.querySelector('.auth')
const productsItem = document.querySelectorAll('.products__item')
const url = window.location.href
const addCartBtn = document.querySelectorAll('#add-cart')

// Обработчики событий

function handlerHeader(e){
    const navList = document.querySelector('.nav__list')
    if (e.target.id === 'hamburger-menu'){
        navList.classList.toggle('active')
    }
}

function handlerPopup(e){
    const popupClose = document.querySelector('#popup__close')
    if (e.target.id === 'popup__close'){
        popup.classList.add('hide-popup')
    }
}

function handlerAuth(e) {
    const formBox = document.querySelector('.auth__form-box')
    const body = document.querySelector('body')
    if (e.target.id === 'login'){
        formBox.classList.toggle('active')
        body.classList.toggle('active')

    }
    if (e.target.id === 'signup'){
        formBox.classList.toggle('active')
        body.classList.toggle('active')
    }
}

// productsItem.forEach(el => {
//     const productId = el.dataset.productId
//     el.addEventListener('click', (e) => {
//         if (e.target.id === `add-cart-${productId}`){
//             e.preventDefault()
//             makeRequest(`/add-to-cart/${productId}`, 'GET')
//                 .then(res => res.json())
//                 .then(res => {
//                     console.log('click')
//                     console.log(res)
//                 })
//                 .catch(err => err)
//         }
//     })
// })

addCartBtn.forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault()
        const productId = e.target.dataset.productId
        console.log(productId)
        response = makeRequest(`/add-to-cart/${productId}/`, 'GET')
            .then(res => res.json())
            .then(res => {
                console.log('click')
            })
            .catch(err => err)
    })
})

if (authDiv){
    authDiv.addEventListener('click', handlerAuth)
}

popup.addEventListener('click', handlerPopup)

header.addEventListener('click', handlerHeader)

// Обработчики событий


// Работа с запросами

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

async function makeRequest(url, method, body) {
    const headers = {
        "X-Requested-With": "XMLHttpRequest",
        'Content-Type': 'application/json'
    }
    if (method === 'POST'){
        headers['X-CSRFToken'] = csrftoken
    }

    let response = await fetch(url, {
        method: method,
        headers: headers,
        body: body,
    })
    if (!response.ok){
        throw Error(response.statusText)
    }
    return await response
}




// async function makeRequest(url, method, body) {
//     const headers = {
//         "X-Requested-With": "XMLHttpRequest",
//         'Content-Type': 'application/json'
//     }
//     if (method === 'POST'){
//         headers['X-CSRFToken'] = csrftoken
//     }
//
//     let response = await fetch(url, {
//         method: method,
//         headers: headers,
//         body: body,
//     })
//     if (!response.ok){
//         throw Error(response.statusText)
//     }
//     return await response
// }
//
// function getProducts(){
//     let response = makeRequest('/products/', 'GET')
//         .then(res => res.json())
//         .then(res => {
//             renderProducts(res)
//         })
//         .catch(err => err)
// }
//
// getProducts()
//
// function renderProducts(res){
//     const data = res
//     console.log(data)
// }
