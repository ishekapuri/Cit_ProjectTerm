
function startQuiz() {
    const quizContainer = document.getElementById("quiz-overlay");
    quizContainer.className = "d-flex justify-content-center align-items-center";
    quizContainer.classList.add('blurred')
}

function stopQuiz() {
    const quizContainer = document.getElementById("quiz-overlay");
    quizContainer.className = "d-none";
    quizContainer.classList.remove('blurred')
}

var myCarousel = document.querySelector('#cardCarousel')
var carousel = new bootstrap.Carousel(myCarousel, {
    wrap: false
})
