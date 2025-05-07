const cards = document.querySelectorAll('.flashcardcontent');
for (let i = 0; i < cards.length; i++) {
    cards[i].addEventListener('click', function() {
        const innerCard = cards[i].querySelector('.card-inner');
        innerCard.classList.toggle('flipped');
    });
}
