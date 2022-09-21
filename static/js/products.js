// const productsBox = document.querySelector('.products__box')
//
//
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
// let page = 1
//
// function getProducts() {
//     makeRequest(`/products/?page=${page}`, 'GET')
//         .then(res => res.json())
//         .then(res => {
//             renderProducts(res)
//         })
//         .catch(err => err)
// }
// getProducts()
//
// function renderProducts(res){
//
//     const products = res.object_list
//
//     pagination(res.num_pages, res.current )
//     setTimeout(()=>{
//         products.forEach((el) => {
//             productsBox.innerHTML +=`
//                 <div class="products__item">
//                     <div class="item__view">
//                         <a href="" class="item__view-link">
//                             <img src="${el.image}" alt="">
//                         </a>
//                         <span class="item__discount">60%</span>
//                     </div>
//                     <div class="item__info">
//                         <a href=""><span>${el.category}</span></a>
//                         <h3 class="item__title">${el.name}</h3>
//                         <h4>${el.price}</h4>
//                         <ul class="item__icons">
//                             <li><i class="bx bx-heart"></i></li>
//                             <li><i class="bx bx-search"></i></li>
//                             <li><i class="bx bx-cart"></i></li>
//                         </ul>
//                     </div>
//                 </div>
//             `
//         })
//     }, 100)
// }
//
// function pagination(num_pages, current) {
//     const paginationLeft = document.querySelector('.pagination__left')
//     const paginationRight = document.querySelector('.pagination__right')
//
//     paginationRight.addEventListener('click', (e) =>{
//         e.preventDefault()
//         productsBox.innerHTML = ''
//         page += 1
//         getProducts()
//     })
//
//     paginationLeft.addEventListener('click', (e) => {
//         e.preventDefault()
//         productsBox.innerHTML = ''
//         page -= 1
//         getProducts()
//     })
//
// }
//
// pagination()