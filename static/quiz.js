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

    var cards = await response.json();
    remainingCards = JSON.parse(cards.remainingCards);

    console.log(cards);
  } catch (error) {
    console.error(error.message);
  }
}

async function startQuiz() {
    const quizContainer = document.getElementById("quiz-overlay");
    quizContainer.classList.remove("d-none");
    quizContainer.classList.add("d-flex");
    await getData();
}

async function stopQuiz() {
    const quizContainer = document.getElementById("quiz-overlay");
    quizContainer.classList.add("d-none");
    quizContainer.classList.remove('blurred')
    await logResult();
    location.reload();
}

function addCompletedCard() {
    card = remainingCards[currentSlide];
    console.log(`Card: ${JSON.stringify(card)}`);
    completedCards.push(JSON.stringify(card));
    console.log(`Completed Cards: ${JSON.stringify(completedCards)}`);
}

async function logResult() {
    try {
        var url = window.location.href + "/api/update";
        const response = await fetch(url, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(completedCards),
        });
    } catch (error) {
        console.error(error.message);
    }
}

async function shuffleCards() {
    try {
        var url = window.location.href + "/api/shuffle";
        const response = await fetch(url, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(completedCards),
        });
    } catch (error) {
        console.error(error.message);
    }
    location.reload();
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
