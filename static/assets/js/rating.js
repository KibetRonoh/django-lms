const btn = document.querySelector('button');
const post = document.querySelector('.post');
const widget = document.querySelector('.star-widget');
const editBtn = document.querySelector('.edit');

btn.onclick = ()=> {
    widget.style.display = 'none';
    post.style.display = 'block';
    return false;
}