let comments = document.querySelectorAll('a.reply')
let close = document.querySelector('#close-reply')
let reply_to = document.querySelector('#reply-to')
let form = document.querySelector('#comment-form')
let inp = document.querySelector('#id_parent')
let reply_text = document.querySelector('#reply-text')



close.addEventListener('click', evt => {
    reply_to.classList.add('d-none')
    inp.value = ''
})

comments.forEach(c => {
    c.addEventListener('click', evt => {
        inp.value = c.dataset.id
        form.scrollIntoView({behavior: 'smooth', block: 'start'})
        reply_text.innerText = `پاسخ به "${c.dataset.name}" `
        reply_to.classList.remove('d-none')
    })
})