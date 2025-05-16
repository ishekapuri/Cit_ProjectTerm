var currentSlide = NaN;
var remainingCards = [];
var completedCards = [];

async function getData() {
  var url = window.location.href + "/api/remCards";
  console.log(url);
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    completedCards = await response.json();
    console.log(completedCards);
  } catch (error) {
    console.error(error.message);
  }
}


function startQuiz() {
    const quizContainer = document.getElementById("quiz-overlay");
    quizContainer.className = "d-flex justify-content-center align-items-center";
    quizContainer.classList.add('blurred')
    getData()
}

function stopQuiz() {
    const quizContainer = document.getElementById("quiz-overlay");
    quizContainer.className = "d-none";
    quizContainer.classList.remove('blurred')
}

function addCompletedCard() {

}

function logResult() {
    console.log(completedCards);
}

var myCarousel = document.querySelector('#cardCarousel')
var carousel = new bootstrap.Carousel(myCarousel, {
    wrap: false
})

document.querySelectorAll('#cardCarousel').forEach(function(carousel) {
    carousel.addEventListener('slide.bs.carousel', function(e) {
        var activeSlide = carousel.querySelector('.active');
        currentSlide = Array.prototype.indexOf.call(carousel.querySelectorAll('.carousel-item'), activeSlide);
        var slideTo = Array.prototype.indexOf.call(carousel.querySelectorAll('.carousel-item'), e.relatedTarget);
    });
});
